#!/usr/bin/env python3

import openfhe
from openfhe import *  # 추가 기능들을 임포트

def main():
    try:
        print("OpenFHE 임포트 성공!")
        
        # 기본 기능 테스트
        cc = BinFHEContext()
        print("컨텍스트 생성 성공!")
        
        # 파라미터 설정
        cc.GenerateBinFHEContext(MEDIUM)
        print("파라미터 설정 성공!")
        
        # 키 생성
        sk = cc.KeyGen()
        print("키 생성 성공!")
        
        # 간단한 암호화/복호화 테스트
        pt = 1  # 평문
        ct = cc.Encrypt(sk, pt)  # 암호화
        result = cc.Decrypt(sk, ct)  # 복호화
        
        print(f"암호화/복호화 테스트: {pt} -> (암호화) -> (복호화) -> {result}")
        print("모든 테스트 성공!")
        
    except Exception as e:
        print("에러 발생:", str(e))
        print("에러 타입:", type(e))

if __name__ == "__main__":
    main() 