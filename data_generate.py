import sqlite3
from faker import Faker
import random
from datetime import datetime

# Connexion à SQLite
conn = sqlite3.connect("magasin.db")
cursor = conn.cursor()

# Création des tables (ajout de mois_vente dans Details_Ventes)
cursor.executescript("""
CREATE TABLE IF NOT EXISTS Produits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    categorie TEXT,
    prix_unitaire REAL NOT NULL,
    stock_disponible INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS Clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    email TEXT,
    telephone TEXT,
    adresse TEXT
);

CREATE TABLE IF NOT EXISTS Ventes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER,
    date_vente TEXT NOT NULL,
    FOREIGN KEY (client_id) REFERENCES Clients(id)
);

CREATE TABLE IF NOT EXISTS Details_Ventes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vente_id INTEGER,
    produit_id INTEGER,
    quantite INTEGER NOT NULL,
    montant_total REAL NOT NULL,
    mois_vente INTEGER NOT NULL,
    FOREIGN KEY (vente_id) REFERENCES Ventes(id),
    FOREIGN KEY (produit_id) REFERENCES Produits(id)
);
""")

fake = Faker()

# Dictionnaire de vrais noms de produits par catégorie
produits_reels = {
    "Électronique": ["iPhone 15", "Samsung Galaxy S23", "MacBook Pro", "AirPods Pro", "PlayStation 5", "TV OLED LG", "Apple Watch", "Casque Bose", "Drone DJI", "Nintendo Switch"],
    "Vêtements": ["Jean Levi's", "T-shirt Nike", "Sweat Adidas", "Robe Zara", "Chaussures Puma", "Veste North Face", "Lunettes Ray-Ban", "Montre Fossil", "Casquette New Era"],
    "Maison": ["Aspirateur Dyson", "Machine à café Nespresso", "Table Ikea", "Lampe Philips Hue", "Four Samsung", "Frigo LG", "Canapé Maison du Monde", "Matelas Emma"],
    "Alimentation": ["Nutella", "Coca-Cola", "Kinder Bueno", "Pâtes Barilla", "Riz Uncle Ben's", "Chocolat Lindt", "Café Lavazza", "Eau Evian"],
    "Beauté": ["Parfum Chanel", "Shampoing Kérastase", "Crème Nivea", "Rouge à lèvres MAC", "Gel douche Dove", "Mascara Maybelline", "Fond de teint L’Oréal"]
}

# Génération des produits
produits = []
for _ in range(50000):
    categorie = random.choice(list(produits_reels.keys()))
    nom = random.choice(produits_reels[categorie])
    prix_unitaire = round(random.uniform(5, 500), 2)
    stock = random.randint(10, 500)

    cursor.execute("INSERT INTO Produits (nom, categorie, prix_unitaire, stock_disponible) VALUES (?, ?, ?, ?)",
                   (nom, categorie, prix_unitaire, stock))
    produits.append(cursor.lastrowid)

# Génération des clients
clients = []
for _ in range(10000):
    nom = fake.name()
    email = fake.email()
    telephone = fake.phone_number()
    adresse = fake.address()
    
    cursor.execute("INSERT INTO Clients (nom, email, telephone, adresse) VALUES (?, ?, ?, ?)",
                   (nom, email, telephone, adresse))
    clients.append(cursor.lastrowid)

# Génération des ventes et des détails de ventes
for _ in range(30000):
    client_id = random.choice(clients)
    date_vente = fake.date_time_between(start_date="-1y", end_date="now")
    mois_vente = date_vente.month  # Extraire le mois de la vente

    cursor.execute("INSERT INTO Ventes (client_id, date_vente) VALUES (?, ?)", 
                   (client_id, date_vente.strftime("%Y-%m-%d %H:%M:%S")))
    vente_id = cursor.lastrowid

    # Ajouter 1 à 3 produits par vente
    for _ in range(random.randint(1, 3)):
        produit_id = random.choice(produits)
        quantite = random.randint(1, 10)
        
        cursor.execute("SELECT prix_unitaire FROM Produits WHERE id = ?", (produit_id,))
        prix_unitaire = cursor.fetchone()[0]
        montant_total = round(quantite * prix_unitaire, 2)

        cursor.execute("INSERT INTO Details_Ventes (vente_id, produit_id, quantite, montant_total, mois_vente) VALUES (?, ?, ?, ?, ?)",
                       (vente_id, produit_id, quantite, montant_total, mois_vente))

# Commit et fermeture
conn.commit()
cursor.close()
conn.close()

print("Base de données SQLite chargée avec succès !")
