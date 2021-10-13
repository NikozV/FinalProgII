#LIBRERIAS
import tkinter #Importo modulo tkinter
from tkinter import *
from tkinter import messagebox
#import pymysql
import sqlite3 #Importo el modulo sqlite3

#CONEXION Y CREACION DE TABLA SI NO ESTA Y USUAIO ADMINISTRADOR
def conect():
    conexion = sqlite3.connect('../login/login.db')#Conexion sqlite
    c = conexion.cursor() #Creo cursor

    #Crear tabla si no existe
    c.execute("CREATE TABLE IF NOT EXISTS login("+
    "id INTEGER PRIMARY KEY  AUTOINCREMENT, "+ #creo tabla id
    "nombre VARCHAR(50) NOT NULL UNIQUE, "+ #creo tabla usuario
    "contrasena VARCHAR(50) NOT NULL CHECK (contrasena >=0)"+ #creo tabla cotraseña
    ")")
    conexion.commit() #Guardo cambios

    c.execute("SELECT nombre FROM login") #Veo el contenido de la tabla 

    filas = len(c.fetchall()) #recorro lista
    #print("Contiene ", filas, "usuarios")#Solo para control en terminal de lo que sucede 

    #CORROBORO SI LA TABLA ESTA VACIA
    if filas == 0:
        print("vacia")
        c.execute('INSERT INTO login (nombre,contrasena) VALUES (?,?)', ("adm", "1234")) #y si esta vacia creo el usuario adm
        conexion.commit()#Guardo los cambios
    else:
        print("Contiene", filas, "usuarios registrados")#Para pruebas en la terminal

    conexion.close()#Cierro la conexion
  
#CENTRAR
def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w / 2 - size[0] / 2
    y = h / 2 - size[1] / 2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))
#VALIDACION-ADM
def validacion():
    
    conexion = sqlite3.connect('../login/login.db')#Conexion sqlite
    c = conexion.cursor() #Creo cursor

    datos = (nombreusuario_verify.get(),contraseñausuario_verify.get())
     
    c.execute("SELECT * FROM login WHERE nombre = ? AND contrasena = ?", datos)

    if c.fetchall():
        if (nombreusuario_verify.get() == "adm"):
            #messagebox.showinfo(title="Login Correcto", message=("ADM "))
            pantallaS.destroy()
            import avanzado.py #importo programa para administrador
        else:
            messagebox.showerror(title="ERROR", message=(nombreusuario_verify.get() + " " + "NO es un usuario administrador"))
            #pantallaS.destroy()
            
            import usuario.py
        
    else:
        messagebox.showerror(title="Login inorrecto", message="Usuario o contraseña incorrecta")
        import usuario.py
        

    conexion.close()#cierro coneccion

pantallaS=Tk()
    
pantallaS.geometry("300x250")
pantallaS.title("Inicio de sesion")  
pantallaS.iconbitmap("img/loginuser.ico") #Icono .ico
pantallaS.configure(bg='ghost white')
center(pantallaS)#Uso esta funcion para centrar la pantalla

Label(pantallaS, text="Ingrese con el usuario administrador\npara poder entrar al modo avanzado", bg="orange", width="300" ).pack()
Label(pantallaS, text="", bg='ghost white').pack()

center(pantallaS)#Uso esta funcion para centrar la pantalla
pantallaS.resizable(0,0)#remuevo el botón maximizar

global nombreusuario_verify
global contraseñausuario_verify
nombreusuario_verify = StringVar()
contraseñausuario_verify = StringVar()

global nombre_usuario_entry
global contraseña_usuario_entry

Label(pantallaS, text="Usuario", bg='ghost white').pack()
nombre_usuario_entry = Entry(pantallaS, textvariable=nombreusuario_verify)
nombre_usuario_entry.pack()
Label(pantallaS, bg='ghost white').pack()

Label(pantallaS, text="Contraseña", bg='ghost white').pack()
contraseña_usuario_entry = Entry(pantallaS, show="*", textvariable=contraseñausuario_verify) #Con show="*" hacemos que no se vea la contraseña
contraseña_usuario_entry.pack()
Label(pantallaS, bg='ghost white').pack()

Button(pantallaS, cursor="hand2", bd=1, bg ="white smoke", text="Iniciar Sesion", command = validacion).pack()

pantallaS.mainloop()
