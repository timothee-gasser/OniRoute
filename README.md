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



## 🔐 Chiffrement Hybride : Principe et Raisons

OniRoute utilise une approche de **chiffrement hybride** pour combiner les avantages des deux grandes familles de cryptographie : **asymétrique (RSA)** et **symétrique (AES)**.

### 🔄 Étapes du chiffrement hybride pour chaque relais

1. 🔐 Générer une **clé AES** aléatoire (256 bits) :
   ```python
   key = os.urandom(32)
   ```

2. 🔒 Chiffrer le **message** avec AES (en mode CBC ou GCM) :
   ```python
   encrypted_message = aes_encrypt(message, key, iv)
   ```

3. 🔐 Chiffrer la **clé AES** avec la **clé publique RSA** du relais :
   ```python
   encrypted_key = rsa_encrypt(key, relay_public_key)
   ```

4. 📦 Combiner :
   - Clé AES chiffrée
   - IV (vecteur d'initialisation)
   - Message chiffré

   En un seul bloc transmis au relais :
   ```plaintext
   [clé AES chiffrée] + [IV] + [message AES chiffré]
   ```

### ❓ Pourquoi ce choix ?

- ✅ **Sécurité renforcée** : la clé AES est protégée par RSA, ce qui empêche un relais non autorisé de la lire.
- ✅ **Performance** : le chiffrement symétrique (AES) est bien plus rapide que le chiffrement asymétrique pour les données volumineuses.
- ✅ **Modularité** : chaque couche de chiffrement est indépendante, assurant qu’un relais ne peut pas remonter à l’expéditeur ni lire le contenu final.
- ✅ **Confidentialité** : comme chaque relais ne détient que sa **clé privée**, il est incapable :
  - De reconstituer l'intégralité du message.
  - D’identifier l'expéditeur ou le destinataire final.

Cette méthode est inspirée des principes appliqués dans des protocoles anonymes comme **Tor**, tout en restant légère et pédagogique pour un usage d’apprentissage.


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
