#include "rclcpp/rclcpp.hpp"
#include "turtlesim/msg/pose.hpp"
#include "enc_turtle_cpp/msg/encrypted_data.hpp"
#include "openfhe/pke/openfhe.h"
#include <thread>

// Cereal 등록 매크로 추가
CEREAL_CLASS_VERSION(lbcrypto::CryptoParametersBGVRNS, 1)
CEREAL_CLASS_VERSION(lbcrypto::DCRTPoly, 1)
CEREAL_CLASS_VERSION(lbcrypto::SchemeBGVRNS, 1)
CEREAL_CLASS_VERSION(lbcrypto::CiphertextImpl<lbcrypto::DCRTPoly>, 1)

// 타입 등록
CEREAL_REGISTER_TYPE(lbcrypto::CryptoParametersBGVRNS)
CEREAL_REGISTER_TYPE(lbcrypto::SchemeBGVRNS)
CEREAL_REGISTER_TYPE(lbcrypto::CiphertextImpl<lbcrypto::DCRTPoly>)

// 다형성 관계 등록
CEREAL_REGISTER_POLYMORPHIC_RELATION(lbcrypto::CryptoParametersBase<lbcrypto::DCRTPoly>, lbcrypto::CryptoParametersBGVRNS)
CEREAL_REGISTER_POLYMORPHIC_RELATION(lbcrypto::SchemeBase<lbcrypto::DCRTPoly>, lbcrypto::SchemeBGVRNS)

using namespace lbcrypto;

class EncTurtlePlant : public rclcpp::Node {
public:
  EncTurtlePlant() : Node("enc_turtle_plant") {
    CCParams<CryptoContextBGVRNS> parameters;
    parameters.SetPlaintextModulus(65537);
    parameters.SetMultiplicativeDepth(2);
    parameters.SetSecurityLevel(SecurityLevel::HEStd_128_classic);
    parameters.SetRingDim(16384);  // 2의 14승 암호문 크기 약 1MB

    cc = GenCryptoContext(parameters);
    cc->Enable(PKE);
    cc->Enable(LEVELEDSHE);
    cc->Enable(ADVANCEDSHE);

    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    kp = cc->KeyGen();

    if (kp.secretKey) {
        cc->EvalMultKeyGen(kp.secretKey);
        cc->EvalSumKeyGen(kp.secretKey);
    } else {
        RCLCPP_ERROR(this->get_logger(), "Key generation failed!");
    }

    // QoS 설정
    rclcpp::QoS qos(10);
    qos.reliable();
    qos.durability_volatile();

    pose_sub_ = this->create_subscription<turtlesim::msg::Pose>(
        "turtle1/pose", qos,
        std::bind(&EncTurtlePlant::pose_callback, this, std::placeholders::_1));

    result_sub_ = this->create_subscription<enc_turtle_cpp::msg::EncryptedData>(
        "encrypted_result", qos,
        std::bind(&EncTurtlePlant::result_callback, this, std::placeholders::_1));

    encrypted_pub_ = this->create_publisher<enc_turtle_cpp::msg::EncryptedData>(
        "encrypted_pose", qos);
  }

private:
  void pose_callback(const turtlesim::msg::Pose::SharedPtr msg) {
    try {
      std::vector<int64_t> x_coord = {static_cast<int64_t>(msg->x * 1000)};
      std::vector<int64_t> y_coord = {static_cast<int64_t>(msg->y * 1000)};

      auto plaintext_x = cc->MakePackedPlaintext(x_coord);
      auto plaintext_y = cc->MakePackedPlaintext(y_coord);

      auto ciphertext_x = cc->Encrypt(kp.publicKey, plaintext_x);
      auto ciphertext_y = cc->Encrypt(kp.publicKey, plaintext_y);

      std::stringstream ss_x, ss_y;
      Serial::Serialize(ciphertext_x, ss_x, SerType::BINARY);
      Serial::Serialize(ciphertext_y, ss_y, SerType::BINARY);

      std::string x_str = ss_x.str();
      std::string y_str = ss_y.str();

      std::vector<uint8_t> x_data(x_str.begin(), x_str.end());
      std::vector<uint8_t> y_data(y_str.begin(), y_str.end());

      RCLCPP_INFO(this->get_logger(), "Serialized X coordinate size: %zu bytes", x_data.size());
      RCLCPP_INFO(this->get_logger(), "Serialized Y coordinate size: %zu bytes", y_data.size());

      // X 좌표 전송
      auto msg_x = enc_turtle_cpp::msg::EncryptedData();
      msg_x.data = x_data;
      msg_x.data_type = 0;
      encrypted_pub_->publish(msg_x);
      RCLCPP_INFO(this->get_logger(), "X coordinate published successfully");

      // Y 좌표 전송
      auto msg_y = enc_turtle_cpp::msg::EncryptedData();
      msg_y.data = y_data;
      msg_y.data_type = 1;
      encrypted_pub_->publish(msg_y);
      RCLCPP_INFO(this->get_logger(), "Y coordinate published successfully");

    } catch (const std::exception& e) {
      RCLCPP_ERROR(this->get_logger(), "Error in encryption: %s", e.what());
    }
  }

  void result_callback(const enc_turtle_cpp::msg::EncryptedData::SharedPtr msg) {
    try {
      RCLCPP_INFO(this->get_logger(), "Received result data, size: %zu bytes", msg->data.size());
      std::string data_str(msg->data.begin(), msg->data.end());
      std::stringstream ss(data_str);
      
      Ciphertext<DCRTPoly> ciphertext;
      Serial::Deserialize(ciphertext, ss, SerType::BINARY);
      RCLCPP_INFO(this->get_logger(), "Result deserialized successfully");
      
      Plaintext plaintext;
      cc->Decrypt(kp.secretKey, ciphertext, &plaintext);
      plaintext->SetLength(1);
      
      double result = static_cast<double>(plaintext->GetPackedValue()[0]) / 1000.0;
      RCLCPP_INFO(this->get_logger(), "Decrypted result: %.3f", result);
    } catch (const std::exception& e) {
      RCLCPP_ERROR(this->get_logger(), "Error in decryption: %s", e.what());
    }
  }

  CryptoContext<DCRTPoly> cc;
  KeyPair<DCRTPoly> kp;

  rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr pose_sub_;
  rclcpp::Subscription<enc_turtle_cpp::msg::EncryptedData>::SharedPtr result_sub_;
  rclcpp::Publisher<enc_turtle_cpp::msg::EncryptedData>::SharedPtr encrypted_pub_;
};

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<EncTurtlePlant>());
  rclcpp::shutdown();
  return 0;
}
