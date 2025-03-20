from tkinter import *
from tkinter import messagebox
import subprocess


root=Tk()
root.title('Login')
root.geometry('925x500+250+100')
root.configure(bg="#fff")
root.resizable(True,True)


img_top = PhotoImage(file='images/FSTT.png')
Label(root,image=img_top, bg="white").place(x=300,y=0)

img = PhotoImage(file='images/login.png')
Label(root,image=img,bg='white').place(x=50,y=130)

frame=Frame(root,width=350,height=350,bg="white")
frame.place(x=480,y=150)

heading=Label(frame,text='Sign in',fg='#57a1f8',bg='white',font=('Microsoft Yahei UI LIGHT',23,'bold'))
heading.place(x=100,y=5)


def signin(login_window):
    username=user.get()
    password=code.get()

    if username=='admin' and password=='admin':
       login_window.destroy() 
       subprocess.run(['python', 'admin_screen.py'])
    else:
        messagebox.showerror('Erreur', 'Nom d\'utilisateur ou mot de passe incorrect')

#Username_part
def on_enter(e):
    user.delete(0,'end')
def on_leave(e):
    name=user.get()
    if name=='':
        user.insert(0,'Username')

user=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI LIGHT',11))
user.place(x=30,y=80)
user.insert(0,'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)


#Password_part
def on_enter(e):
    code.delete(0,'end')
def on_leave(e):
    name=code.get()
    if name=='':
        code.insert(0,'Password')

code=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI LIGHT',11))
code.place(x=30,y=150)
code.insert(0,'Password')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>',on_leave)

Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)

#Submit_part
Button(frame, width=39, pady=7, text='Sign in', bg='#57a1f8', fg='white',cursor='hand2', border=0, command=lambda: signin(root)).place(x=35, y=204)

root.mainloop()