import socket
import csv
import secrets

def charger_relais_par_ordre(fichier_csv):
    relais_par_ordre = {}

    with open(fichier_csv, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            try:
                ordre = int(row[0])
                ip = row[2].strip()
                port = int(row[3])
                if ordre not in relais_par_ordre:
                    relais_par_ordre[ordre] = []
                relais_par_ordre[ordre].append((ip, port))
            except (IndexError, ValueError):
                continue

    return relais_par_ordre


relais = charger_relais_par_ordre("relay.csv")


relais_choisis = []
for ordre in sorted(relais.keys()):
    relai = secrets.choice(relais[ordre])
    relais_choisis.append(relai)


serveur = ('127.0.0.1', 9000)


data = "Bonjour, ici le client !"


premier_relai = relais_choisis[0]
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(premier_relai)


message_parts = [f"{relai}" for relai in relais_choisis[1:]]
message_parts.append(f"{serveur}")
message_parts.append(data)
message = ",".join(message_parts)


client_socket.send(message.encode())


response = client_socket.recv(1024).decode()
print("Réponse finale reçue :", response)

client_socket.close()
