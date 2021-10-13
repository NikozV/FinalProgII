from tkinter import *
from tkinter import messagebox
import sqlite3

def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth() #obtengo inf. del ancho del la resol. del monintor
    h = toplevel.winfo_screenheight() #obtengo inf. del altura del la resol. del monintor
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w / 2 - size[0] / 2
    y = h / 2 - size[1] / 2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

#CONEXION A LA BD
conexion = sqlite3.connect('../login/login.db')

ventanaM = Tk()
ventanaM.title("Administrador")
ventanaM.geometry("400x500") #Dimen. ventana administrador
try:
    ventanaM.iconbitmap("img/loginuser.ico") #Icono .ico
except:
    pass
ventanaM.config(bg='ghost white')
center(ventanaM) #Uso esta funcion para acomodar la pantalla
ventanaM.resizable(0,0)#remuevo el botón maximizar

#Etiqueta PANEL ADMINISTRADOR
Label(ventanaM, text="Panel de control de Usuario", bg="orange", width="300", font=("calibri", 13)).pack()

#Label(ventana, text="", bg='ghost white').pack()

global buscar #Creo variable global

def listado():
    tabla = conexion.cursor()
    tabla.execute("SELECT * FROM login ORDER BY id")
    conexion.commit()
    datos = tabla.fetchall()
    tabla.close
    lista.delete(0,END)
    for dato in datos:
        alumno = str(dato[1])
        lista.insert(END,alumno)

lista = Listbox(ventanaM,width = 35,heigh=20,font=("Arial",12))#Lista
lista.place(x=40,y=40) #ubicacion boton lista
botonListar = Button(ventanaM,cursor="hand2", bd=1, bg ="white smoke", width=10, text="Ver Usuarios",font=("calibri", 11),command=listado)#boton Ver Usuarios
botonListar.place(x=50,y=450) #ubicacion boton Ver Usuarios

def avanzado():
    ventanaM.destroy()
    import seguridad.py
botonListar = Button(ventanaM,cursor="hand2", bd=1, bg ="white smoke", width=10, text="Avanzado",font=("calibri", 11), command=avanzado)#boton Avanzado
botonListar.place(x=220,y=450) #ubicacion boton Avanzado



ventanaM.mainloop()