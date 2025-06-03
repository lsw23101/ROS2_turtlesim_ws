#include <iostream>
#include <openfhe/pke/openfhe.h>

using namespace lbcrypto;

int main() {
    // 1. BGV 파라미터 설정
    CCParams<CryptoContextBGVRNS> parameters;
    parameters.SetPlaintextModulus(65537);
    parameters.SetMultiplicativeDepth(2);
    parameters.SetSecurityLevel(SecurityLevel::HEStd_128_classic);
    parameters.SetRingDim(16384);  // 권장되는 최소 Ring dimension으로 변경

    std::cout << "BGV 파라미터 설정 완료" << std::endl;

    // 2. 암호화 컨텍스트 생성
    CryptoContext<DCRTPoly> cc = GenCryptoContext(parameters);
    cc->Enable(PKE);
    cc->Enable(KEYSWITCH);
    cc->Enable(LEVELEDSHE);

    std::cout << "암호화 컨텍스트 생성 완료" << std::endl;

    // 3. 키 생성
    KeyPair<DCRTPoly> keyPair = cc->KeyGen();
    if (!keyPair.secretKey) {
        std::cout << "키 생성 실패" << std::endl;
        return 1;
    }

    std::cout << "키 생성 완료" << std::endl;

    // 4. 테스트 값
    std::vector<int64_t> vectorOfInts1 = {5};
    std::vector<int64_t> vectorOfInts2 = {3};

    // 5. 평문 인코딩
    Plaintext plaintext1 = cc->MakePackedPlaintext(vectorOfInts1);
    Plaintext plaintext2 = cc->MakePackedPlaintext(vectorOfInts2);

    std::cout << "평문1: " << plaintext1 << std::endl;
    std::cout << "평문2: " << plaintext2 << std::endl;

    // 6. 암호화
    auto ciphertext1 = cc->Encrypt(keyPair.publicKey, plaintext1);
    auto ciphertext2 = cc->Encrypt(keyPair.publicKey, plaintext2);

    std::cout << "암호화 완료" << std::endl;

    // 7. 암호화된 상태에서의 덧셈
    auto ciphertextAdd = cc->EvalAdd(ciphertext1, ciphertext2);

    std::cout << "암호화된 덧셈 완료" << std::endl;

    // 8. 복호화
    Plaintext plaintextAdd;
    cc->Decrypt(keyPair.secretKey, ciphertextAdd, &plaintextAdd);

    plaintextAdd->SetLength(1);
    std::cout << "복호화된 결과: " << plaintextAdd << std::endl;

    return 0;
}