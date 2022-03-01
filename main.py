#BIBLIOTECAS
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import *
import sqlite3
import tkinter as tk
import os

listaArticulos = []
clientes = []


#CONEXION A BD
def conexionBBDD():
    miConexion=sqlite3.connect('insumos.db')
    miCursor=miConexion.cursor()
    ventConexion=sqlite3.connect('venta.db')
    tabla = ventConexion.cursor()
    conexion=sqlite3.connect('clientes.db')
    cursorCliente = conexion.cursor()
    
    try:
        #CREO LAS TABLAS insumos
        miCursor.execute('''
            CREATE TABLE insumos (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NOMBRE VARCHAR(50) NOT NULL,
            CANTIDAD INT NOT NULL,
            PRECIO REAL NOT NULL)
            ''')
        #CREO LAS TABLAS venta
        tabla.execute('''
            CREATE TABLE venta (
            nfactura INTEGER PRIMARY KEY AUTOINCREMENT,
            subtotal REAL,
            iva INT REAL,
            total REAL)
            ''')
        #CREO LAS TABLAS venta
        tabla.execute('''
            CREATE TABLE articulosVendidos (
            articuloVendido	INTEGER PRIMARY KEY AUTOINCREMEN,
            nfactura INTEGER,
            codigo	INTEGER,
            detalle	TEXT,
            cantidad REAL,
            subtotal REAL,
            iva	REAL,
            total REAL)                
        ''')
        #CREO LAS TABLAS clientes
        cursorCliente.execute('''
            CREATE TABLE clientes (
            dni INTEGER PRIMARY KEY,
            nombre VARCHAR(50) NOT NULL,
            apellido VARCHAR(50) NOT NULL)
            ''')
        
        messagebox.showinfo("CONEXION"," Base de datos creada correctamente")
    except:
        #messagebox.showinfo("CONEXION"," Conexion exitosa con la base de datos")
        pass

########## INSUMOS - STOCK##########
def vInsumos(): 
    insumos=tk.Toplevel()
    insumos.geometry("750x400") 
    insumos.title("Insumos")
    insumos.iconbitmap("iconoInsumos.ico")
    insumos.config(bg='ghost white')
    insumos.resizable(0,0)#remuevo el botón maximizar
    
    miId=StringVar()
    miNombre=StringVar()
    miCantidad=StringVar()
    miPrecio=StringVar()
         
    """ #ELIMINAR BD
    def eliminarBBDD():
        miConexion=sqlite3.connect("base.db")
        miCursor=miConexion.cursor()
        if messagebox.askyesno(message="¿Los datos se perderan definitivamente, desea continuar?", title="ADVERTENCIA"):
            miCursor.execute("DROP TABLE insumos")
        else:
            pass
        limpiarCampos()
        mostrar()  """

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
    #menubasedat.add_command(label="Eliminar Base de Datos", command=eliminarBBDD)
    menubasedat.add_command(label="Salir", command=salirAplicacion)
    menubar.add_cascade(label="Inicio", menu=menubasedat)

    ayudamenu=Menu(menubar, tearoff=0)
    #ayudamenu.add_command(label="Recetear Campos", command=limpiarCampos)
    ayudamenu.add_command(label="Acerca", command=mensaje)
    menubar.add_cascade(label="Ayuda", menu=ayudamenu)

    #ETIQUEtAS Y CAJAS DE TEXTO
    e1=Entry(insumos, textvariable=miId) #No se ve, recolecta los valores del registro

    l2=Label(insumos, text="Insumos/Descartables")
    l2.place(x=80,y=270)
    e2=Entry(insumos, textvariable=miNombre, width=50)
    e2.place(x=220, y=270)

    l3=Label(insumos, text="Cantidad")
    l3.place(x=100,y=310)
    e3=Entry(insumos, textvariable=miCantidad)
    e3.place(x=200, y=310)

    l4=Label(insumos, text="Precio")
    l4.place(x=350,y=310)
    e4=Entry(insumos, textvariable=miPrecio, width=10)
    e4.place(x=400, y=310)

    l5=Label(insumos, text="AR$")
    l5.place(x=470,y=310)

    #BOTONES
    b1=Button(insumos, text="Crear Registro", command=crear)
    b1.place(x=80, y=350)

    b2=Button(insumos, text="Modificar Registro", command=actualizar)
    b2.place(x=210, y=350)

    b3=Button(insumos, text="Mostrar Lista", command=mostrar)
    b3.place(x=350, y=350)

    b4=Button(insumos, text="Eliminar Registro", command=borrar)
    b4.place(x=480, y=350)

    #MOSTRAR MENU
    insumos.config(menu=menubar)
    center(insumos)

