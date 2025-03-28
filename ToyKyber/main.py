import kyber

print("\n=========================[ Parameter Set ]=========================")
print("| n = 8, q = 3329, k = 2, eta_1 = 3, eta_2 = 2, d_u = 10, d_v = 4 |")
print("===================================================================\n\n")


# ====== ====== ====== ====== ====== ====== ====== ====== ====== 
# ====== ML-KEM.KeyGen ====== ====== ====== ====== ====== ====== 
# ====== ====== ====== ====== ====== ====== ====== ====== ======
# 1: z <- B^32
# 2: (ek_PKE, dk_PKE) <- K-PKE.KeyGen()
# 3: ek <- ek_PKE
# 4: dk <- (dk_PKE||ek||H(ek)||z)
# 5: return (ek, dk)
# ====== ====== ====== ====== ====== ====== ====== ====== ======

# 1: z 배열 생성
z = kyber.randarray(32)
# print("z = ", z)
# 2: (ek_PKE, dk_PKE) <- K-PKE.KeyGen()

# ====== ====== ====== ====== ====== ====== ====== ====== ====== 
# ======  K-PKE.KeyGen ====== ====== ====== ====== ====== ====== 
# ====== ====== ====== ====== ====== ====== ====== ====== ======

# 1. rho, sigma 선언
rho   =  [ 165, 123, 204, 21, 165, 131, 156, 186, 60, 34, 142, 120, 56, 137, 207, 222, 175, 154, 249, 113, 7, 72, 182, 113, 90, 139, 87, 165, 231, 205, 241, 90,  ]
sigma =  [ 18, 195, 233, 231, 186, 75, 24, 95, 187, 204, 60, 162, 220, 198, 97, 229, 11, 226, 62, 13, 171, 32, 144, 116, 220, 66, 188, 44, 115, 152, 58, 109,  ]

# 2. A_mat 선언 (XOF)
A_mat = [[[1362, 2963, 2046, 1451, 1165, 352, 2213, 2297], [2341, 2617, 2962, 1434, 227, 3061, 2742, 1408]], [[3030, 2891, 2275, 59, 2234, 474, 1260, 3203], [464, 555, 2459, 677, 369, 2816, 911, 900]]]

# 3-1. s, e 추출 (CBD)
s = [[-1,  0,  1,  2,  1, -1, -1, -1], [-1,  1,  1, -2, -3, -2,  0,  2]]
e = [[ 1,  0,  0,  0,  0,  0, -2,  0], [ 0,  0, -1,  1,  1,  0,  2,  3]]

# 3-2. s_hat, e_hat 출력 : NTT(s,e)
s_hat = [[0] for _ in range(2)]
e_hat = [[0] for _ in range(2)]

for k in range(2):
    s_hat[k] = kyber.NTT(s[k])
    e_hat[k] = kyber.NTT(e[k])
       
# print("s_hat = ",s_hat)
# print("e_hat = ",e_hat)

# 4. t_hat 생성하기
# 4-1. A_hat * s_hat = t 생성
t = [[0]*8 for _ in range(2)]
for i in range(2):
    temp1 = kyber.MultiplyNTTs( A_mat[i][0], s_hat[0] )
    temp2 = kyber.MultiplyNTTs( A_mat[i][1], s_hat[1] )
    t[i] = kyber.AddPoly(temp1, temp2)

# print("t = ", t)

# 4-2. t_hat = A_hat * s_hat + e_hat
t_hat = [[0]*8 for _ in range(2)]
for i in range(2):
    t_hat[i] = kyber.AddPoly(t[i], e_hat[i])
# print("t_hat = ", t_hat)

# 5. ek_PKE <- ByteEncode_12(t_hat) || rho 생성하기
t_hat_encoded = []
kyber.polyvec_tobytes(t_hat_encoded, t_hat)

ek_PKE = t_hat_encoded + rho

# 6. dk_PKE <- ByteEncode_12(s_hat) 생성하기
s_hat_encoded = []
kyber.polyvec_tobytes(s_hat_encoded, s_hat)
dk_PKE = s_hat_encoded

# print("ek_PKE = ", ek_PKE)
# print("dk_PKE = ", dk_PKE)

# ====== ====== (K-PKE.KeyGen() Finish)  ====== ====== ====== ======

