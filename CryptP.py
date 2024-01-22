import os.path
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from random import randbytes
from random import randint
import sys
import struct

def h():
    print("Olá! Este programa visa criptografar arquivos de texto de forma segura. Há três funções:"
          "Gerar Chave: -gerar -senha (escolha uma senha)"
          "Encrypt: -encrypt -chave -texto"
          "Decrypt: -decrypt -chave -texto criptografado")
def gerar_chave():
    print("GERANDO CHAVE...")
    id = randint(1,99)
    senha = sys.argv[2]
    salt = randbytes(16)
    chave = PBKDF2(salt, senha, dkLen=32)
    with open(f"chave_{id}.enc", "wb") as f:
        f.write(chave)
    print("Pronto! Armazene a chave em um lugar diferente do arquivo criptografado!")

def encrypt():
    print("CRIPTOGRAFANDO SENHA...")
    chave_arquivo = sys.argv[2]
    with open(chave_arquivo, 'rb') as f:
        chave = f.read()
    id = chave_arquivo.split('_')[1]
    id = id.split('.')[0]
    texto_arquivo = sys.argv[3]
    with open(texto_arquivo, 'rb') as f:
        texto = f.read()
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

def decrypt():
    print("DECRIPTOGRAFANDO ARQUIVO...")
    chave_arquivo = sys.argv[2]
    id = chave_arquivo.split('_')[1]
    id = id.split('.')[0]
    with open(chave_arquivo, 'rb') as f:
        chave = f.read()
    criptografado_arquivo = sys.argv[3]
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
    if sys.argv[1] == '-h':
        h()
    if sys.argv[1] == 'gerar':
        gerar_chave()
    if sys.argv[1] == 'encrypt':
        encrypt()
    if sys.argv[1] == 'decrypt':
        decrypt()