import socket
import csv
import secrets
import base64
import os

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def charger_relais_par_ordre(fichier_csv):
    relais_par_ordre = {}

    with open(fichier_csv, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            try:
                ordre = int(row[0])
                nom = row[1].strip()
                ip = row[2].strip()
                port = int(row[3])
                cle_pub_b64 = row[4].strip()

                if ordre not in relais_par_ordre:
                    relais_par_ordre[ordre] = []

                relais_par_ordre[ordre].append((nom, ip, port, cle_pub_b64))
            except (IndexError, ValueError):
                continue

    return relais_par_ordre

def charger_cle_publique_base64(b64_string):
    key_bytes = base64.b64decode(b64_string)
    return serialization.load_pem_public_key(key_bytes)

def chiffrer_hybride(message: bytes, cle_publique_rsa):
    aes_key = os.urandom(32)  # AES-256
    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    pad_len = 16 - (len(message) % 16)
    padded_message = message + bytes([pad_len] * pad_len)
    ciphertext = encryptor.update(padded_message) + encryptor.finalize()

    encrypted_key = cle_publique_rsa.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return encrypted_key + iv + ciphertext

# Charger les relais
relais = charger_relais_par_ordre("relay.csv")

# Sélection aléatoire de relais par ordre
relais_choisis = []
for ordre in sorted(relais.keys()):
    relai = secrets.choice(relais[ordre])
    relais_choisis.append(relai)

# Destination finale
serveur = ('127.0.0.1', 9000)

# Message initial
data = "Bonjour, ici le client !"
message = data.encode()

# Construction du message en oignon
for i in reversed(range(len(relais_choisis))):
    nom, ip, port, cle_pub_b64 = relais_choisis[i]
    suivant = (relais_choisis[i + 1][1], relais_choisis[i + 1][2]) if i + 1 < len(relais_choisis) else serveur
    enveloppe = f"{suivant},".encode() + message

    cle_publique = charger_cle_publique_base64(cle_pub_b64)
    message = chiffrer_hybride(enveloppe, cle_publique)

# Envoi au premier relai
_, ip, port, _ = relais_choisis[0]
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ip, port))
client_socket.send(message)

# Réception de la réponse finale
response = client_socket.recv(4096).decode()
print("Réponse finale reçue :", response)
client_socket.close()
