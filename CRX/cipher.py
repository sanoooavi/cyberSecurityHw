def rotate_left(x, y, w):
    return ((x << y) & ((1 << w) - 1)) | (x >> (w - y))


def rotate_right(x, y, w):
    return (x >> y) | ((x << (w - y)) & ((1 << w) - 1))


def initial_permutation(A, B):
    return B, A


def final_permutation(A, B):
    return B, A


def simplified_rcx_key_schedule(K, w, r):
    P_w = 0xB7E15163
    Q_w = 0x9E3779B9

    u = w // 8  # u=4
    b = len(K)  # b =16 byte or 128 bit
    c = (b + u - 1) // u  # c= 4
    t = 2 * (r + 1)  # number of sub_keys , t= 26, r=round key

    L = [0] * c  # array of length 4
    for i in range(b - 1, -1, -1):  # i from 15 to 0
        L[i // u] = (L[i // u] << 8) + K[i]
    # L[3]=K[15]K[14]K[13]K[12],  L[2]=K[11]K[10]K[9]K[8],  L[1]=K[7]K[6]K[5]K[4], L[0]=K[3]K[2]K[1]K[0]

    S = [0] * t
    S[0] = P_w
    # 1<<w is 1 with 32 zeroes = 2^32
    for i in range(1, t):
        S[i] = (S[i - 1] + Q_w) % (1 << w)

    for i in range(t):
        S[i] = (S[i] + L[i % c]) % (1 << w)

    return S


def simplified_rcx_encrypt_block(block, S, w, r):
    A, B = initial_permutation(block[0], block[1])
    A = (A + S[0]) % (1 << w)
    B = (B + S[1]) % (1 << w)

    for i in range(1, r + 1):
        A = (A ^ B) + S[2 * i] % (1 << w)
        B = (B ^ A) + S[2 * i + 1] % (1 << w)

    return final_permutation(A, B)


def simplified_rcx_decrypt_block(block, S, w, r):
    A, B = final_permutation(block[0], block[1])

    for i in range(r, 0, -1):
        B = (B - S[2 * i + 1]) ^ A % (1 << w)
        A = (A - S[2 * i]) ^ B % (1 << w)

    A = (A - S[0]) % (1 << w)
    B = (B - S[1]) % (1 << w)

    return initial_permutation(A, B)


def pad_string(s, block_size):
    padding_len = block_size - (len(s) % block_size)
    padding = chr(padding_len) * padding_len
    return s + padding


def unpad_string(s):
    padding_len = ord(s[-1])
    return s[:-padding_len]


def string_to_blocks(s):
    s = pad_string(s, 8)
    byte_array = s.encode('utf-8')
    blocks = []
    for i in range(0, len(byte_array), 8):
        block = byte_array[i:i + 8]
        A = int.from_bytes(block[:4], byteorder='big', signed=False)
        B = int.from_bytes(block[4:], byteorder='big', signed=False)
        blocks.append((A, B))
    return blocks


def blocks_to_string(blocks):
    byte_array = bytearray()
    for A, B in blocks:
        byte_array.extend(A.to_bytes(4, byteorder='big', signed=False))
        byte_array.extend(B.to_bytes(4, byteorder='big', signed=False))
    return unpad_string(byte_array.decode('utf-8'))


def simplified_rcx_encrypt_string(plaintext, S, w, r):
    blocks = string_to_blocks(plaintext)
    encrypted_blocks = [simplified_rcx_encrypt_block(block, S, w, r) for block in blocks]
    return encrypted_blocks


def simplified_rcx_decrypt_string(ciphertext, S, w, r):
    decrypted_blocks = [simplified_rcx_decrypt_block(block, S, w, r) for block in ciphertext]
    return blocks_to_string(decrypted_blocks)


if __name__ == "__main__":
    w = 32
    r = 12
    key = [0x91, 0x5F, 0x46, 0x19, 0xBE, 0x41, 0xB2, 0x51, 0x91, 0x5F, 0x46, 0x19, 0xBE, 0x41, 0xB2, 0x51]
    plaintext = "RCX is here"

    S = simplified_rcx_key_schedule(key, w, r)

    ciphertext = simplified_rcx_encrypt_string(plaintext, S, w, r)
    print(f"Ciphertext: {ciphertext}")

    decrypted = simplified_rcx_decrypt_string(ciphertext, S, w, r)
    print(f"Decrypted: {decrypted}")
