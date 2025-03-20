import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

jours = 6
periodes = 5
recess_break_aft = 3 # recess after 3rd Period
name = None
butt_grid = []


noms_periodes = ['09h00-->10h45', '11h00-->12h45', '13h00-->14h45', '15h00-->16h45', '17h00-->18h45']
noms_jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']


def select_fac():
    global name
    name = str(combo1.get())
    print(name)
    update_table(name)



def update_table(name):
    for i in range(jours):
        for j in range(periodes):
            cursor = conn.execute(f"SELECT FILIERE, SUBCODE FROM SCHEDULE\
                WHERE DAYID={i} AND PERIODID={j} AND ENSEIGNANT='{name}'")
            cursor = list(cursor)
            print(cursor)
            
            butt_grid[i][j]
            if len(cursor) != 0:
                subcode = cursor[0][1]
                cur1 = conn.execute(F"SELECT SUBTYPE FROM SUBJECTS WHERE SUBCODE='{subcode}'")
                cur1 = list(cur1)
                subtype = cur1[0][0]
                butt_grid[i][j]['fg'] = 'black'
                if subtype == 'T':
                    butt_grid[i][j]['bg'] = 'green'
                elif subtype == 'P':
                    butt_grid[i][j]['bg'] = 'blue'

                sec_li = [x[0] for x in cursor]
                t = ', '.join(sec_li)
                butt_grid[i][j]['text'] = t
                print(i, j, cursor[0][0])
            else:
                butt_grid[i][j]['fg'] = 'black'
                butt_grid[i][j]['text'] = "No Class"
                butt_grid[i][j].update()



def process_button(d, p):
    print(d, p, name)
    details = tk.Tk()
    cursor = conn.execute(f"SELECT FILIERE, SUBCODE FROM SCHEDULE\
                WHERE DAYID={d} AND PERIODID={p} AND ENSEIGNANT='{name}'")
    cursor = list(cursor)
    print("section", cursor)
    if len(cursor) != 0:
        sec_li = [x[0] for x in cursor]
        t = ', '.join(sec_li)
        subcode = cursor[0][1]
        cur1 = conn.execute(f"SELECT SUBNAME, SUBTYPE FROM SUBJECTS\
            WHERE SUBCODE='{subcode}'")
        cur1 = list(cur1)
        subname = str(cur1[0][0])
        subtype = str(cur1[0][1])

        if subtype == 'T':
            subtype = 'Theory'
        elif subtype == 'P':
            subtype = 'Practical'

    #     print(subcode, NAME, subname, subtype, fname, femail)
    else:
        sec_li = subcode = subname = subtype = t = 'None'

    tk.Label(details, text='Class Details', font=('Consolas', 15, 'bold')).pack(pady=15)
    tk.Label(details, text='Day: '+noms_jours[d], font=('Consolas'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Period: '+str(p+1), font=('Consolas'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Subject Code: '+subcode, font=('Consolas'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Subject Name: '+subname, font=('Consolas'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Subject Type: '+subtype, font=('Consolas'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Teacher Name: '+name, font=('Consolas'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Sections: '+t, font=('Consolas'), anchor="w").pack(expand=1, fill=tk.X, padx=20)

    tk.Button(
        details,
        text="OK",
        font=('Consolas'),
        width=10,
        command=details.destroy
    ).pack(pady=10)

    details.mainloop()



def fac_tt_frame(tt, f):
    img_path = "images/FSTT.png"

    img = tk.PhotoImage(file=img_path)
    
    img_label = tk.Label(tt,image=img,background='#f9f9f9')
    img_label.image = img
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


    global butt_grid
    global NAME
    NAME = f

    table = tk.Frame(tt,background='#f9f9f9')
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
        if i < recess_break_aft:
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
            if j < recess_break_aft:
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
        # print(b)
        b = []

    print(butt_grid[0][1], butt_grid[1][1])
    update_table(NAME)


    # connecting database
conn = sqlite3.connect(r'files/Data_projet.db')
if __name__ == "__main__":
    
    root = tk.Tk()
    root.title('Teacher Timetable')
    root.geometry('1000x680+200+10')
    root.configure(bg="#f9f9f9")

    fac_tt_frame(root, name)

    fac_select_f = tk.Frame(root, pady=15,background='#f9f9f9')
    fac_select_f.pack()

    tk.Label(
        fac_select_f,
        text='Selectionnez un prof:  ',
        font=('Arial Rounded MT Bold', 18, 'bold'),
        foreground='#ffb432',
        background='#f9f9f9'
    ).pack(side=tk.LEFT)

    cursor = conn.execute("SELECT DISTINCT NAME FROM ENSEIGNANTS")
    fac_li = [row[0] for row in cursor]
    print(fac_li)
    combo1 = ttk.Combobox(
        fac_select_f,
        values=fac_li,
        width=25,
    )
    combo1.pack(side=tk.LEFT)
    combo1.current(0)

    b = tk.Button(
        fac_select_f,
        text="OK",
        font=('Arial Rounded MT Bold', 12, 'bold'),
        background='#7fb3d5',
        padx=10,
        command=select_fac
    )
    b.pack(side=tk.LEFT, padx=10)
    b.invoke()


    root.mainloop()