# 3: ek <- ek_PKE
ek = ek_PKE

# 4: dk <- (dk_PKE||ek||H(ek)||z)
hashed_ek = kyber.sha3_256(ek_PKE)
dk_PKE_temp = [0]*len(dk_PKE)
for i in range(len(dk_PKE)):
    dk_PKE_temp[i] = dk_PKE[i]
dk = dk_PKE + ek + hashed_ek + z

print("ek =", end="")
kyber.printarray(ek)
print("dk =", end="")
kyber.printarray(dk)
print("===== ML-KEM KeyGen Done =====\n")
# 5: return (ek, dk)

# ====== ====== (ML-KEM.KeyGen() Finish)  ====== ====== ====== ======

# ====== ====== ====== ====== ====== ====== ====== ====== ====== 
# ====== ML-KEM.Encaps(ek) == ====== ====== ====== ====== ====== 
# ====== ====== ====== ====== ====== ====== ====== ====== ======
# 1: m <- B^1
# 2: (K, r) <- G(m||H(ek))
# 3: c <- K-PKE.Encrypt(ek, m, r)
# 4: return (K, c)
# ====== ====== ====== ====== ====== ====== ====== ====== ======

# 1: m <- B^1
m = [170]

# 2: (K, r) <- G(m||H(ek))
KEM_temp = kyber.sha3_512((m+hashed_ek))

K = KEM_temp[:32]
r = KEM_temp[32:]

# print(KEM_temp)
# print("K = ", K)
# print("r = ", r)

# 3: c <- K-PKE.Encrypt(ek, m, r)

# ====== ====== ====== ====== ====== ====== ====== ====== ====== 
# ====== K-PKE.Encrypt ====== ====== ====== ====== ====== ====== 
# ====== ====== ====== ====== ====== ====== ====== ====== ======
def K_PKE_Encrypt(ek_PKE, m, r):
    # 1. t_hat_decoded, rho 생성
    t_hat_decoded =[[0]*8 for _ in range(2)]
    kyber.polyvec_frombytes(t_hat_decoded, ek_PKE[:24])
    rho = ek_PKE    [24:]
    # print("t_hat_decoded = ", t_hat_decoded)
    # print("rho = ", rho)

    A_mat_Encrypt = [[[1362, 2963, 2046, 1451, 1165, 352, 2213, 2297], [2341, 2617, 2962, 1434, 227, 3061, 2742, 1408]], [[3030, 2891, 2275, 59, 2234, 474, 1260, 3203],   [464, 555, 2459, 677, 369, 2816, 911, 900]]]

    # 2. r을 통해 추출한 r_vec, e1_vec, e2
    r_vec  = [[-1,  0,  3, -1,  0, -1,  1, -1, ],[-1,  0,  0,  0, -1,  0, -1,  1, ]]
    e1_vec = [[ 0,  2, -2, -1, -1,  0,  3,  1, ],[-3,  1, -1,  0,  0,  1,  1, -1, ]]
    e2     = [ 1,  0,  1,  0,  0, -1,  1,  0, ]

    # 3. r_hat 생성하기
    r_hat = [[0]*8 for _ in range(2)]
    for i in range(2):
        r_hat[i] = kyber.NTT(r_vec[i])
    # print("r_hat = ", r_hat)

    # 4. u_vec 생성하기
    # 4-1. A_mat_T * r_hat
    A_mat_T = [[0]*2 for _ in range(2)]
    for i in range(2):
        for j in range(2):
            A_mat_T[i][j] = A_mat_Encrypt[j][i]

    u_vec_temp = [[0]*8 for _ in range(2)]
    for i in range(2):
        temp1 = kyber.MultiplyNTTs( A_mat_T[i][0], r_hat[0] )
        temp2 = kyber.MultiplyNTTs( A_mat_T[i][1], r_hat[1] )
        u_vec_temp[i] = kyber.AddPoly(temp1, temp2)

    # print("u_vec_temp = ", u_vec_temp)

    # 5.2 NTT inverse
    for k in range(2):
        u_vec_temp[k] = kyber.inv_NTT(u_vec_temp[k])
    # print("NTT^(-1)(u_vec_temp) = ", u_vec_temp)

    # 5.3 u_vec = NTT(-1)(A_mat_T * r_hat) + e1_vec
    u_vec = [[0]*8 for _ in range(2)]
    for i in range(2):
        u_vec[i] = kyber.AddPoly(u_vec_temp[i], e1_vec[i])
        
    # print("u_vec = ", u_vec)

    # 5. mu 생성하기
    mu = kyber.poly_frommsg(m[0])
    # print("mu = ", mu)

    # 6. v 생성하기
    # 6-1. v_temp = t_T_hat * r_hat
    v_temp = [0]*8
    temp1 = kyber.MultiplyNTTs( t_hat[0], r_hat[0] )
    temp2 = kyber.MultiplyNTTs( t_hat[1], r_hat[1] )
    v_temp = kyber.AddPoly(temp1, temp2)

    # print("t_T_hat * r_hat = ", v_temp)

    # 6-2. NTT^(-1) (t_T_hat * r_hat)
    v_temp = kyber.inv_NTT(v_temp)
    # print("inv_NTT(t_T_hat * r_hat) = ", v_temp)

    # 6-3. NTT^(-1) (t_T_hat * r_hat) + e2_vec + mu
    v=[]
    for i in range(8):
        v.append((v_temp[i]+e2[i]+mu[i]) % kyber.q)
    # print("v = ", v)

    # 7. c1, c2 생성하기
    # 7-1. c1, c2 compress하기
    c1 = []
    c2 = []
    for i in range(2):
        for j in range(8):
            c1.append(kyber.compress(u_vec[i][j], 10))
    for j in range(8):
        c2.append(kyber.compress(v[j], 4))
        
    # print("c1 = ", c1)
    # print("c2 = ", c2)

    # 7-2. c1, c2 ByteEncode하기
    c1 = kyber.ByteEncode_du_vec(c1)
    c2 = kyber.ByteEncode_dv(c2)

    # print("Encode_c1 = ", c1)
    # print("Encode_c2 = ", c2)

    # 8. c <- (c1 || c2)
    c = c1 + c2
    return c
    # ====== ====== (K-PKE.Encrypt() Finish)  ====== ====== ====== ======

