import socket
import threading

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


PORT = 2003
CLE_PRIVEE_PATH = "././keys/06_private.pem"

def charger_cle_privee(path):
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def dechiffrer_hybride(paquet: bytes, cle_privee_rsa):
    encrypted_key = paquet[:256]
    iv = paquet[256:272]
    ciphertext = paquet[272:]

    aes_key = cle_privee_rsa.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_msg = decryptor.update(ciphertext) + decryptor.finalize()

    pad_len = padded_msg[-1]
    return padded_msg[:-pad_len]

def handle_client(client_conn, client_addr, cle_privee):
    print(f"[Relai] Connexion de {client_addr}")
    try:
        data = client_conn.recv(4096)
        decrypted_data = dechiffrer_hybride(data, cle_privee)

        split_index = decrypted_data.find(b"),")
        if split_index == -1:
            raise ValueError("Format invalide")

        target_str = decrypted_data[:split_index + 1].decode()
        client_msg = decrypted_data[split_index + 2:]

        target_tuple = eval(target_str)
        target_ip, target_port = target_tuple

        print(f"[Relai] Transfert vers {target_ip}:{target_port}")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((target_ip, target_port))
            s.send(client_msg)
            response = s.recv(4096)

        client_conn.send(response)

    except Exception as e:
        print(f"[Relai] Erreur : {e}")
        client_conn.send(b"[Erreur relais]")

    finally:
        client_conn.close()

def start_relay():
    cle_privee = charger_cle_privee(CLE_PRIVEE_PATH)

    relay_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    relay_socket.bind(('127.0.0.1', PORT))
    relay_socket.listen()
    print(f"[Relai] En écoute sur le port {PORT}...")

    while True:
        client_conn, client_addr = relay_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_conn, client_addr, cle_privee))
        thread.start()

if __name__ == "__main__":
    start_relay()
