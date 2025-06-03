#!/usr/bin/env python3

import openfhe
from openfhe import *
import base64
import sys

def test_bgv():
    print("OpenFHE BGV 스킴 테스트 시작...")
    
    try:
        # BGV 파라미터 설정
        params = CCParams()
        params.SetScheme(SCHEME.BGV)
        params.SetRingDim(1 << 12)
        params.SetPlaintextModulus(65537)
        params.SetScalingModSize(50)
        params.SetBatchSize(8)
        
        # 암호화 컨텍스트 생성
        cc = GenCryptoContext(params)
        cc.Enable(PKESchemeFeature.PKE)
        cc.Enable(PKESchemeFeature.KEYSWITCH)
        cc.Enable(PKESchemeFeature.LEVELEDSHE)
        print("\n1. BGV 컨텍스트 생성 완료")
        
        # 키 생성
        keys = cc.KeyGen()
        print("2. 키 생성 완료")
        
        # 테스트할 값들
        test_values = [0, 1, 2, 3, 4, 5, 10, 20, 30, 40, 50, 100, 500, 1000]
        print("\n3. 암호화/복호화 테스트:")
        
        for value in test_values:
            # 정수를 암호화
            plaintext = cc.MakePackedPlaintext([value])
            ciphertext = cc.Encrypt(keys.publicKey, plaintext)
            
            # 복호화
            decrypted_text = cc.Decrypt(keys.secretKey, ciphertext)
            decrypted_value = decrypted_text.GetPackedValue()[0]
            
            print(f"  입력: {value}, 출력: {decrypted_value}")
            
        # 덧셈 테스트
        print("\n4. 덧셈 테스트:")
        value1, value2 = 42, 24
        
        pt1 = cc.MakePackedPlaintext([value1])
        pt2 = cc.MakePackedPlaintext([value2])
        
        ct1 = cc.Encrypt(keys.publicKey, pt1)
        ct2 = cc.Encrypt(keys.publicKey, pt2)
        
        # 암호화된 상태에서 덧셈
        ct_sum = cc.EvalAdd(ct1, ct2)
        
        # 결과 복호화
        decrypted_sum = cc.Decrypt(keys.secretKey, ct_sum)
        result = decrypted_sum.GetPackedValue()[0]
        
        print(f"  {value1} + {value2} = {result}")
        
        # 직렬화 테스트
        print("\n5. 직렬화 테스트:")
        try:
            print("  - 사용 가능한 메서드:", dir(ct1))
            print("  - 타입:", type(ct1))
            if hasattr(ct1, 'SerializeToString'):
                print("  - SerializeToString 메서드 있음")
            if hasattr(ct1, 'Serialize'):
                print("  - Serialize 메서드 있음")
            if hasattr(ct1, 'save'):
                print("  - save 메서드 있음")
            if hasattr(ct1, 'SaveToFile'):
                print("  - SaveToFile 메서드 있음")
        except Exception as e:
            print(f"  - 직렬화 테스트 중 에러: {str(e)}")
            
    except Exception as e:
        print(f"에러 발생: {str(e)}")
        print(f"에러 타입: {type(e)}")

if __name__ == "__main__":
    test_bgv() 