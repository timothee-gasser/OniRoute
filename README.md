# OniRoute

**OniRoute** est une preuve de concept (POC) de routage en oignon (onion routing) développée en Python. Il permet de simuler un enchaînement de relais chiffrés inspiré du fonctionnement du réseau Tor. Ce projet est conçu comme un exercice personnel pour mieux comprendre la **sécurisation des réseaux** et la **cryptographie**.

## 🎯 Objectifs pédagogiques

- Comprendre les bases du routage en oignon.
- Appliquer le chiffrement asymétrique et symétrique pour protéger les communications.
- Implémenter un système distribué simulant des nœuds anonymes.

## 📁 Arborescence du projet

```
OniRoute-main/
├── Client.py
├── Client2.py
├── Serveur.py
├── Key_gen.py
├── relay.csv
├── keys/
│   └── *.pem                  # Clés privées des relais
└── Relay/
    ├── Relay1/
    ├── Relay2/
    ├── Relay3/
    └── Relay4/
        └── relayX.Y.py       # Scripts pour relais à différents niveaux
```

## 🔧 Composants principaux

- `Client.py` / `Client2.py` : Clients qui construisent un circuit, chiffrent le message en couches, et l’envoient via les relais.
- `Serveur.py` : Serveur final qui reçoit et affiche les messages une fois totalement déchiffrés.
- `Relay/RelayX/relayX.Y.py` : Représente un relais de niveau Y dans le circuit. Chaque relais déchiffre une couche et transfère le message.
- `Key_gen.py` : Générateur de paires de clés (clé privée PEM).
- `relay.csv` : Fichier de configuration listant les relais et leurs clés.
- `keys/` : Contient les clés privées des relais en format PEM.

## 📄 Format du fichier `relay.csv`

```
niveau_du_noeud, identifiant_noeud (hex), port, clef_de_chiffrement
```

### Exemple :
```
1,01,5001,0123456789abcdef0123456789abcdef
2,02,5002,abcdef0123456789abcdef0123456789
3,03,5003,6789abcdef0123456789abcdef012345
```

- `niveau_du_noeud` : Position dans la chaîne (de 1 à N).
- `identifiant_noeud` : Identifiant en hexadécimal.
- `port` : Port d’écoute du relais.
- `clef_de_chiffrement` : Clé AES utilisée pour le déchiffrement symétrique de cette couche.

## 🔐 Fonctionnement

1. Le **client** sélectionne une chaîne de relais depuis `relay.csv`.
2. Il chiffre le message en autant de couches qu’il y a de relais (chiffrement en oignon).
3. Le message traverse les relais. Chaque relais :
   - Déchiffre une couche.
   - Lit l’adresse suivante.
   - Relaye le message suivant.
4. Le **serveur final** reçoit le message totalement déchiffré.

## ▶️ Exécution

1. **Générer les clés (si nécessaire) :**
   ```bash
   python Key_gen.py
   ```

2. **Lancer les relais :**
   ```bash
   python Relay/RelayX/relayX.Y.py
   ```

3. **Lancer le serveur :**
   ```bash
   python Serveur.py
   ```

4. **Lancer un client pour envoyer un message :**
   ```bash
   python Client.py
   ```

## 🛡️ Technologies utilisées

- **Python 3**
- **Cryptographie** :
  - `cryptography` ou `pycryptodome` pour le chiffrement AES.
  - Fichiers PEM pour la gestion des clés.


## 🔐 Sécurité & Chiffrement

Ce projet repose sur un **chiffrement hybride**, combinant chiffrement asymétrique et symétrique :

- Le **client** chiffre une clé AES pour chaque relais à l’aide de la **clé publique** correspondante (non incluse dans le dépôt).
- Le **message** est ensuite chiffré avec cette clé AES.
- Chaque **relais** ne possède que sa **clé privée**, ce qui lui permet de déchiffrer uniquement **sa propre couche** du message.

### 🔒 Confidentialité

- Un relais ne connaît que :
  - Sa propre clé privée.
  - L'adresse du **relais suivant**.
  - La **couche suivante du message**, toujours chiffrée.

- Un relais **ne peut pas** :
  - Lire le message complet.
  - Connaître l'identité de l'expéditeur.
  - Connaître l'identité du destinataire.

Ce mécanisme garantit un haut niveau d’anonymat et d’isolation entre les nœuds du circuit.

## 📚 Ressources utiles

- [Routage en oignon sur Wikipédia](https://fr.wikipedia.org/wiki/Routage_en_oignon)
- [Tor Project](https://www.torproject.org/)

## 📝 Licence

Projet éducatif open-source — libre à modifier et utiliser dans le cadre d’un apprentissage personnel.