c = K_PKE_Encrypt(ek_PKE, m, r)

# 4: return (K, c)
print("K =", end="")
kyber.printarray(K)
print("c =", end="")
kyber.printarray(c)
print("===== ML-KEM Encaps Done =====")
# ====== ====== (ML-KEM.Encaps() Finish)  ====== ====== ====== ======


# ====== ====== ====== ====== ====== ====== ====== ====== ====== 
# ====== ML-KEM.Decpas(c, dk) ====== ====== ====== ====== ====== 
# ====== ====== ====== ====== ====== ====== ====== ====== ======
# 1: dk_PKE = dk[0:24]
# 2: ek_PKE = dk[24:24+56] = dk[24:80]
# 3: h <- dk[80:80+32] = dk[80:112]
# 4: z <- dk[112:112+32] = dk[112:144]
# 5: m' <- K-PKE.Decrypt(dk_PKE, c)
# 6: (K', r') <- G(m'||h)
# 7: K_bar <- J(z||c, 32)
# 8: c' <- K-PKE.Encrypt(ek_PKE, m', r')
# 9: if c != c' then
# 10:    K' <- K_bar
# 11: end if
# 12: return K'
# ====== ====== ====== ====== ====== ====== ====== ====== ======

# 1: dk_PKE = dk[0:24]
dk_PKE_decaps = dk[:24]

# 2: ek_PKE = dk[24:24+56] = dk[24:80]
ek_PKE_decaps = dk[24:80]

# 3: h <- dk[80:80+32] = dk[80:112]
h_decaps = dk[80:112]

# 4: z <- dk[112:112+32] = dk[112:144]
z_decaps = dk[112:144]

# print("dk_PKE_decaps = ", dk_PKE_decaps)
# print("ek_PKE_decaps = ", ek_PKE_decaps)
# print("h = ", h_decaps)
# print("z_decaps = ", z_decaps)


# 5: m' <- K-PKE.Decrypt(dk_PKE, c)

