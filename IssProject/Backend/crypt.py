from cryptography.fernet import Fernet
def write_key():                                #creating a key
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():                                 #reading the generated key
    return open("key.key", "rb").read()

data = input()
data = bytes(data,'utf-8')                      #you cannot encrypt str do converting it to bytes
write_key()                                     #creating the key
key = load_key()                                #loading the key
f = Fernet(key)
encrypted = f.encrypt(data)                     #encrypting the data

file = open("encrypted.txt", "wb")               #writing the encrypted the data
file.write(encrypted)
file.close()

with open("encrypted.txt", "rb") as f:           #reading the encrypted the data
    rdata =f.read()

key = load_key()
f = Fernet(key)
decrypted_encrypted = f.decrypt(rdata)
print(decrypted_encrypted)