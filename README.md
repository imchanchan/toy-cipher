**🔐 Kyber Toy Cipher**

진행 기간: 2023.11.20 ~ 2024.02.27

소속: RB 연구실

참여 인원: 최찬, 원희정, 김예진


이 프로젝트는 NIST의 Post-Quantum Cryptography(PQC) 표준 알고리즘인 Kyber를 이해하고 분석하기 위한 목적으로 진행되었습니다.
Kyber는 양자 내성 공개 키 암호화(PKE) 및 키 캡슐화 메커니즘(KEM)으로, 본 프로젝트에서는 Kyber의 구조를 축소된 형태로 구현한 Toy Cipher를 개발하여 알고리즘의 동작 원리를 직관적으로 분석할 수 있도록 하였습니다.



## Parameter

$$
n = 8,\quad q = 3329,\quad k = 2,\quad \eta_1 = 3,\quad \eta_2 = 2,\quad d_u = 10,\quad d_v = 4
$$

주요 개념과 알고리즘의 핵심 원리, 증명 과정 및 Python 기반 코드 예제를 포함하고 있습니다. Toy Cipher 예제를 통해 알고리즘의 전체적인 동작 과정을 쉽게 이해할 수 있도록 구성했습니다.


## 예제 실행 화면

### 1. KeyGen
![KEM KeyGen](images/KEMGen.png)
![PKE KeyGen](images/PKEGen.png)

### 2. Encapsulation & Encryption
![KEM Encapsulation](images/KEMEncaps.png)
![PKE Encryption](images/PKEEncrypt.png)

### 3. Decapsulation & Decryption
![KEM Decapsulation](images/KEMDecaps.png)
![PKE Decryption](images/PKEDecrypt.png)