########## COMPRAS ##########
def vCompras(): 
    compras=tk.Toplevel()
    compras.geometry("750x400") 
    compras.title("Compras de Insumos y Descartables")
    compras.config(bg='ghost white')
    compras.resizable(0,0)#remuevo el botón maximizar
    compras.iconbitmap("iconoCompras.ico")
    
    miId=StringVar()
    miNombre=StringVar()
    miCantidad=StringVar()
    miIngreso=StringVar()
    miPrecio=StringVar()

    """ #ELIMINAR BD
    def eliminarBBDD():
        miConexion=sqlite3.connect("base.db")
        miCursor=miConexion.cursor()
        if messagebox.askyesno(message="¿Los datos se perderan definitivamente, desea continuar?", title="ADVERTENCIA"):
            miCursor.execute("DROP TABLE insumos")
        else:
            pass
        limpiarCampos()
        mostrar()  """

    #LIMPIAR LOS CAMPOS
    def limpiarCampos():
        miId.set("")
        miNombre.set("")
        miCantidad.set("")
        miPrecio.set("")

    #VISTA - CABECERAS DE LAS COLUMNAS
    listaInsumos=Frame(compras)
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
            datos=miNombre.get(),miIngreso.get(),miPrecio.get()
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

    #MODIFICAR - ACTUALIZAR - AGREGAR STOCK
    def actualizar():
        cantidad = int(miCantidad.get())
        ingreso = int(miIngreso.get())
        
        nuevoIngreso =  cantidad + ingreso 
        
        miConexion=sqlite3.connect("insumos.db")
        miCursor=miConexion.cursor()
        try:
            datos=miNombre.get(),nuevoIngreso,miPrecio.get()
            miCursor.execute("UPDATE insumos SET NOMBRE=?, CANTIDAD=?, PRECIO=? WHERE ID="+ miId.get(),(datos))
            miConexion.commit()
        except:
            pass
            """ datos=miNombre.get(),miIngreso.get(),miPrecio.get()
            miCursor.execute("UPDATE insumos SET NOMBRE=?, CANTIDAD=?, PRECIO=? WHERE ID="+ miId.get(),(datos))
            miConexion.commit() """
            
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
    menubar=Menu(compras)
    menubasedat=Menu(menubar, tearoff=0)
    menubasedat.add_command(label="Crear/Conectar Base de Datos", command=conexionBBDD)
    #menubasedat.add_command(label="Eliminar Base de Datos", command=eliminarBBDD)
    menubasedat.add_command(label="Salir", command=salirAplicacion)
    menubar.add_cascade(label="Inicio", menu=menubasedat)

    ayudamenu=Menu(menubar, tearoff=0)
    #ayudamenu.add_command(label="Recetear Campos", command=limpiarCampos)
    ayudamenu.add_command(label="Acerca", command=mensaje)
    menubar.add_cascade(label="Ayuda", menu=ayudamenu)

    #ETIQUEtAS Y CAJAS DE TEXTO
    e1=Entry(compras, textvariable=miId) #No se ve, recolecta los valores del registro

    l2=Label(compras, text="Insumos/Descartables")
    l2.place(x=80,y=270)
    e2=Entry(compras, textvariable=miNombre, width=50)
    e2.place(x=220, y=270)

    l3=Label(compras, text="Cantidad a ingresar: ")
    l3.place(x=80,y=310)
    e3=Entry(compras, textvariable=miIngreso)
    e3.place(x=220, y=310)
    
    #l5=Label(compras, text="Cantidad a ingresar: ")
    #l5.place(x=50,y=300)
    e5=Entry(compras, textvariable=miCantidad)
    #e5.place(x=130, y=300)
    
    l4=Label(compras, text="Precio")
    l4.place(x=350,y=310)
    e4=Entry(compras, textvariable=miPrecio, width=10)
    e4.place(x=400, y=310)

    l5=Label(compras, text="AR$")
    l5.place(x=470,y=310)

    #BOTONES
    b1=Button(compras, text="Crear", command=crear)
    b1.place(x=80, y=350)

    b2=Button(compras, text="Agregar", command=actualizar)
    b2.place(x=210, y=350)

    b3=Button(compras, text="Mostrar Lista", command=mostrar)
    b3.place(x=350, y=350)

    b4=Button(compras, text="Eliminar", command=borrar)
    b4.place(x=480, y=350)

    #MOSTRAR MENU
    compras.config(menu=menubar)
    center(compras)

