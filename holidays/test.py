from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_EAX)
data = b'sgfl;akjgl;dsafgja;ldsgkjsd'

ciphertext, tag = cipher.encrypt_and_digest(data)

file_out = open('output.bin', 'wb')
for x in (cipher.nonce, tag, ciphertext):
    file_out.write(x)

file_out.close()


file_in = open('output.bin', 'rb')
nonce, tag, ciphertext = [file_in.read(x) for x in (16, 16, -1)]

cipher = AES.new(key, AES.MODE_EAX, nonce)
data = cipher.decrypt_and_verify(ciphertext, tag)

print(data)
file_in.close()
