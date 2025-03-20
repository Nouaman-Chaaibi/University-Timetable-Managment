import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedTk
import sqlite3

jours = 6
periodes = 5
pause = 3  # recess after 3rd Period
filiere = None
butt_grid = []

noms_periodes = ['09h00-->10h45', '11h00-->12h45', '13h00-->14h45', '15h00-->16h45', '17h00-->18h45']
noms_jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']


def update_p(d, p, tree, parent):
    try:
        if len(tree.selection()) > 1:
            messagebox.showerror("Sélection incorrecte", "Sélectionnez un module à la fois !")
            parent.destroy()
            return

        row = tree.item(tree.selection()[0])['values']
        schedule_id = filiere + str((d * periodes) + p)

        if row[0] == 'NULL' and row[1] == 'NULL':
            conn.execute(f"DELETE FROM SCHEDULE WHERE ID='{schedule_id}'")
        else:
            conn.execute(f"UPDATE SCHEDULE SET SUBCODE='{row[1]}', ENS_ABV='{row[0]}', ENSEIGNANT='{row[0]}'\
                WHERE DAYID='{d}' AND PERIODID='{p}' AND FILIERE='{filiere}' ")

        conn.commit()
        update_table()

    except IndexError:
        messagebox.showerror("Sélection incorrecte", "Veuillez sélectionner un module dans la liste!")

    parent.destroy()



def process_button(d, p):
    print(d, p)
    add_p = tk.Tk()
    cursor = conn.execute("SELECT SUBCODE FROM SUBJECTS WHERE FILIERE=?", (filiere,))
    subcode_li = [row[0] for row in cursor]
    subcode_li.insert(0, 'NULL')

    tk.Label(add_p, text='Sélectionner un module', font=('Arial Rounded MT Bold', 12, 'bold')).pack()
    tk.Label(add_p, text=f'Jour: {noms_jours[d]}', font=('Arial Rounded MT Bold', 12)).pack()
    tk.Label(add_p, text=f'Periode: {p+1}', font=('Arial Rounded MT Bold', 12)).pack()

    tree = ttk.Treeview(add_p)
    tree['columns'] = ('un', 'deux')
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("un", width=200, stretch=tk.NO)
    tree.column("deux", width=100, stretch=tk.NO)
    tree.heading('#0', text="")
    tree.heading('un', text="Enseignant")
    tree.heading('deux', text="Code module")

    cursor = conn.execute("SELECT ENSEIGNANTS.NAME, ENSEIGNANTS.SUBCODE1, ENSEIGNANTS.SUBCODE2, SUBJECTS.SUBCODE\
    FROM ENSEIGNANTS, SUBJECTS\
    WHERE ENSEIGNANTS.SUBCODE1=SUBJECTS.SUBCODE OR ENSEIGNANTS.SUBCODE2=SUBJECTS.SUBCODE")
    for row in cursor:
        print(row)
        tree.insert(
            "",
            0,
            values=(row[0], row[-1])
        )
    tree.pack(pady=10, padx=30)

    tk.Button(
        add_p,
        text="OK",
        padx=15,
        command=lambda x=d, y=p, z=tree, d=add_p: update_p(x, y, z, d)
    ).pack(pady=20)

    add_p.mainloop()


def select_sec():
    global filiere
    filiere = str(combo1.get())
    print(filiere)
    update_table()


def update_table():
    for i in range(jours):
        for j in range(periodes):
            cursor = conn.execute(f"SELECT SUBCODE, ENS_ABV FROM SCHEDULE\
                WHERE DAYID={i} AND PERIODID={j} AND FILIERE='{filiere}'")
            cursor = list(cursor)
            print(cursor)
            if len(cursor) != 0:
                butt_grid[i][j]['text'] = str(cursor[0][0]) + '\n' + str(cursor[0][1])
                butt_grid[i][j].update()
                print(i, j, cursor[0][0])



# connecting database
conn = sqlite3.connect(r'files/Data_projet.db')

# creating Table in the database
conn.execute('CREATE TABLE IF NOT EXISTS SCHEDULE\
(ID CHAR(10) NOT NULL PRIMARY KEY,\
DAYID INT NOT NULL,\
PERIODID INT NOT NULL,\
SUBCODE CHAR(10) NOT NULL,\
FILIERE CHAR(5) NOT NULL,\
FINI CHAR(10) NOT NULL)')
# DAYID AND PERIODID ARE ZERO INDEXED


root = ThemedTk()
root.title('Section timetable')
root.geometry('1000x680+200+10')
root.configure(bg="#f9f9f9")
style = ttk.Style(root)
style.theme_use('adapta')

# Ajout de l'image
img_path = "images/FSTT.png"
img = tk.PhotoImage(file=img_path)
img_label = tk.Label(root, image=img,background='#f9f9f9')
img_label.pack()

title_lab = tk.Label(
    root,
    text='Emploi du temps 2023/2024',
    font=('Algerian', 20, 'bold'),
    foreground='#ffb432',
    background='#f9f9f9',
    pady=5
)
title_lab.pack()

table = tk.Frame(root)
table.pack()

first_half = tk.Frame(table,background='#f9f9f9')
first_half.pack(side='left')

second_half = tk.Frame(table,background='#f9f9f9')
second_half.pack(side='left')

for i in range(jours):
    b = tk.Label(
        first_half,
        text=noms_jours[i],
        font=('Arial Rounded MT Bold', 12, 'bold'),
        width=9,
        height=2,
        background='#7fb3d5',
        bd=5,
        relief='raised'
    )
    b.grid(row=i+1, column=0)

for i in range(periodes):
    if i < pause:
        b = tk.Label(first_half)
        b.grid(row=0, column=i+1)
    else:
        b = tk.Label(second_half)
        b.grid(row=0, column=i)

    b.config(
        text=noms_periodes[i],
        font=('Arial Rounded MT Bold', 12, 'bold'),
        width=14,
        height=1,
        background='#7fb3d5',
        bd=5,
        relief='raised'
    )

for i in range(jours):
    b = []
    for j in range(periodes):
        if j < pause:
            bb = tk.Button(first_half)
            bb.grid(row=i+1, column=j+1)
        else:
            bb = tk.Button(second_half)
            bb.grid(row=i+1, column=j)

        bb.config(
            text='Hello World!',
            font=('Arial Rounded MT Bold', 10),
            width=18,
            height=3,
            background='white',
            bd=5,
            relief='raised',
            wraplength=120,
            justify='center',
            command=lambda x=i, y=j: process_button(x, y)
        )
        b.append(bb)

    butt_grid.append(b)

sec_select_f = tk.Frame(root, pady=15,background='#f9f9f9')
sec_select_f.pack()

tk.Label(
    sec_select_f,
    text='Sélectionnez la filière:  ',
    font=('Arial Rounded MT Bold', 18, 'bold'),
    foreground='#ffb432',
    background='#f9f9f9'
).pack(side=tk.LEFT)

cursor = conn.execute("SELECT DISTINCT FILIERE FROM FILIERES")
sec_li = [row[0] for row in cursor]
print(sec_li)
combo1 = ttk.Combobox(
    sec_select_f,
    values=sec_li,
    width=50,
)
combo1.pack(side=tk.LEFT)
combo1.current(0)

b = tk.Button(
    sec_select_f,
    text="OK",
    font=('Arial Rounded MT Bold', 12, 'bold'),
    background='#7fb3d5',
    padx=10,
    command=select_sec
)
b.pack(side=tk.LEFT, padx=10)
b.invoke()

update_table()

root.mainloop()