# ====== ====== ====== ====== ====== ====== ====== ====== ====== 
# ====== K-PKE.Decrypt(dk_PKE, c) == ====== ====== ====== ====== 
# ====== ====== ====== ====== ====== ====== ====== ====== ======
def K_PKE_Decrypt(dk_PKE, c):
    # 1. c1 <- c[0:20]
    c1_decrypt = c[:20]

    # 2. c2 <- c[20:]
    c2_decrypt = c[20:]

    # 3. u <- Decompress_du(ByteDecode_du(c1))
    u_vec_decode = kyber.ByteDecode_du_vec(c1_decrypt)
    u_vec_decrypt = [[0]*8 for _ in range(2)]
    for i in range(2):
        for j in range(8):
            u_vec_decrypt[i][j] = (kyber.decompress(u_vec_decode[8*i+j],10))
    # print("u_vec_decrypt = ", u_vec_decrypt)

    # 4. v <- Decompress_dv(ByteDecode_dv(c2))
    v_decode = kyber.ByteDecode_dv(c2_decrypt)
    v_decrypt = [0]*8
    for j in range(8):
        v_decrypt[j] = (kyber.decompress(v_decode[j],4))
    # print("v_decrypt = ", v_decrypt)

    # 5. s_hat <- ByteDecode_12(dk_PKE)
    s_hat_decrypt = [[0]*8 for _ in range(2)]
    kyber.polyvec_frombytes(s_hat_decrypt, dk_PKE_temp)
    # print("s_hat_decrypt = ", s_hat_decrypt)

    # 6. w <- v - NTT^(-1)(s_hat_T * NTT(u))
    # 6-1. u_ntt = NTT(u) 구하기
    u_ntt = [[0]*8 for _ in range(2)]
    for i in range(2):
        u_ntt[i] = kyber.NTT(u_vec_decrypt[i])
    # print("u_ntt = ", u_ntt)

    # 6-2. s_hat_T * NTT(u) 구하기
    w_temp = [0]*8
    w_temp1 = kyber.MultiplyNTTs( s_hat_decrypt[0] , u_ntt[0] )
    w_temp2 = kyber.MultiplyNTTs( s_hat_decrypt[1] , u_ntt[1] )
    w_temp = kyber.AddPoly(w_temp1, w_temp2)

    # 6-3. w <- v - NTT^(-1) (s_hat_T * NTT(u))
    w = kyber.inv_NTT(w_temp)
    w = kyber.SubPoly(v_decrypt, w)
    # print("w = ", w)

    # 7. m <- ByteEncode_1(Compress_1(w))
    m_decrypt = [0]
    m_decrypt[0] = kyber.poly_tomsg(w)
    # print("m_decrypt = ", m_decrypt)
    
    return m_decrypt
# ====== ====== (K-PKE.Decrypt() Finish)  ====== ====== ====== ======

m_decrypt = K_PKE_Decrypt(dk_PKE, c)

# 6: (K', r') <- G(m'||h)
Decaps_pair = kyber.sha3_512(m_decrypt+h_decaps)
K_prime = Decaps_pair[:32]
r_prime = Decaps_pair[32:]

# 7: K_bar <- J(z||c, 32)
K_bar = kyber.sha3_256(z_decaps+c)
# print("K_bar = ", K_bar)

# 8: c' <- K-PKE.Encrypt(ek_PKE, m', r')
c_prime = K_PKE_Encrypt(ek_PKE, m_decrypt, r_prime)

# 9: if c != c' then
# 10:    K' <- K_bar
# 11: end if
if c != c_prime:
    K_prime = K_bar
    
# 12: return K'"
print("\nK' =", end="")
kyber.printarray(K_prime)
print("===== ML-KEM Decaps Done =====\n")
# ====== ====== (ML-KEM.Decaps() Finish)  ====== ====== ====== ======
print("\n===================================")
print("| m         = 0x%02x" %(m[0]), end="                |\n")
print("| m_decrypt = 0x%02x" %(m_decrypt[0]), end="                |\n")

if m[0] != m_decrypt[0]:
    print("| Decryption Failure !!", end="           |\n")
else:
    print("| Decryption Success !!", end="           |\n")
print("===================================\n")

print("\n===============================================================================================================================================================================================================")
print("| K     =", end="")
kyber.printarray(K)
print("| K'    =", end="")
kyber.printarray(K_prime)
print("| K_bar =", end="")
kyber.printarray(K_bar)

if K != K_prime:
    print("| Decapsulation Failure !!")
else:
    print("| Decapsulation Success !!")
print("===============================================================================================================================================================================================================\n")

# K_prime != K_bar -> Decapsulation Success