########## CLIENTES ##########
def vClientes(): 
    clientes=tk.Toplevel()
    clientes.geometry("750x400") 
    clientes.title("Clientes")
    clientes.config(bg='ghost white')
    clientes.resizable(0,0)#remuevo el botón maximizar
    clientes.iconbitmap("iconoClientes.ico")
    
    miDni=StringVar()
    miNombre=StringVar()
    miApellido=StringVar() #cantidad
    #miPrecio=StringVar() #precio
         

    #SALIR DE LA APLICACION
    def salirAplicacion():
        valor=messagebox.askquestion("Salir", "¿Esta seguro que quiere salir?")
        if valor == "yes":
            clientes.destroy()

    #LIMPIAR LOS CAMPOS
    def limpiarCampos():
        miDni.set("")
        miNombre.set("")
        miApellido.set("")
        #miPrecio.set("")

    #VISTA - CABECERAS DE LAS COLUMNAS
    listaInsumos=Frame(clientes)
    listaInsumos.pack(pady=30)
    tree=ttk.Treeview(listaInsumos, height=10, columns=('#0','#1','#2')) #Indica que va a tener 3 columnas para los valores
    tree.pack(side=tk.TOP)

    tree.column('#0', width=100)
    tree.heading('#0', text="DNI", anchor=CENTER)
    tree.heading('#1', text="Nombre", anchor=CENTER)
    tree.heading('#2', text="Apellido", anchor=CENTER)


    ###METODOS###
    #CREAR
    def crear():
        conexion=sqlite3.connect('clientes.db')
        miCursor=conexion.cursor()
            #HACER VALIDACIONES
        try:
            datos=miDni.get() ,miNombre.get(),miApellido.get()
            miCursor.execute("INSERT INTO clientes VALUES(?,?,?)",(datos))
            conexion.commit()
        except:
            messagebox.showwarning("ADVERTENCIA","Ocurrio un error, verifique conexión con BBDD")
            pass
        limpiarCampos()
        mostrar()

    #MOSTRAR
    def mostrar():
        conexion=sqlite3.connect('clientes.db')
        miCursor=conexion.cursor()
        registros = tree.get_children()
        for elemento in registros:
            tree.delete(elemento)

        try:
            miCursor.execute("SELECT * FROM clientes")
            for row in miCursor:
                tree.insert("",0,text=row[0], values=(row[1],row[2]))
        except:
            pass

    #SELECCION CLICKEANDO EN LISTA
    def seleccionarUsandoClick(event):
        item=tree.identify('item', event.x, event.y)
        miDni.set(tree.item(item, "text"))
        miNombre.set(tree.item(item, "values")[0])
        miApellido.set(tree.item(item, "values")[1])
        #miPrecio.set(tree.item(item, "values")[2])

    tree.bind("<Double-1>", seleccionarUsandoClick) #La ligo a la tabla

    #MODIFICAR - ACTUALIZAR
    def actualizar():
        conexion=sqlite3.connect('clientes.db')
        miCursor=conexion.cursor()
        try:
            datos= str(miDni.get()) ,miNombre.get(),miApellido.get()
            miCursor.execute("UPDATE clientes SET dni=?, nombre=?, apellido=? WHERE dni="+ miDni.get(),(datos))
            conexion.commit()
        except:
            messagebox.showwarning("ADVERTENCIA","Ocurrio un error, verifique conexión con BBDD")
            pass
        limpiarCampos()
        mostrar()

    #BORRAR - ELIMINAR
    def borrar():
        conexion=sqlite3.connect('clientes.db')
        miCursor=conexion.cursor()
        try:  
            if messagebox.askyesno(message="¿Realmente desea eliminar el registro?", title="ADVERTENCIA"):  
                miCursor.execute("DELETE FROM clientes WHERE dni="+ miDni.get())
                conexion.commit()
        except:
            messagebox.showwarning("ADVERTENCIA","Ocurrio un error, verifique conexión con BBDD")
            pass
        limpiarCampos()   
        mostrar()

    ###VISTAS - WIDGETS###

    #MENU
    menubar=Menu(clientes)
    menubasedat=Menu(menubar, tearoff=0)
    menubasedat.add_command(label="Crear/Conectar Base de Datos", command=conexionBBDD)
    #menubasedat.add_command(label="Eliminar Base de Datos", command=eliminarBBDD)
    menubasedat.add_command(label="Salir", command=salirAplicacion)
    menubar.add_cascade(label="Inicio", menu=menubasedat)

    ayudamenu=Menu(menubar, tearoff=0)
    #ayudamenu.add_command(label="Recetear Campos", command=limpiarCampos)
    ayudamenu.add_command(label="Acerca", command=mensaje)
    menubar.add_cascade(label="Ayuda", menu=ayudamenu)

    #ETIQUEtAS Y CAJAS DE TEXTO
    e1=Entry(clientes, textvariable=miDni) #No se ve, recolecta los valores del registro

    l2=Label(clientes, text="Nombre: ")
    l2.place(x=110,y=270)
    e2=Entry(clientes, textvariable=miNombre, width=30)
    e2.place(x=190, y=270)

    l3=Label(clientes, text="Apellido: ")
    l3.place(x=110,y=310)
    e3=Entry(clientes, textvariable=miApellido)
    e3.place(x=190, y=310)

    l4=Label(clientes, text="DNI: ")
    l4.place(x=370,y=310)
    e4=Entry(clientes, textvariable=miDni, width=30)
    e4.place(x=420, y=310) 
    """
    l5=Label(insumos, text="AR$")
    l5.place(x=390,y=300)"""

    #BOTONES
    b1=Button(clientes, text="Crear Cliente", command=crear)
    b1.place(x=50, y=350)

    b2=Button(clientes, text="Modificar Cliente", command=actualizar)
    b2.place(x=180, y=350)

    b3=Button(clientes, text="Mostrar Clientes", command=mostrar)
    b3.place(x=320, y=350)

    b4=Button(clientes, text="Eliminar Cliente", command=borrar)
    b4.place(x=450, y=350)

    #MOSTRAR MENU
    clientes.config(menu=menubar)
    center(clientes)

