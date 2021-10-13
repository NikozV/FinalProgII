#BIBLIOTECAS
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import *
import sqlite3
import tkinter as tk


########## INSUMOS - STOCK##########
def vInsumos(): 
    insumos=tk.Toplevel()
    insumos.geometry("750x400") 
    insumos.title("Insumos")
    insumos.config(bg='ghost white')
    insumos.resizable(0,0)#remuevo el botón maximizar
    
    miId=StringVar()
    miNombre=StringVar()
    miCantidad=StringVar()
    miPrecio=StringVar()

    #CONEXION A BD
    def conexionBBDD():
        miConexion=sqlite3.connect('insumos.db')
        miCursor=miConexion.cursor()

        #CREO LAS TABLAS insumos
        try:
            miCursor.execute('''
                CREATE TABLE insumos (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NOMBRE VARCHAR(50) NOT NULL,
                CANTIDAD INT NOT NULL,
                PRECIO REAL NOT NULL)
                ''')
            messagebox.showinfo("CONEXION"," Base de datos creada correctamente")
        except:
            messagebox.showinfo("CONEXION"," Conexion exitosa con la base de datos")
        
    #ELIMINAR BD
    def eliminarBBDD():
        miConexion=sqlite3.connect("base.db")
        miCursor=miConexion.cursor()
        if messagebox.askyesno(message="¿Los datos se perderan definitivamente, desea continuar?", title="ADVERTENCIA"):
            miCursor.execute("DROP TABLE insumos")
        else:
            pass
        limpiarCampos()
        mostrar() 

    #SALIR DE LA APLICACION
    def salirAplicacion():
        valor=messagebox.askquestion("Salir", "¿Esta seguro que quiere salir?")
        if valor == "yes":
            insumos.destroy()

    #LIMPIAR LOS CAMPOS
    def limpiarCampos():
        miId.set("")
        miNombre.set("")
        miCantidad.set("")
        miPrecio.set("")

    #VISTA - CABECERAS DE LAS COLUMNAS
    listaInsumos=Frame(insumos)
    listaInsumos.pack(pady=30)
    tree=ttk.Treeview(listaInsumos, height=10, columns=('#0','#1','#2')) #Indica que va a tener 3 columnas para los valores
    tree.pack(side=tk.TOP)

    tree.column('#0', width=100)
    tree.heading('#0', text="ID", anchor=CENTER)
    tree.heading('#1', text="Insumos/Descartables", anchor=CENTER)
    tree.heading('#2', text="Stock", anchor=CENTER)
    tree.column('#3', width=100)
    tree.heading('#3', text="Precio", anchor=CENTER)

    ###METODOS###
    #CREAR
    def crear():
        miConexion=sqlite3.connect("insumos.db")
        miCursor=miConexion.cursor()
    #HACER VALIDACIONES
        try:
            datos=miNombre.get(),miCantidad.get(),miPrecio.get()
            miCursor.execute("INSERT INTO insumos VALUES(NULL,?,?,?)",(datos))
            miConexion.commit()
        except:
            messagebox.showwarning("ADVERTENCIA","Ocurrio un error, verifique conexión con BBDD")
            pass
        limpiarCampos()
        mostrar()

    #MOSTRAR
    def mostrar():
        miConexion=sqlite3.connect("insumos.db")
        miCursor=miConexion.cursor()
        registros = tree.get_children()
        for elemento in registros:
            tree.delete(elemento)

        try:
            miCursor.execute("SELECT * FROM insumos")
            for row in miCursor:
                tree.insert("",0,text=row[0], values=(row[1],row[2],row[3]))
        except:
            pass

    #SELECCION CLICKEANDO EN LISTA
    def seleccionarUsandoClick(event):
        item=tree.identify('item', event.x, event.y)
        miId.set(tree.item(item, "text"))
        miNombre.set(tree.item(item, "values")[0])
        miCantidad.set(tree.item(item, "values")[1])
        miPrecio.set(tree.item(item, "values")[2])

    tree.bind("<Double-1>", seleccionarUsandoClick) #La ligo a la tabla

    #MODIFICAR - ACTUALIZAR
    def actualizar():
        miConexion=sqlite3.connect("insumos.db")
        miCursor=miConexion.cursor()
        try:
            datos=miNombre.get(),miCantidad.get(),miPrecio.get()
            miCursor.execute("UPDATE insumos SET NOMBRE=?, CANTIDAD=?, PRECIO=? WHERE ID="+ miId.get(),(datos))
            miConexion.commit()
        except:
            messagebox.showwarning("ADVERTENCIA","Ocurrio un error, verifique conexión con BBDD")
            pass
        limpiarCampos()
        mostrar()

    #BORRAR - ELIMINAR
    def borrar():
        miConexion=sqlite3.connect("insumos.db")
        miCursor=miConexion.cursor()
        try:  
            if messagebox.askyesno(message="¿Realmente desea eliminar el registro?", title="ADVERTENCIA"):  
                miCursor.execute("DELETE FROM insumos WHERE ID="+ miId.get())
                miConexion.commit()
        except:
            messagebox.showwarning("ADVERTENCIA","Ocurrio un error, verifique conexión con BBDD")
            pass
        limpiarCampos()   
        mostrar()

    ###VISTAS - WIDGETS###

    #MENU
    menubar=Menu(insumos)
    menubasedat=Menu(menubar, tearoff=0)
    menubasedat.add_command(label="Crear/Conectar Base de Datos", command=conexionBBDD)
    menubasedat.add_command(label="Eliminar Base de Datos", command=eliminarBBDD)
    menubasedat.add_command(label="Salir", command=salirAplicacion)
    menubar.add_cascade(label="Inicio", menu=menubasedat)

    ayudamenu=Menu(menubar, tearoff=0)
    ayudamenu.add_command(label="Recetear Campos", command=limpiarCampos)
    ayudamenu.add_command(label="Acerca", command=mensaje)
    menubar.add_cascade(label="Ayuda", menu=ayudamenu)

    #ETIQUECTAS Y CAJAS DE TEXTO
    e1=Entry(insumos, textvariable=miId) #No se ve, recolecta los valores del registro

    l2=Label(insumos, text="Insumos/Descartables")
    l2.place(x=50,y=260)
    e2=Entry(insumos, textvariable=miNombre, width=50)
    e2.place(x=190, y=260)

    l3=Label(insumos, text="Cantidad")
    l3.place(x=50,y=300)
    e3=Entry(insumos, textvariable=miCantidad)
    e3.place(x=130, y=300)

    l4=Label(insumos, text="Precio")
    l4.place(x=280,y=300)
    e4=Entry(insumos, textvariable=miPrecio, width=10)
    e4.place(x=320, y=300)

    l5=Label(insumos, text="AR$")
    l5.place(x=390,y=300)

    #BOTONES
    b1=Button(insumos, text="Crear Registro", command=crear)
    b1.place(x=50, y=350)

    b2=Button(insumos, text="Modificar Registro", command=actualizar)
    b2.place(x=180, y=350)

    b3=Button(insumos, text="Mosrtar Lista", command=mostrar)
    b3.place(x=320, y=350)

    b4=Button(insumos, text="Eliminar Registro", command=borrar)
    b4.place(x=450, y=350)

    #MOSTRAR MENU
    insumos.config(menu=menubar)
    center(insumos)

