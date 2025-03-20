import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedTk

class GestionnaireModules:
    def __init__(self, root):
        self.root = root
        self.connexion_bd = sqlite3.connect('files/Data_projet.db')
        self.image_top = tk.PhotoImage(file='images/FSTT.png')
        self.image_pattern= tk.PhotoImage(file='images/Pattern_icone.png')
        self.mise_en_place_interface()
        self.charger_modules_existants()

    def charger_modules_existants(self):
        curseur = self.connexion_bd.execute("SELECT * FROM SUBJECTS")
        for ligne in curseur:
            self.tree.insert("", 0, values=ligne)

    def mise_en_place_interface(self):
        self.root.geometry('800x650+300+30')
        self.root.title('Gestionnaire de Modules')
        self.root.configure(background="#fff")
        self.root.resizable(True, True)

        self.creer_widgets()

    def creer_widgets(self):
        # Ajoute l'image avant le titre
        label_image = ttk.Label(self.root, image=self.image_top, padding=(0, 0, 0, 0),background='white')
        label_image.pack(pady=5)

        ttk.Label(self.root, text='Liste des Modules de toutes les filières', foreground='#ffb432',font=('Algerian', 20, 'bold'),background='white').pack(pady=5)
        label_image = ttk.Label(self.root, image=self.image_pattern, padding=(0, 0, 0, 0),background='white')
        label_image.place(x=20,y=200)
        label_image = ttk.Label(self.root, image=self.image_pattern, padding=(0, 0, 0, 0),background='white')
        label_image.place(x=520,y=200)

        self.entree_code_module = tk.Entry(self.root, font=('Arial Rounded MT Bold', 12),borderwidth=2,width=20)
        self.entree_nom_module = tk.Text(self.root, font=('Arial Rounded MT Bold', 10),borderwidth=2, width=20, height=2, wrap=tk.WORD)

        ttk.Label(self.root, text='ID module:',font=('Arial Rounded MT Bold', 12),foreground='#2876dc',background='white').pack(pady=5)
        self.entree_code_module.pack(pady=1)
        ttk.Label(self.root, text='Nom module:',font=('Arial Rounded MT Bold', 12),foreground='#2876dc',background='white').pack(pady=5)
        self.entree_nom_module.pack(pady=1)

        self.variable_radio = tk.StringVar()
        ttk.Radiobutton(self.root, text='Cours', style='TRadiobutton', variable=self.variable_radio, value='Cours').pack(pady=1)
        ttk.Radiobutton(self.root, text='TD', style='TRadiobutton', variable=self.variable_radio, value='TD').pack(pady=1)

        ttk.Button(self.root, text='Ajouter Module', style='TButton', command=self.ajouter_module).pack(pady=1)
        ttk.Button(self.root, text='Supprimer Module', style='TButton', command=self.supprimer_module).pack(pady=1)

        # Utilisation de ttk.Treeview pour le widget tree
        self.tree = ttk.Treeview(self.root, columns=('ID', 'Nom', 'Type'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nom', text='Nom')
        self.tree.heading('Type', text='Type')
        self.tree.pack(padx=10, pady=10)
        
    def ajouter_module(self):
        code_module = self.entree_code_module.get().strip()
        nom_module = self.entree_nom_module.get("1.0", tk.END).strip()
        type_module = self.variable_radio.get()

        if not code_module or not nom_module:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return

        # Vérifier si l'ID du module existe déjà
        if self.module_existe_deja(code_module):
            messagebox.showerror("Erreur", "L'ID du module existe déjà.")
            return

        self.connexion_bd.execute("INSERT INTO SUBJECTS (SUBCODE, SUBNAME, SUBTYPE) VALUES (?, ?, ?)",
                        (code_module, nom_module, type_module))
        self.connexion_bd.commit()

        self.tree.insert("", 0, values=(code_module, nom_module, type_module))
        self.vider_champs()

    def module_existe_deja(self, code_module):
        curseur = self.connexion_bd.execute("SELECT COUNT(*) FROM SUBJECTS WHERE SUBCODE=?", (code_module,))
        nombre_modules = curseur.fetchone()[0]
        return nombre_modules > 0

        self.tree.insert("", 0, values=(code_module, nom_module, type_module))
        self.vider_champs()

    def supprimer_module(self):
        item_selectionne = self.tree.selection()
        if not item_selectionne:
            messagebox.showerror("Erreur", "Veuillez sélectionner un module.")
            return

        code_module = self.tree.item(item_selectionne)['values'][0]

        self.connexion_bd.execute("DELETE FROM SUBJECTS WHERE SUBCODE=?", (code_module,))
        self.connexion_bd.commit()

        self.tree.delete(item_selectionne)

    def vider_champs(self):
        self.entree_code_module.delete(0, tk.END)
        self.entree_nom_module.delete("1.0", tk.END)


root = ThemedTk()
style = ttk.Style(root)
style.theme_use('adapta')
style.configure('TRadiobutton', background='white', foreground='#2876dc', font=('Arial', 10, 'bold'))
style.configure('TButton', background='white', foreground='#2876dc', font=('Arial', 10, 'bold'))

gestionnaire_modules = GestionnaireModules(root)

root.mainloop()
