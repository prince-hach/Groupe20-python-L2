import sqlite3

# Connexion à la base de données SQLite (créée si elle n'existe pas)
def get_connection():
    return sqlite3.connect('contrats.db')

# Création de la table des contrats si elle n'existe pas
def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contrats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            locataire TEXT NOT NULL,
            parcelle TEXT NOT NULL,
            date_debut TEXT NOT NULL,
            date_fin TEXT NOT NULL,
            montant REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Ajouter un contrat
def ajouter_contrat(locataire, parcelle, date_debut, date_fin, montant):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO contrats (locataire, parcelle, date_debut, date_fin, montant)
        VALUES (?, ?, ?, ?, ?)
    ''', (locataire, parcelle, date_debut, date_fin, montant))
    conn.commit()
    conn.close()

# Récupérer tous les contrats
def lister_contrats():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contrats')
    result = cursor.fetchall()
    conn.close()
    return result

# Modifier un contrat
def modifier_contrat(contrat_id, locataire, parcelle, date_debut, date_fin, montant):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE contrats SET locataire=?, parcelle=?, date_debut=?, date_fin=?, montant=? WHERE id=?
    ''', (locataire, parcelle, date_debut, date_fin, montant, contrat_id))
    conn.commit()
    conn.close()

# Supprimer un contrat
def supprimer_contrat(contrat_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contrats WHERE id=?', (contrat_id,))
    conn.commit()
    conn.close()

# Rechercher des contrats par locataire ou parcelle
def rechercher_contrats(terme):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM contrats WHERE locataire LIKE ? OR parcelle LIKE ?
    ''', (f'%{terme}%', f'%{terme}%'))
    result = cursor.fetchall()
    conn.close()
    return result 