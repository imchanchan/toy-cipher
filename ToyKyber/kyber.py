''' [ unity 거듭제곱해서 mod q 취한 값 ]
    |  40^1 = 40
    |  40^2 = 1600
    |  40^3 = 749
    |  40^4 = 3328
    |  40^5 = 3289
    |  40^6 = 1729
    |  40^7 = 2580
    |  40^8 = 1
'''

q = 3329

#===============================
#== [함수 : NTT] ================
#===============================
ntt_zeta = [3328, 1600, 1729]

def NTT(f):
    f_hat = [0]*8
    for i in range(8):
        f_hat[i] = f[i]
        
    k = 0
    for len in range(4, 0, -2):
        for start in range(0, 8, 2*len):
            for j in range(start, start+len):
                t = (ntt_zeta[k] * f_hat[j+len]) % q
                f_hat[j+len] = (f_hat[j]-t) % q
                f_hat[j] = (f_hat[j]+t) % q
            k += 1
    return f_hat

#===============================
#== [함수 : InvNTT] =============
#===============================
zeta_inv = [1729, 1600, 3328]

def inv_NTT(f):
    f_hat = [0]*8
    for i in range(8):
        f_hat[i] = f[i]
        
    k = 0
    for len in range(2, 5, 2):
        for start in range(0, 8, 2*len):
            for j in range(start, start+len):
                t = f_hat[j]
                f_hat[j] = (t + f_hat[j+len]) % q
                f_hat[j+len] = (zeta_inv[k] * (t-f_hat[j+len])) % q
            k += 1
                        
    for t in range(8):
        f_hat[t] = (f_hat[t]*2497) % q    # 2497 = 4^(-1) mod q
    return f_hat

#===============================
#== [함수 : MultiplyNTTs] =======
#===============================
mul_zeta = [40, 40, 3289, 3289]

def MultiplyNTTs(f, g):
    h = [0]*8
    for i in range(4):
        h[2*i], h[2*i+1] = (BaseCaseMultiply(f[2*i], f[2*i+1], g[2*i], g[2*i+1], mul_zeta[i]))
    return h

#===============================  
#== [함수 : BaseCaseMultiply] ===
#===============================  
def BaseCaseMultiply(a0, a1, b0, b1, gamma):
    c0 = (a0*b0 + a1*b1*gamma) % q
    c1 = (a0*b1 + a1*b0) % q
    return c0, c1

#===============================
#== [함수 : AddPoly] ============
#===============================
def AddPoly(f, g):
    h = [0]*8
    for i in range(8):
        h[i] = (f[i] + g[i]) % q
    return h

#===============================
#== [함수 : SubPoly] ============
#===============================
def SubPoly(f, g):
    h = [0]*8
    for i in range(8):
        h[i] = (f[i] - g[i]) % q
    return h

#=======================================
#== [함수 : ByteEncode12 = poly_tobytes]
#=======================================
def poly_tobytes(r, a):
    for i in range(4):
        t0 = a[2*i]
        t1 = a[2*i+1]
        r.append ( ( t0 >> 0) & 0xFF)
        r.append ( ((t0 >> 8) & 0xFF) | ((t1 << 4) & 0xF0) )
        r.append ( ( t1 >> 4) & 0xFF)
    return r

def polyvec_tobytes(r, a):
    for i in range(2):
        poly_tobytes(r, a[i])
    return r

#========================================
#== [함수 : ByteDecode12 = poly_frombytes]
#========================================
def poly_frombytes(r, a):
    for i in range(4):
        r[2*i]   = ((a[3*i+0] >> 0) | (a[3*i+1] << 8)) & 0xFFF
        r[2*i+1] = ((a[3*i+1] >> 4) | (a[3*i+2] << 4)) & 0xFFF

def polyvec_frombytes(r, a):
    poly_frombytes(r[0], a[:12])
    poly_frombytes(r[1], a[12:])
    return r

#========================================
#== [함수 : poly_frommsg(B)] =============
# Decompress_1(ByteDecode_1(B))을 수행
# input  : 1byte B
# return : 8차 다항식
#========================================
def poly_frommsg(B):
    res =[]
    for i in range(1):
        for j in range(8):
            if (B>>j)&1 == 1 :
                res.append(1665)    # 1665=kyber_Q+1/2
            else:
                res.append(0)
    return res

#========================================
#== [함수 : poly_tomsg(B)] ===============
# ByteEncdoe_1(Compress_1(B))을 수행
# input  : 8차 다항식
# return : 1바이트 res
#========================================
def poly_tomsg(B):
    res = 0
    for i in range(8):
        res |= (int(round((2/3329)*B[i])) & 1) << i
    return res

