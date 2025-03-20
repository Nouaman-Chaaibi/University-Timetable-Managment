import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk


class GestionnaireProf:
    def __init__(self, root):
        self.root = root
        self.image_top = tk.PhotoImage(file='images/FSTT.png')
        self.mise_en_place_interface()

    def mise_en_place_interface(self):
        self.root.geometry('1000x550+200+60')
        self.root.title('Ajouter/Supprimer/Mettre à jour des profs')
        self.root.configure(background="#fff")
        self.root.resizable(True, True)

        self.entrees = {}
        self.combos = {}
        label_image = ttk.Label(self.root, image=self.image_top, style='TLabel', padding=(0, 0, 0, 0),background='white')
        label_image.pack(pady=1)

        labels = [
            'ID PROF:', 'Mot de passe:',  'Nom du prof:',
            'Initiales:', 'Email:', 'Matière 1:', 'Matière 2:'
        ]

        positions_entrees = [(100, 150), (100, 190), (100, 230), (100, 270),
                           (100, 310), (100, 360), (100, 400)]

        for i, texte_label in enumerate(labels):
            ttk.Label(self.root, text=texte_label, font=('Arial Rounded MT Bold', 12),background='white',foreground='#2876dc').place(x=positions_entrees[i][0], y=positions_entrees[i][1])

        # Widgets Entry
        noms_entrees = ['eid', 'passw', 'name', 'ini', 'email']
        for i, nom_entree in enumerate(noms_entrees):
            entree = ttk.Entry(self.root, font=('Consolas', 12), width=20 if i < 3 else 25)
            entree.place(x=260, y=positions_entrees[i][1])
            self.entrees[nom_entree] = entree

        # Comboboxes pour le code de la matière
        self.combos['combo1'] = ttk.Combobox(self.root, values=self.get_codes_matieres())
        self.combos['combo1'].place(x=260, y=340)
        self.combos['combo1'].current(0)

        self.combos['combo2'] = ttk.Combobox(self.root, values=self.get_codes_matieres())
        self.combos['combo2'].place(x=260, y=390)
        self.combos['combo2'].current(0)

        # Boutons
        ttk.Button(self.root, text='Ajouter prof',style='TButton', command=self.analyser_donnees).place(x=150, y=485)
        ttk.Button(self.root, text='Mettre à jour prof',style='TButton', command=self.mettre_a_jour_donnees).place(x=410, y=485)
        ttk.Button(self.root, text='Supprimer prof(s)',style='TButton', command=self.supprimer_donnees).place(x=650, y=485)

        # Treeview
        self.tree = ttk.Treeview(self.root)
        self.creer_treeview()
        self.mettre_a_jour_treeview()

    def creer_treeview(self):
        self.tree['columns'] = list(map(lambda x: '#' + str(x), range(1, 5)))
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("#1", width=70, stretch=tk.NO)
        self.tree.column("#2", width=200, stretch=tk.NO)
        self.tree.column("#3", width=80, stretch=tk.NO)
        self.tree.column("#4", width=80, stretch=tk.NO)
        self.tree.heading('#0', text="")
        self.tree.heading('#1', text="ID PROF")
        self.tree.heading('#2', text="Nom")
        self.tree.heading('#3', text="Matière 1")
        self.tree.heading('#4', text="Matière 2")
        self.tree['height'] = 15
        self.tree.place(x=530, y=100)

    def mettre_a_jour_treeview(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        curseur = conn.execute("SELECT EID, NAME, SUBCODE1, SUBCODE2 FROM ENSEIGNANTS")
        for row in curseur:
            self.tree.insert(
                "",
                0,
                values=(row[0], row[1], row[2], row[3])
            )
        self.tree.place(x=530, y=100)

    def analyser_donnees(self):
        eid = str(self.entrees['eid'].get())
        passw = str(self.entrees['passw'].get())
        name = str(self.entrees['name'].get()).upper()
        ini = str(self.entrees['ini'].get()).upper()
        email = str(self.entrees['email'].get())
        subcode1 = str(self.combos['combo1'].get())
        subcode2 = str(self.combos['combo2'].get())

        if eid == "" or passw == "" or name == "":
            messagebox.showwarning("Mauvaise saisie", "Certains champs sont vides ! Veuillez les remplir.")
            return

        if subcode1 == "NULL":
            messagebox.showwarning("Mauvaise saisie", "La Matière 1 ne peut pas être NULL.")
            return

        # Vérifiez si la faculté existe déjà
        curseur = conn.execute("SELECT COUNT(*) FROM ENSEIGNANTS WHERE EID = ?", (eid,))
        count = curseur.fetchone()[0]
        
        if count > 0:
            # La faculté existe, mettez à jour les données
            new_values = {
                'EID': eid,
                'PASSW': passw,
                'NAME': name,
                'INI': ini,
                'EMAIL': email,
                'SUBCODE1': subcode1,
                'SUBCODE2': subcode2
            }

            conn.execute(
                f"REPLACE INTO ENSEIGNANTS (EID, PASSW, NAME, INI, EMAIL, SUBCODE1, SUBCODE2) "
                f"VALUES (:EID, :PASSW, :NAME, :INI, :EMAIL, :SUBCODE1, :SUBCODE2)",
                new_values
            )
        else:
            # La faculté n'existe pas, ajoutez-la simplement
            conn.execute(
                f"INSERT INTO ENSEIGNANTS (EID, PASSW, NAME, INI, EMAIL, SUBCODE1, SUBCODE2) "
                f"VALUES ('{eid}', '{passw}', '{name}', '{ini}', '{email}', '{subcode1}', '{subcode2}')"
            )
        
        conn.commit()
        self.mettre_a_jour_treeview()

        for entree in self.entrees.values():
            entree.delete(0, tk.END)
        self.combos['combo1'].current(0)
        self.combos['combo2'].current(0)


    def mettre_a_jour_donnees(self):
        try:
            if len(self.tree.selection()) != 1:
                messagebox.showerror("Sélection incorrecte", "Sélectionnez un prof à la fois pour mettre à jour !")
                return

            selected_eid = self.tree.item(self.tree.selection()[0])['values'][0]
            curseur = conn.execute(f"SELECT * FROM ENSEIGNANTS WHERE EID = ?", (selected_eid,))

            row = curseur.fetchone()
            if row:
                new_eid = str(self.entrees['eid'].get())
                new_passw = str(self.entrees['passw'].get())
                new_name = str(self.entrees['name'].get()).upper()
                new_ini = str(self.entrees['ini'].get()).upper()
                new_email = str(self.entrees['email'].get())
                new_subcode1 = str(self.combos['combo1'].get())
                new_subcode2 = str(self.combos['combo2'].get())

                # Mettez à jour la base de données avec les nouvelles valeurs
                conn.execute(
                    f"UPDATE ENSEIGNANTS SET EID=?, PASSW=?, NAME=?, INI=?, EMAIL=?, SUBCODE1=?, SUBCODE2=? WHERE EID=?",
                    (new_eid, new_passw, new_name, new_ini, new_email, new_subcode1, new_subcode2, selected_eid)
                )
                conn.commit()

                # Mettez à jour le Treeview
                self.mettre_a_jour_treeview()

        except IndexError:
            messagebox.showerror("Sélection incorrecte", "Veuillez d'abord sélectionner un prof dans la liste !")
            return


    def supprimer_donnees(self):
        if len(self.tree.selection()) < 1:
            messagebox.showerror("Sélection incorrecte", "Veuillez d'abord sélectionner un prof dans la liste !")
            return
        for i in self.tree.selection():
            conn.execute(f"DELETE FROM ENSEIGNANTS WHERE EID = ?", (self.tree.item(i)['values'][0],))
            conn.commit()
            self.tree.delete(i)
            self.mettre_a_jour_treeview()

    def get_codes_matieres(self):
        curseur = conn.execute("SELECT SUBCODE FROM SUBJECTS")
        return [''] + [row[0] for row in curseur]

    def vider_entrees(self):
        for entree in self.entrees.values():
            entree.delete(0, tk.END)
        self.combos['combo1'].current(0)
        self.combos['combo2'].current(0)


if __name__ == "__main__":
    conn = sqlite3.connect('files/Data_projet.db')
    conn.execute('CREATE TABLE IF NOT EXISTS ENSEIGNANTS\
        (EID CHAR(10) NOT NULL PRIMARY KEY,\
        PASSW CHAR(50) NOT NULL,\
        NAME CHAR(50) NOT NULL,\
        INI CHAR(5) NOT NULL,\
        EMAIL CHAR(50) NOT NULL,\
        SUBCODE1 CHAR(10) NOT NULL,\
        SUBCODE2 CHAR(10))')

    root = ThemedTk()
    style = ttk.Style(root)
    style.theme_use('adapta')
    root.configure(bg="#fff")
    style.configure('TButton', background='white', foreground='#2876dc', font=('Arial', 10, 'bold'))

    gestionnaire_faculte = GestionnaireProf(root)
    
    root.mainloop()

    conn.close()
