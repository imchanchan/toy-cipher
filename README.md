# 🔐 Kyber Toy Cipher

> NIST PQC 표준 알고리즘인 **Kyber**의 동작 원리를 학습하기 위한 Toy 버전 구현 프로젝트

---

## 진행 기간
2023.11.20 ~ 2024.02.27

## 참여 인원 (3명)
[RB 연구실] 최찬 , 원희정 , 김예진 

---

## 📌 프로젝트 소개

본 프로젝트는 NIST의 PQC (Post-Quantum Cryptography) 표준 알고리즘 중 하나인 **Kyber**의 핵심 개념을 이해하기 위해 수행되었습니다.  
Kyber는 양자 컴퓨팅 환경에서도 안전한 **공개키 암호화(PKE)** 및 **키 캡슐화 메커니즘(KEM)**을 제공하며,  
해당 프로젝트에서는 이를 **간소화된 파라미터를 사용한 Toy Cipher**로 구현하였습니다.

### 🎯 주요 목표
- Kyber 알고리즘의 수학적 구조 및 흐름 분석
- 축소 파라미터 기반의 Toy Cipher 구현
- Python 기반의 예제 코드로 학습 지원

---

## **🔅 Parameter (Toy Version)**


$$
n = 8,\quad q = 3329,\quad k = 2,\quad \eta_1 = 3,\quad \eta_2 = 2,\quad d_u = 10,\quad d_v = 4
$$

주요 개념과 알고리즘의 핵심 원리, 증명 과정 및 Python 기반 코드 예제를 포함하고 있습니다. Toy Cipher 예제를 통해 알고리즘의 전체적인 동작 과정을 쉽게 이해할 수 있도록 구성했습니다.


---
## **🔅예제 실행 화면**

#### 1. KeyGen
![KEM KeyGen](images/KEMGen.png)
![PKE KeyGen](images/PKEGen.png)

#### 2. Encapsulation & Encryption
![KEM Encapsulation](images/KEMEncaps.png)
![PKE Encryption](images/PKEEncrypt.png)

#### 3. Decapsulation & Decryption
![KEM Decapsulation](images/KEMDecaps.png)
![PKE Decryption](images/PKEDecrypt.png)
