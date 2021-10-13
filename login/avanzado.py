from tkinter import *
from tkinter import messagebox
import sqlite3

def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w / 2 - size[0] / 2
    y = h / 2 - size[1] / 2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

#CONEXION A LA BD
conexion = sqlite3.connect('../login/login.db')

ventanaA = Tk()
ventanaA.title("Administrador avanzado")
ventanaA.geometry("400x500") #Dimen. ventana administrador
ventanaA.config(bg='ghost white')
try:
    ventanaA.iconbitmap("img/loginuser.ico") #Icono .ico
except:
    pass
center(ventanaA) #Uso esta funcion para acomodar la pantalla
ventanaA.resizable(0,0)#remuevo el botón maximizar

labelId = Label(ventanaA,text="ID del usuario:",font=("calibri", 11),bg='ghost white')
labelId.place(x=30,y=100) #ubicacion label id
labelNombre= Label(ventanaA,text="Usuario:",font=("calibri", 11),bg='ghost white')
labelNombre.place(x=30,y=150) #ubicacion label nombre
labelContrasena = Label(ventanaA,text="Contraseña:",font=("calibri", 11),bg='ghost white')
labelContrasena.place(x=30,y=200) #ubicacion label contrasena

id = Entry(ventanaA,font=("calibri", 11),state="readonly") #Entry id
id.place(x=150,y=100) #ubicacion entry id
nombre = Entry(ventanaA,font=("calibri", 11)) #Entry nombre
nombre.place(x=150,y=150) #ubicacion entry nombre
contrasena = Entry(ventanaA,font=("calibri", 11)) #Entry contrasena
contrasena.place(x=150,y=200) #ubicacion entry contrasena

#######
#Etiqueta PANEL AVANZADO
Label(ventanaA, text="Panel avanzado de Administrador", bg="orange", width="300", font=("calibri", 13)).pack()

def busqueda():
    buscarId = (buscar.get(),)
    tabla = conexion.cursor()
    tabla.execute("SELECT * FROM login WHERE id = ?",buscarId)
    conexion.commit()
    datos = tabla.fetchall()
    tabla.close
    
    if(len(datos)>0):
        id.config(state="normal")
        for dato in datos:
            id.delete(0,END)
            id.insert(END,dato[0])
            nombre.delete(0,END)
            nombre.insert(END,dato[1])
            contrasena.delete(0,END)
            contrasena.insert(END,dato[2])
            
        id.config(state="readonly")
        
        botonModificar.config(state="normal")
        
    else:
        pass
     
buscar = Entry(ventanaA,width=10,font=("calibri", 11))
buscar.place(x=30,y=50) #Entry Buscar
botonBuscar = Button(ventanaA,cursor="hand2", bd=1, bg ="white smoke", width=10,text="Buscar por ID",font=("calibri", 11),command=busqueda) #Boton Buscar po ID
botonBuscar.place(x=120,y=50) #ubicacion boton Buscar por id

def guardar():
    datos = (nombre.get(),contrasena.get())
    tabla = conexion.cursor()
    tabla.execute("INSERT INTO login(nombre,contrasena) VALUES(?,?)",datos)
    conexion.commit()
    tabla.close
    messagebox.showinfo(title="Guardado", message=("El usuario se guardo\n   correctamente "))
    nombre.delete(0,END)
    contrasena.delete(0,END)

botonGuardar = Button(ventanaA,cursor="hand2", bd=1, bg ="white smoke", width=10,text="Guardar",font=("calibri", 11),command=guardar)
botonGuardar.place(x=30,y=240)

def modificar():
    datos = (nombre.get(),contrasena.get(),id.get())
    tabla = conexion.cursor()
    tabla.execute("UPDATE login SET nombre=?,contrasena=? WHERE id = ?",datos)
    conexion.commit()
    tabla.close
    messagebox.showinfo(title="Modificado", message=("El usuario se modifico\n   correctamente "))
    id.delete(0,END)
    nombre.delete(0,END)
    contrasena.delete(0,END)
botonModificar= Button(ventanaA,cursor="hand2", bd=1, bg ="white smoke", width=10, state="disabled", text="Modificar",font=("calibri", 11),command=modificar)
botonModificar.place(x=140,y=240)

def eliminar():
    
    eliminarId = (id.get(),)
    tabla = conexion.cursor()
    tabla.execute("DELETE FROM login WHERE id = ?",eliminarId)
    conexion.commit()
    tabla.close
    messagebox.showinfo(title="Eliminado", message=("El usuario fue eliminado\n   correctamente "))
    id.delete(0,END)
    nombre.delete(0,END)
    contrasena.delete(0,END)
botonEliminar= Button(ventanaA,cursor="hand2", bd=1, bg ="white smoke", width=10,text="Eliminar",font=("calibri", 11),command=eliminar)
botonEliminar.place(x=250,y=240)

def listado():
    tabla = conexion.cursor()
    tabla.execute("SELECT * FROM login ORDER BY id")
    conexion.commit()
    datos = tabla.fetchall()
    tabla.close
    lista.delete(0,END)
    for dato in datos:
        alumno = str(dato[0])+" "+str(dato[1])+" "+str(dato[2])
        lista.insert(END,alumno)

lista = Listbox(ventanaA,width = 35,heigh=8,font=("Arial",12))#Lista
lista.place(x=30,y=280) #ubicacion boton lista
botonListar = Button(ventanaA,cursor="hand2", bd=1, bg ="white smoke", width=10, text="Ver Usuarios",font=("calibri", 11),command=listado)#boton Ver Usuarios
botonListar.place(x=30,y=450) #ubicacion boton Ver Usuarios


ventanaA.mainloop()