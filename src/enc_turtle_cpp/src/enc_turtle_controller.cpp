#include "rclcpp/rclcpp.hpp"
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

class EncTurtleController : public rclcpp::Node {
public:
  EncTurtleController() : Node("enc_turtle_controller") {
    CCParams<CryptoContextBGVRNS> parameters;
    parameters.SetPlaintextModulus(65537);
    parameters.SetMultiplicativeDepth(2);
    parameters.SetSecurityLevel(SecurityLevel::HEStd_128_classic);
    parameters.SetRingDim(16384);

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
    
    encrypted_sub_ = this->create_subscription<enc_turtle_cpp::msg::EncryptedData>(
        "encrypted_pose", qos,
        std::bind(&EncTurtleController::enc_pose_callback, this, std::placeholders::_1));

    result_pub_ = this->create_publisher<enc_turtle_cpp::msg::EncryptedData>(
        "encrypted_result", qos);
  }

private:
  void enc_pose_callback(const enc_turtle_cpp::msg::EncryptedData::SharedPtr msg) {
    try {
      RCLCPP_INFO(this->get_logger(), "Received data size: %zu bytes", msg->data.size());
      std::string data_str(msg->data.begin(), msg->data.end());
      std::stringstream ss(data_str);

      if (msg->data_type == 0) {  // X coordinate
        RCLCPP_INFO(this->get_logger(), "Processing X coordinate");
        Serial::Deserialize(ciphertext_x, ss, SerType::BINARY);
        RCLCPP_INFO(this->get_logger(), "X coordinate deserialized successfully");
      } else if (msg->data_type == 1) {  // Y coordinate
        RCLCPP_INFO(this->get_logger(), "Processing Y coordinate");
        Serial::Deserialize(ciphertext_y, ss, SerType::BINARY);
        RCLCPP_INFO(this->get_logger(), "Y coordinate deserialized successfully");
        
        // Y 좌표를 받았으면 계산 수행
        auto ct_result = cc->EvalAdd(ciphertext_x, ciphertext_y);
        RCLCPP_INFO(this->get_logger(), "Addition performed successfully");
        
        std::stringstream ss_result;
        Serial::Serialize(ct_result, ss_result, SerType::BINARY);
        std::string result_str = ss_result.str();
        std::vector<uint8_t> result_data(result_str.begin(), result_str.end());
        RCLCPP_INFO(this->get_logger(), "Result serialized, size: %zu bytes", result_data.size());
        
        auto msg_out = enc_turtle_cpp::msg::EncryptedData();
        msg_out.data = result_data;
        msg_out.data_type = 2;  // Result type
        
        result_pub_->publish(msg_out);
        RCLCPP_INFO(this->get_logger(), "Result published successfully");
      }
    } catch (const std::exception& e) {
      RCLCPP_ERROR(this->get_logger(), "Error in encryption: %s", e.what());
    }
  }

  CryptoContext<DCRTPoly> cc;
  KeyPair<DCRTPoly> kp;
  Ciphertext<DCRTPoly> ciphertext_x;
  Ciphertext<DCRTPoly> ciphertext_y;

  rclcpp::Subscription<enc_turtle_cpp::msg::EncryptedData>::SharedPtr encrypted_sub_;
  rclcpp::Publisher<enc_turtle_cpp::msg::EncryptedData>::SharedPtr result_pub_;
};

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<EncTurtleController>());
  rclcpp::shutdown();
  return 0;
}
