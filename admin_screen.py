from tkinter import *
import subprocess

root=Tk()
root.title('Admin Screen')
root.geometry('800x650+300+30')
root.configure(bg="#fff")
root.resizable(True,True)


def run_python_file(filename):
    subprocess.run(['python', filename])
    

#images
img_top = PhotoImage(file='images/FSTT.png')
Editimg = PhotoImage(file='images/edit_icon.png')
Calendrier = PhotoImage(file='images/Calendrier_icon.png')
Moduleimg = PhotoImage(file='images/Module_icon.png')
Profimg = PhotoImage(file='images/Teacher_icon.png')
Filiereimg = PhotoImage(file='images/Filiere_icon.png')
Notebookimg= PhotoImage(file='images/Notebook.png')



Label(root,image=img_top, bg="white").place(x=250,y=0)

Label(root,text='Bienvenue dans votre espace administartif', bg="white",fg='#ffb432',font=('Algerian', 20, 'bold')).place(x=100,y=150)


Label(root,text='Modifier',bg="white",fg='#2876dc',font=(' Arial Rounded MT Bold',16,'bold')).place(x=180,y=200)
Label(root,image=Editimg,bg='white').place(x=270,y=200)
Label(root,text='Emplois du temps',bg="white",fg='#2876dc',font=(' Arial Rounded MT Bold',16,'bold')).place(x=460,y=200)
Label(root,image=Calendrier,bg='white').place(x=650,y=200)


Label(root,image=Notebookimg,bg='white').place(x=70,y=240)

Button(root, width=15, height=2, pady=7, text='Modules', font=(' Arial Rounded MT Bold', 12, 'bold'),bg='#ffb432', fg='black',cursor='hand2', border=0,command=lambda: run_python_file('subjects.py')).place(x=195, y=307)
Button(root, width=15, height=2, pady=7, text='Profs', font=(' Arial Rounded MT Bold', 12, 'bold'),bg='#ffb432',borderwidth=2, fg='black',cursor='hand2', border=0,command=lambda: run_python_file('teachers.py')).place(x=195, y=507)
Label(root,image=Profimg,bg='#f5f5f5').place(x=95,y=500)
Label(root,image=Moduleimg,bg='#f5f5f5').place(x=95,y=300)


Label(root,image=Filiereimg,bg='#f5f5f5').place(x=450,y=300)
Label(root,image=Profimg,bg='#f5f5f5').place(x=450,y=500)
Button(root, width=15, height=2, pady=7, text='Filières', font=(' Arial Rounded MT Bold', 12, 'bold'),bg='#ffb432', fg='black',borderwidth=2,cursor='hand2', border=0,command=lambda: run_python_file('timetable_section.py')).place(x=535, y=307)
Button(root, width=15, height=2, pady=7, text='Profs', font=(' Arial Rounded MT Bold', 12, 'bold'),bg='#ffb432', fg='black',borderwidth=2,cursor='hand2', border=0,command=lambda: run_python_file('timetable_teacher.py')).place(x=535, y=507)



root.mainloop()