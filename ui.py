import tkinter as tk
from tkinter import ttk, messagebox
import db

class ContratApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Gestion des Contrats de Bail')
        self.root.geometry('800x500')
        
        # Champs de saisie
        self.frame_form = tk.Frame(root)
        self.frame_form.pack(pady=10)
        
        tk.Label(self.frame_form, text='Locataire').grid(row=0, column=0)
        self.entry_locataire = tk.Entry(self.frame_form)
        self.entry_locataire.grid(row=0, column=1)
        
        tk.Label(self.frame_form, text='Parcelle').grid(row=0, column=2)
        self.entry_parcelle = tk.Entry(self.frame_form)
        self.entry_parcelle.grid(row=0, column=3)
        
        tk.Label(self.frame_form, text='Date début').grid(row=1, column=0)
        self.entry_date_debut = tk.Entry(self.frame_form)
        self.entry_date_debut.grid(row=1, column=1)
        
        tk.Label(self.frame_form, text='Date fin').grid(row=1, column=2)
        self.entry_date_fin = tk.Entry(self.frame_form)
        self.entry_date_fin.grid(row=1, column=3)
        
        tk.Label(self.frame_form, text='Montant').grid(row=2, column=0)
        self.entry_montant = tk.Entry(self.frame_form)
        self.entry_montant.grid(row=2, column=1)
        
        # Boutons d'action
        self.btn_ajouter = tk.Button(self.frame_form, text='Ajouter', command=self.ajouter_contrat)
        self.btn_ajouter.grid(row=2, column=2)
        
        self.btn_modifier = tk.Button(self.frame_form, text='Modifier', command=self.modifier_contrat)
        self.btn_modifier.grid(row=2, column=3)
        
        self.btn_supprimer = tk.Button(self.frame_form, text='Supprimer', command=self.supprimer_contrat)
        self.btn_supprimer.grid(row=2, column=4)
        
        # Recherche
        self.frame_recherche = tk.Frame(root)
        self.frame_recherche.pack(pady=5)
        tk.Label(self.frame_recherche, text='Recherche (locataire ou parcelle):').pack(side=tk.LEFT)
        self.entry_recherche = tk.Entry(self.frame_recherche)
        self.entry_recherche.pack(side=tk.LEFT)
        self.btn_rechercher = tk.Button(self.frame_recherche, text='Rechercher', command=self.rechercher_contrats)
        self.btn_rechercher.pack(side=tk.LEFT)
        self.btn_tout_afficher = tk.Button(self.frame_recherche, text='Tout afficher', command=self.charger_contrats)
        self.btn_tout_afficher.pack(side=tk.LEFT)
        
        # Tableau des contrats
        self.tree = ttk.Treeview(root, columns=('id', 'locataire', 'parcelle', 'date_debut', 'date_fin', 'montant'), show='headings')
        for col in self.tree['columns']:
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        self.selected_id = None
        self.charger_contrats()

    def ajouter_contrat(self):
        # Récupérer les valeurs des champs
        locataire = self.entry_locataire.get()
        parcelle = self.entry_parcelle.get()
        date_debut = self.entry_date_debut.get()
        date_fin = self.entry_date_fin.get()
        montant = self.entry_montant.get()
        if not (locataire and parcelle and date_debut and date_fin and montant):
            messagebox.showwarning('Champs manquants', 'Veuillez remplir tous les champs.')
            return
        try:
            db.ajouter_contrat(locataire, parcelle, date_debut, date_fin, float(montant))
            self.charger_contrats()
            self.clear_form()
        except Exception as e:
            messagebox.showerror('Erreur', str(e))

    def charger_contrats(self):
        # Afficher tous les contrats dans le tableau
        for row in self.tree.get_children():
            self.tree.delete(row)
        for contrat in db.lister_contrats():
            self.tree.insert('', tk.END, values=contrat)

    def on_select(self, event):
        # Remplir le formulaire avec les données sélectionnées
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])['values']
            self.selected_id = values[0]
            self.entry_locataire.delete(0, tk.END)
            self.entry_locataire.insert(0, values[1])
            self.entry_parcelle.delete(0, tk.END)
            self.entry_parcelle.insert(0, values[2])
            self.entry_date_debut.delete(0, tk.END)
            self.entry_date_debut.insert(0, values[3])
            self.entry_date_fin.delete(0, tk.END)
            self.entry_date_fin.insert(0, values[4])
            self.entry_montant.delete(0, tk.END)
            self.entry_montant.insert(0, values[5])

    def modifier_contrat(self):
        # Modifier le contrat sélectionné
        if not self.selected_id:
            messagebox.showwarning('Sélection', 'Veuillez sélectionner un contrat à modifier.')
            return
        locataire = self.entry_locataire.get()
        parcelle = self.entry_parcelle.get()
        date_debut = self.entry_date_debut.get()
        date_fin = self.entry_date_fin.get()
        montant = self.entry_montant.get()
        if not (locataire and parcelle and date_debut and date_fin and montant):
            messagebox.showwarning('Champs manquants', 'Veuillez remplir tous les champs.')
            return
        try:
            db.modifier_contrat(self.selected_id, locataire, parcelle, date_debut, date_fin, float(montant))
            self.charger_contrats()
            self.clear_form()
        except Exception as e:
            messagebox.showerror('Erreur', str(e))

    def supprimer_contrat(self):
        # Supprimer le contrat sélectionné
        if not self.selected_id:
            messagebox.showwarning('Sélection', 'Veuillez sélectionner un contrat à supprimer.')
            return
        try:
            db.supprimer_contrat(self.selected_id)
            self.charger_contrats()
            self.clear_form()
        except Exception as e:
            messagebox.showerror('Erreur', str(e))

    def rechercher_contrats(self):
        # Rechercher des contrats par locataire ou parcelle
        terme = self.entry_recherche.get()
        for row in self.tree.get_children():
            self.tree.delete(row)
        for contrat in db.rechercher_contrats(terme):
            self.tree.insert('', tk.END, values=contrat)

    def clear_form(self):
        # Réinitialiser le formulaire
        self.entry_locataire.delete(0, tk.END)
        self.entry_parcelle.delete(0, tk.END)
        self.entry_date_debut.delete(0, tk.END)
        self.entry_date_fin.delete(0, tk.END)
        self.entry_montant.delete(0, tk.END)
        self.selected_id = None 