#========================================
#== [함수 : compress] ====================
# input  : 12비트 정수 입력, d
# return : d비트 정수 출력
#========================================
def compress(x,d):
    y= int(round((2**d/3329)*x)) %2**d
    return y

#========================================
#== [함수 : decompress] ==================
#========================================
def decompress(x,d):
    y= int(round(3329/(2**d)*x)) % 3329
    return y


#========================================
#== [함수 : ByteEncode_du_vec] - du=10 ===
# input  : 계수의 범위가 Z_du인 8차 다항식
# retrun : 길이가 du인 바이트 배열
#========================================
def ByteEncode_du_vec(B):
    enc = [0 for _ in range(20)]
    for i in range(4):
        enc[5*i+0] = ( B[4*i+0] >> 0) & 0xff
        enc[5*i+1] = ((B[4*i+0] >> 8) | (B[4*i+1] << 2)) & 0xff
        enc[5*i+2] = ((B[4*i+1] >> 6) | (B[4*i+2] << 4)) & 0xff
        enc[5*i+3] = ((B[4*i+2] >> 4) | (B[4*i+3] << 6)) & 0xff
        enc[5*i+4] = ( B[4*i+3] >> 2) & 0xff
    return enc

#========================================
#== [함수 : ByteEncode_dv ] ==============
#========================================
def ByteEncode_dv(B):
    enc = [0 for _ in range(4)]
    for i in range(4):
        enc[i] = (B[2*i] | (B[2*i+1] << 4)) & 0xff

    return enc

#========================================
#== [함수 : ByteDecode_du_vec ] ==========
#========================================
def ByteDecode_du_vec(B):
    dec = [0 for _ in range(16)]
    for i in range(4):
        dec[4*i+0] = ((B[5*i+0] >> 0) | (B[5*i+1] << 8)) & 0x3ff # aaaa aaaa | bbbb bbbb 0000 0000 -> bb aaaa aaaa
        dec[4*i+1] = ((B[5*i+1] >> 2) | (B[5*i+2] << 6)) & 0x3ff # 00bb bbbb | 00cc cccc cc00 0000 -> cc ccbb bbbb
        dec[4*i+2] = ((B[5*i+2] >> 4) | (B[5*i+3] << 4)) & 0x3ff # 0000 cccc | dddd dddd 0000      -> dd dddd cccc
        dec[4*i+3] = ((B[5*i+3] >> 6) | (B[5*i+4] << 2)) & 0x3ff # 0000 00dd | 00ee eeee ee00      -> ee eeee eedd
    return dec

#========================================
#== [함수 : ByteDecode_dv ] ==============
#========================================
def ByteDecode_dv(B):
    dec = [0 for _ in range(8)]
    for i in range(4):
        dec[2*i]   = B[i] & 0xf
        dec[2*i+1] = (B[i] >> 4) & 0xf 
        # B[0] = bbbb aaaa -> dec[0] = aaaa, dec[1] = bbbb
    return dec

##############[[         해시함수         ]]##############

from Crypto.Hash import SHA3_256
from Crypto.Hash import SHA3_512

#=========================================
#== [함수 : sha3_256] ====================
# in_data : 1차원 배열 형태의 sha3_256 입력 배열
# return  : hash된 32바이트 list
#=========================================
def sha3_256(in_data):
    hash_object = SHA3_256.new()
    hash_object.update(bytes(in_data))
    hashed_data = hash_object.digest()
    return list(bytearray(hashed_data))

#=========================================
#== [함수 : sha3_512] =====================
# in_data : 1차원 배열 형태의 sha3_512 입력 배열
# return  : hash된 64바이트 list
#=========================================
def sha3_512(in_data):
    hash_object = SHA3_512.new()
    hash_object.update(bytes(in_data))
    hashed_data = hash_object.digest()
    return list(bytearray(hashed_data))

#######################################################

import random
#=========================================
#== [함수 : randarray(int)] ===============
# return  : random한 int 바이트 길이의 list
#=========================================
def randarray(int):
    array = []
    for _ in range(int):
        array.append( random.randint(0, 255))
    return array

#######################################################

#=========================================
#== [함수 : printarray(array)] ============
#=========================================
def printarray(array):
    print("  [ ", end="")
    for i in range(len(array)):
        print("0x%02x, " %(array[i]), end="")
    print("]")

#=========================================
#== [함수 : printvecotr(vector)] ============
#=========================================   
def printvector(vector):
    print("  [ ", end="")
    for i in range(len(vector)):
        print("[", end="")
        for j in range(len(vector[0])):
            print("0x%02x, " %(vector[i][j]), end="")
        print("] ", end="")
    print("]")