########## CLIENTES ##########
def vClientes(): 
    pass

########## VENTAS ##########
def vVentas(): 
    ventas=tk.Toplevel()
    ventas.geometry("600x400") 
    ventas.title("Ventas")
    ventas.config(bg='ghost white')
    ventas.resizable(0,0)#remuevo el botón maximizar

    #VISTA - CABECERAS DE LAS COLUMNAS
    listaStock=Frame(ventas)
    listaStock.pack(pady=30)

    tree=ttk.Treeview(listaStock, height=10, columns=('#0','#1','#2')) #Indica que va a tener 3 columnas para los valores
    tree.pack() #ubicacion de la lista

    tree.column('#0', width=50)
    tree.heading('#0', text="ID", anchor=CENTER)
    tree.heading('#1', text="Insumos", anchor=CENTER)
    tree.heading('#2', text="Marca", anchor=CENTER)
    tree.column('#3', width=100)
    tree.heading('#3', text="Costo", anchor=CENTER)

    btVentas=Button(ventas, text="Ventas")
    btVentas.place(x=50, y=10)

    center(ventas)

########## COMPRAS ##########
def vCompras(): 
    compras=tk.Toplevel()
    compras.geometry("600x400") 
    compras.title("Compras")
    compras.config(bg='ghost white')
    compras.resizable(0,0)#remuevo el botón maximizar

    center(compras)

########## PROVEEDORES ##########
def vProveedores(): 
    proveedores=tk.Toplevel()
    proveedores.geometry("600x400") 
    proveedores.title("Compras")
    proveedores.config(bg='ghost white')
    proveedores.resizable(0,0)#remuevo el botón maximizar

    center(proveedores)

#SALIR DE LA APLICACION
def salirAplicacion():
    valor=messagebox.askquestion("Salir", "¿Esta seguro que quiere salir?")
    if valor == "yes":
        root.destroy()    

#CENTRAR
def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w / 2 - size[0] / 2
    y = h / 2 - size[1] / 2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

#MENSAJE DE INFO DE LA APLICACION
def mensaje():
    acerca='''
    Aplicación CRUD
    Version 1.0
    Tecnología Python Tkinter
    '''
    messagebox.showinfo(title="Información", message=acerca)

#INTERFAZ GRAFICA
root=Tk()
root.title("Ventana principal")
root.geometry("1000x600")
##PONER ICONO################
center(root)#Uso esta funcion para centrar la pantalla
root.config(bg='#040170')
root.resizable(0,0)#remuevo el botón maximizar

#BOTONES
btInsumos=Button(root, text="Insumos", command= vInsumos)
btClientes=Button(root, text="Clientes", command=vClientes)
btVentas=Button(root, text="Ventas", command= vVentas)
btCompras=Button(root, text="Compras", command= vCompras)
btProveedores=Button(root, text="Proveedores", command=vProveedores)
btSalir=Button(root, text="Salir", command= salirAplicacion)

btInsumos.place(x=10, y=20, width=80, height=80)
btClientes.place(x=10, y=100, width=80, height=80)
btVentas.place(x=10, y=180, width=80, height=80)
btCompras.place(x=10, y=260, width=80, height=80)
btProveedores.place(x=10, y=340, width=80, height=80)
btSalir.place(x=10, y=420, width=80, height=80)

def menu():
    #MENU
    menubar=Menu(root)

    menubasedat=Menu(menubar, tearoff=0)
    menubasedat.add_command(label="Crear/Conectar Base de Datos")
    menubasedat.add_command(label="Eliminar Base de Datos")
    menubasedat.add_command(label="Salir", command= salirAplicacion)
    menubar.add_cascade(label="Inicio", menu=menubasedat)

    ayudamenu=Menu(menubar, tearoff=0)
    #ayudamenu.add_command(label="Recetear Campos")
    ayudamenu.add_command(label="Acerca", command=mensaje)
    menubar.add_cascade(label="Ayuda", menu=ayudamenu)

    #MOSTRAR MENU
    root.config(menu=menubar)
menu()
root.mainloop()