#!/usr/bin/env python3

import openfhe
from openfhe import *
import base64
import pickle
import sys
import json

def test_serialization():
    print("OpenFHE 직렬화/역직렬화 테스트 시작...")
    
    # FHE 컨텍스트 설정
    cc = BinFHEContext()
    cc.GenerateBinFHEContext(MEDIUM)
    sk = cc.KeyGen()
    
    # 테스트할 값
    original_value = 42
    print(f"\n1. 원본 값: {original_value}")
    
    # 암호화
    ct = cc.Encrypt(sk, original_value)
    print("\n2. 암호화 완료")
    
    print("\n3. GetLength와 GetModulus 메서드 테스트:")
    try:
        length = ct.GetLength()
        modulus = ct.GetModulus()
        print(f"  - Length: {length}")
        print(f"  - Modulus: {modulus}")
    except Exception as e:
        print(f"  - 메서드 호출 실패: {str(e)}")
    
    print("\n4. 객체 내부 구조 확인:")
    try:
        print("  - dir(ct):", dir(ct))
        print("  - ct.__dict__:", ct.__dict__ if hasattr(ct, '__dict__') else "No __dict__ attribute")
        print("  - ct.__slots__:", ct.__slots__ if hasattr(ct, '__slots__') else "No __slots__ attribute")
    except Exception as e:
        print(f"  - 내부 구조 확인 실패: {str(e)}")
    
    print("\n5. pybind11 conduit 테스트:")
    try:
        conduit = getattr(ct, '_pybind11_conduit_v1_', None)
        print(f"  - Conduit available: {conduit is not None}")
        if conduit:
            print(f"  - Conduit type: {type(conduit)}")
            print(f"  - Conduit dir: {dir(conduit)}")
    except Exception as e:
        print(f"  - Conduit 접근 실패: {str(e)}")
    
    # 복호화 테스트 (원본 ct)
    try:
        print("\n6. 원본 암호문 복호화 테스트:")
        decrypted = cc.Decrypt(sk, ct)
        print(f"  - 복호화된 값: {decrypted}")
        print(f"  - 원본과 일치: {original_value == decrypted}")
        
        # 여러 값 테스트
        print("\n7. 여러 값 암호화/복호화 테스트:")
        for test_value in [0, 1, 2, 3, 4, 5, 10, 20, 30, 40, 50]:
            test_ct = cc.Encrypt(sk, test_value)
            test_decrypted = cc.Decrypt(sk, test_ct)
            print(f"  - 입력: {test_value}, 출력: {test_decrypted}")
    except Exception as e:
        print(f"  - 복호화 실패: {str(e)}")

if __name__ == "__main__":
    test_serialization() 