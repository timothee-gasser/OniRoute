import csv
import os
import base64
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


fichier_csv = "relay.csv"
temp_csv = "relay_temp.csv"
KEYS_DIR = "keys"
os.makedirs(KEYS_DIR, exist_ok=True)

# Lecture + génération clés
with open(fichier_csv, newline='') as infile, open(temp_csv, "w", newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        if len(row) < 4:
            continue  # Ligne invalide

        ordre = row[0].strip()
        nom = row[1].strip()
        ip = row[2].strip()
        port = row[3].strip()

        # Générer les clés
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()

        # Sauvegarde de la clé privée
        with open(f"{KEYS_DIR}/{nom}_private.pem", "wb") as f:
            f.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
            )

        # Encode la clé publique pour CSV
        pub_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        pub_b64 = base64.b64encode(pub_bytes).decode("utf-8")

        # Nouvelle ligne avec clé publique
        nouvelle_ligne = [ordre, nom, ip, port, pub_b64]
        writer.writerow(nouvelle_ligne)

# Remplace l’ancien CSV
os.replace(temp_csv, fichier_csv)

print("✅ Clés générées et relay.csv mis à jour avec les clés publiques.")
