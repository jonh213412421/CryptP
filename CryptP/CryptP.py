import os.path
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from random import randbytes
from random import randint
import sys
import struct

#basic instructions (portuguese)
def h():
    print("Olá! Este programa visa criptografar arquivos de texto de forma segura. Há três funções:"
          "Gerar Chave: -gerar -senha (escolha uma senha)"
          "Encrypt: -encrypt -chave -texto"
          "Decrypt: -decrypt -chave -texto criptografado")
#generates key
def gerar_chave():
    print("GERANDO CHAVE...")
    #generates randint for the key name
    id = randint(1,99)
    #gets senha from sys.args
    senha = sys.argv[2]
    #creates salt
    salt = randbytes(16)
    #creates key
    chave = PBKDF2(salt, senha, dkLen=32)
    #write key in file
    with open(f"chave_{id}.enc", "wb") as f:
        f.write(chave)
    #succes message
    print("Pronto! Armazene a chave em um lugar diferente do arquivo criptografado!")

#encrypt function
def encrypt():
    print("CRIPTOGRAFANDO SENHA...")
    #gets path for key file
    chave_arquivo = sys.argv[2]
    #reads and get key
    with open(chave_arquivo, 'rb') as f:
        chave = f.read()
    id = chave_arquivo.split('_')[1]
    #gets original filename
    id = id.split('.')[0]
    texto_arquivo = sys.argv[3]
    #reads file
    with open(texto_arquivo, 'rb') as f:
        texto = f.read()
    #encrypts braking file in smaller chunks (handy with large files)
    iv = randbytes(16)
    tamanho_arquivo = os.path.getsize(sys.argv[3])
    encryptor = AES.new(chave, AES.MODE_CBC, iv=iv)
    with open (f"arquivo_{id}.enc", 'wb') as f:
        f.write(struct.pack('<Q', tamanho_arquivo))
        f.write(iv)
        if len(texto) % 16 != 0:
            texto += b" " * (16 - len(texto) % 16)
        f.write(encryptor.encrypt(texto))
    print("processo concluido com êxito!")
  
#decrypt function
def decrypt():
    print("DECRIPTOGRAFANDO ARQUIVO...")
    #gets path for key file
    chave_arquivo = sys.argv[2]
    id = chave_arquivo.split('_')[1]
    id = id.split('.')[0]
    #reads and get key
    with open(chave_arquivo, 'rb') as f:
        chave = f.read()
    criptografado_arquivo = sys.argv[3]
    #decrypts file
    with open(criptografado_arquivo, 'rb') as f:
        tamanho_original = struct.unpack('<Q', f.read(struct.calcsize('Q')))[0]
        iv=f.read(16)
        decryptor = AES.new(chave, AES.MODE_CBC, iv=iv)
        with open(f'arquivo_decriptografado_{id}.txt', 'wb') as f2:
            texto = f.read()
            f2.write(decryptor.decrypt(texto))
            f2.truncate(tamanho_original)
    print("processo concluido com êxito!")

if __name__ == '__main__':
    #function switch case
    if sys.argv[1] == '-h':
        h()
    if sys.argv[1] == 'gerar':
        gerar_chave()
    if sys.argv[1] == 'encrypt':
        encrypt()
    if sys.argv[1] == 'decrypt':
        decrypt()