########## VENTAS VENT. PRINCIPAL ##########
def ventas(): 

    miId=StringVar()
    miNombre=StringVar()
    miCantidad=StringVar()
    miPrecio=StringVar()
        
    #VISTA - CABECERAS DE LAS COLUMNAS STOCK
    listaInsumos=Frame(root)
    listaInsumos.place(x=130,y=65)
    tree=ttk.Treeview(listaInsumos, height=27, columns=('#0','#1','#2')) #Indica que va a tener 3 columnas para los valores
    tree.pack(side=tk.TOP)

    tree.column('#0', width=100)
    tree.heading('#0', text="ID", anchor=CENTER)
    tree.heading('#1', text="Insumos/Descartables", anchor=CENTER)
    tree.heading('#2', text="Stock", anchor=CENTER)
    tree.column('#3', width=100)
    tree.heading('#3', text="Precio", anchor=CENTER)
    
    #VISTA - CABECERAS DE LAS COLUMNAS VENTA
    
    vista = ttk.Treeview(root, height=17)
    vista.place(x=800,y=65)


    vista["columns"]=("1","2","3","4")

    vista.column("#0", width=80, stretch=NO)
    vista.column("1", width=100, stretch=NO)
    vista.column("2", width=100, stretch=NO)
    vista.column("3", width=100, stretch=NO)
    vista.column("4", width=100, stretch=NO)

    vista.heading("#0",text="ID",anchor=CENTER)
    vista.heading("1", text="Insumos/Descartables", anchor=CENTER)
    vista.heading("2", text="Cantidad",anchor=CENTER)
    vista.heading("3", text="Subtotal",anchor=CENTER)
    vista.heading("4", text="Total",anchor=CENTER)
    
    ###METODOS###

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

        #LIMPIAR LOS CAMPOS
    
    #AGREGAR A LA COMPRA
    def agregar():
        try:
            subtotal = round(int(entryCantidad.get())*float(entryPrecio.get()),2)
            iva= round(subtotal* 0.21 , 2)
            total= round(subtotal + iva, 2)
            vista.insert("",END,text=entryCodigo.get(),values=(entryInsumo.get(),entryCantidad.get(),subtotal,total))
            listaArticulos.append([entryCodigo.get(),"Stock",entryStock.get(),entryCantidad.get(),subtotal,iva,total,entryInsumo.get()])
            print(listaArticulos)
            
        except:
            messagebox.showinfo("Datos"," Debe de llenar todos los datos")
        clientes.append(["DNI: : ",entryDni.get(),"Apellido: ",entryApellido.get(),"Nombre: ",entryNombre.get()])
        print(clientes)
    #Venta y ticket
    def vender():
        miConexion=sqlite3.connect('insumos.db')
        ventConexion=sqlite3.connect('venta.db')
        miCursor= miConexion.cursor()
        tabla= ventConexion.cursor()
        subtotal = 0
        for dato in listaArticulos:
            nuevoStock = int(dato[2]) - int(dato[3])
            valores = (nuevoStock, dato[0])
            
            miCursor.execute("UPDATE insumos SET CANTIDAD=? WHERE ID=?",valores)
            
            miConexion.commit()
            subtotal = subtotal + dato[4]
        subtotal= round(subtotal,2)
        iva = round(subtotal * 0.21,2)
        total = round(subtotal + iva,2)
        
        valores = (subtotal,iva,total)
        tabla.execute("INSERT INTO venta(subtotal,iva,total) VALUES(?,?,?)",valores)
        ventConexion.commit()
        tabla.execute("SELECT max(nfactura) FROM venta")
        nFacturaMax = tabla.fetchall()
        for dato in listaArticulos:
            articuloVenta = (dato[0],nFacturaMax[0][0],dato[7],dato[3],dato[4],dato[5],dato[6])
            tabla.execute("INSERT INTO articulosVendidos(codigo,nfactura,detalle,cantidad,subtotal,iva,total) VALUES(?,?,?,?,?,?,?)",articuloVenta)
        ventConexion.commit()        
        miCursor.close()
        ventConexion.close()
        
        nombreTxt = str(entryDni.get())+".txt"
        escribir = open(nombreTxt,"w")
        escribir.write("Ticket Venta")
        escribir.write("\n")
        escribir.write("\n")
        escribir.write("Datos Cliente")
        escribir.write("\n")
        escribir.write("\n")
        escribir.write("DNI: " + str(entryDni.get()))
        escribir.write("\n")
        escribir.write("Apellido: " + str(entryApellido.get()))
        escribir.write("\n")
        escribir.write("Nombre: " + str(entryNombre.get()))
        
        escribir.write("\n")
        escribir.write("\n")
        
        escribir.write("----------------")
        escribir.write("\n")
        escribir.write("\n")
        escribir.write("Insumos/Descartables: ")
        escribir.write("\n")
        for dato in listaArticulos:
            escribir.write(str(dato[7])+" x "+str(dato[3]))
            escribir.write("\n")
        escribir.write("                   "+str(subtotal))
        escribir.write("\n")
        escribir.write("\n")
        escribir.write("----------------")
        escribir.write("\n")                 
        escribir.write("Subtotal              "+str(subtotal))
        escribir.write("\n")
        escribir.write("IVA                   "+str(iva))
        escribir.write("\n")
        escribir.write("Total                 "+str(total))
        escribir.close()
        os.startfile(nombreTxt,"print")
        
    
    tree.bind("<Double-1>", seleccionarUsandoClick) #Ligo a la tabla

    
    def buscar():
        conexion=sqlite3.connect('clientes.db')
        conexion.row_factory = sqlite3.Row
        buscar=(buscarDni.get(),)
        tabla= conexion.cursor()
        
        tabla.execute("SELECT * FROM clientes WHERE dni=?",buscar)
        
        datos = tabla.fetchall()
        tabla.close()
        
        if(len(datos)>0):
            #messagebox.showinfo("Sistema","Cliente encontrado")
            entryDni.config(state="normal")
            entryNombre.config(state="normal")
            entryApellido.config(state="normal")
            
            entryDni.delete(0,END)
            entryNombre.delete(0,END)
            entryApellido.delete(0,END)
            
            for dato in datos:
                entryDni.insert(0,dato['dni'])
                entryNombre.insert(0,dato['nombre'])
                entryApellido.insert(0,dato['apellido'])
                
            entryDni.config(state="readonly")
            entryNombre.config(state="readonly")
            entryApellido.config(state="readonly")
            
        else:
            messagebox.showwarning("Sistema","Cliente NO encontrado")

    
    #ETIQUEtAS Y CAJAS DE TEXTO
    
    tituloClientes = tk.Label(root,text="DNI Cliente: ",bg="#040170",fg="white", font=("bold"))
    tituloClientes.place(x=800,y=470)
    
    buscarDni = Entry(root)
    buscarDni.place(x=900,y=470)   
    
    botonBuscarCliente= Button(root,cursor="hand2",text="Buscar",command=buscar)
    botonBuscarCliente.place(x=1050,y=470) 
    
    #labelDni = tk.Label(root,text="DNI",bg="steel blue",fg="white",font=("Calibri",20,"bold"))
    #labelDni.grid(row=9,column=0,padx=20,pady=10)
    entryDni = Entry(root,font=("Calibri",15),state="readonly")
    #entryDni.grid(row=9,column=1)

    labelNombre = tk.Label(root,text="Nombre: ",bg="#040170",fg="white",font=("bold"))
    labelNombre.place(x=800,y=530)
    entryNombre = Entry(root,state="readonly", width=40)
    entryNombre.place(x=880,y=530)

    labelApellido= tk.Label(root,text="Apellido: ",bg="#040170",fg="white",font=("bold"))
    labelApellido.place(x=800,y=570)
    entryApellido = Entry(root,state="readonly", width=40)
    entryApellido.place(x=880,y=570)
    
    #LABEL
    #Insumos/Descartables
    l2=tk.Label(root, background='#040170', foreground="white", text="Insumos/Descartables: ", font=("bold"))
    l2.place(x=130,y=670)
    #Cantidad
    l3=tk.Label(root, background='#040170', foreground="white", text="Cantidad: ", font=("bold"))
    l3.place(x=450,y=670)
       
    #Ventas TITULO
    titulo = tk.Label(root, background='#040170', foreground="white",text="VENTA DE INSUMOS MEDICOS - STOCK",font=("Calibri",20,"bold"))
    titulo.place(x=200,y=10)
    #Carrito TITULO
    titulo2 = tk.Label(root, background='#040170', foreground="white",text="CARRITO DE COMPRAS",font=("Calibri",20,"bold"))
    titulo2.place(x=895,y=10)
    
    #ENTRY
    #ID
    e1=Entry(root, textvariable=miId) #No se ve, recolecta los valores del registro
    #Precio
    entryPrecio=Entry(root, textvariable=miPrecio)#No se ve, recolecta los valores del registro
    #Codigo
    entryCodigo=Entry(root, textvariable=miId) #No se ve, recolecta los valores del registro
    #Insumo
    entryInsumo=Entry(root, textvariable=miNombre, width=50)
    #Stock
    entryStock=Entry(root, textvariable=miCantidad)
    #Cantidad
    entryCantidad=Entry(root)
    entryCantidad.place(x=550, y=670)
    #Insumos/Descartables
    e2=Entry(root, textvariable=miNombre, width=20)
    e2.place(x=310, y=670)
        
    #BOTONES
    #Boton mostrar
    botonMostrar=tk.Button(root, cursor="hand2",text="Mostrar Lista", width=85 ,command=mostrar)
    botonMostrar.place(x=130, y=635)
    #Boton Agregar
    botonVender=tk.Button(root,cursor="hand2",text="Agregar al carrito ->", command=agregar)
    botonVender.place(x=618, y=700)
    #Boton Vender
    botonVender= tk.Button(root,cursor="hand2",text="Realizar Compra",width=68,command=vender)
    botonVender.place(x=800,y=635)
    
