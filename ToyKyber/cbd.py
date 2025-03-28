def load32_littleendian(x):
    r = 0
    r |= x[0]
    r |= x[1] << 8
    r |= x[2] << 16
    r |= x[3] << 24
    return r


def load24_littleendian(x):
    r = 0
    r |= x[0]
    r |= x[1] << 8
    r |= x[2] << 16
    return r

a = [0x02, 0x03, 0x04]
print(bin(load24_littleendian(a)))

'''
def kyber_function(buf, r):

    for i in range(256 // 4):
        t = load24_littleendian(buf[3*i:3*(i+1)])
        d = t & 0x00249249
        d += (t >> 1) & 0x00249249
        d += (t >> 2) & 0x00249249

        for j in range(4):
            a = (d >> (6*j+0)) & 0x7
            b = (d >> (6*j+3)) & 0x7




# ========

for i in range(256/8):
    t = load32_littleendian(buf)


buf = [0xe2, 0x76, 0x36, 0x91]
for i in buf:
    print(bin(i), end=" ")

print(bin(load32_littleendian(buf)))

0b11100010 0b01110110 0b00110110 0b10010001
0b11100010 0b01110110 0b00110110 0b10010001

'''