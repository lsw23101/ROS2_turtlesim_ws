#!/usr/bin/env python3

import openfhe
from openfhe import *
import base64
import sys

def test_bgv():
    print("OpenFHE BGV 스킴 테스트 시작...")
    
    try:
        # BGV 파라미터 설정
        cc = CryptoContext()
        cc.GenerateBGVContext(8192, 65537, 1)
        print("\n1. BGV 컨텍스트 생성 완료")
        
        # 키 생성
        sk = cc.KeyGen()
        print("2. 키 생성 완료")
        
        # 테스트할 값들
        test_values = [0, 1, 2, 3, 4, 5, 10, 20, 30, 40, 50, 100, 500, 1000]
        print("\n3. 암호화/복호화 테스트:")
        
        for value in test_values:
            # 정수를 암호화
            ct = cc.Encrypt(sk, value)
            
            # 복호화
            decrypted = cc.Decrypt(sk, ct)
            
            print(f"  입력: {value}, 출력: {decrypted}")
            
        # 덧셈 테스트
        print("\n4. 덧셈 테스트:")
        value1, value2 = 42, 24
        
        ct1 = cc.Encrypt(sk, value1)
        ct2 = cc.Encrypt(sk, value2)
        
        # 암호화된 상태에서 덧셈
        ct_sum = ct1 + ct2
        
        # 결과 복호화
        result = cc.Decrypt(sk, ct_sum)
        
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
        except Exception as e:
            print(f"  - 직렬화 테스트 중 에러: {str(e)}")
            
    except Exception as e:
        print(f"에러 발생: {str(e)}")
        print(f"에러 타입: {type(e)}")

if __name__ == "__main__":
    test_bgv() 