########## PROVEEDORES ##########
""" def vProveedores(): 
    proveedores=tk.Toplevel()
    proveedores.geometry("600x400") 
    proveedores.title("Compras")
    proveedores.config(bg='ghost white')
    proveedores.resizable(0,0)#remuevo el botón maximizar

    center(proveedores) """

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
    Aplicación CRUD - Venta de Insumos
    Version 1.0
    
    Tecnologías: Python - Tkinter - SQLite
    
    Profesor: QUIROGA, Ignacio
    Alumno: VASSALLO, Mario Nicolás
    
          -INSTITUTO NUEVO CUYO-
    '''
    messagebox.showinfo(title="Información", message=acerca)

#BOTONES
def botones():
    
    btInsumos=Button(root, cursor="hand2", text="Insumos", command= vInsumos, state='normal' )
    #btProveedores=Button(root, text="Proveedores", command=vProveedores, state='normal')
    btCompras=Button(root, cursor="hand2",text="Compras", command=vCompras, state='normal')    
    btClientes=Button(root,cursor="hand2",text="Clientes", command=vClientes)
    btVentas=Button(root,cursor="hand2",text="Recetear carrito", command=ventas)
    btSalir=Button(root,cursor="hand2" ,text="Salir", command= salirAplicacion)
    
    #Ubicacion de Botones
    btInsumos.place(x=10, y=160, width=80, height=80)
    #btProveedores.place(x=10, y=160, width=80, height=80)
    btCompras.place(x=10, y=240, width=80, height=80)
    btClientes.place(x=10, y=320, width=80, height=80)
    btVentas.place(x=1170,y=520, width=100, height=80)
    btSalir.place(x=10, y=550, width=80, height=80)


#INTERFAZ GRAFICA
root=Tk()
root.title("Ventana principal")
#root.geometry("1000x600")
root.attributes("-fullscreen", True)
root.iconbitmap("iconoMain.ico")
center(root)#Uso esta funcion para centrar la pantalla
root.config(bg='#040170')
root.resizable(0,0)#remuevo el botón maximizar

#LLAMO FUNCIONES
conexionBBDD()
ventas()
botones()

def cerrar():
    if messagebox.askokcancel("Cerrar","Desea salir"):
        root.destroy()
root.protocol("WM_DELETE_WINDOW", cerrar)

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