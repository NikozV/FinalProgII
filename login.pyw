#LIBRERIAS

from tkinter import *
from tkinter import messagebox

import sqlite3 #Importo el modulo sqlite3

#CONEXION Y CREACION DE TABLA SI NO ESTA Y USUAIO ADMINISTRADOR
def conect():
    conexion = sqlite3.connect('login.db')#Conexion sqlite
    c = conexion.cursor() #Creo cursor

    #Crear tabla si no existe
    c.execute("CREATE TABLE IF NOT EXISTS login("+
    "id INTEGER PRIMARY KEY  AUTOINCREMENT, "+ #creo tabla id
    "nombre VARCHAR(50) NOT NULL UNIQUE, "+ #creo tabla nombre 
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

#PANTALLA PRINCIPAL
def menu_pantalla():
    conect() #Conecto con la bd
    global pantalla #creo variable global para pantalla

    pantalla=Tk() 
    pantalla.geometry("300x380") #Le doy las dimensiones a la pantalla
    pantalla.title("Bienvenido") #Titulo de pantalla
    try:
        pantalla.iconbitmap("loginuser.ico") #Icono .ico
    except:
        pass
    center(pantalla)#Uso esta funcion para centrar la pantalla
    pantalla.resizable(0,0)#remuevo el botón maximizar
        
    #IMAGEN
    image=PhotoImage(file="icon-login.gif") #Llamo una imagen
    image=image.subsample(2,2) #Redimensiono imagen
    label=Label(image=image)
    label.pack() #uso el metodo pack para mostrarlo

    #ETIQUETA ACCESO
    Label(text="Acceso al Sistema", #texto del label
    bg="orange", #color de fondo del label
    #fg="White", #color letra
    width="300", #ancho del label
    height="1", #altura del label
    font=("Calibri", 15) #tipo de fuente y tamaño
    ).pack() #uso el metodo pack para mostrarlo
    Label(text="").pack() #creo un Label con texto en blanco para dar un salto de linea y los muestro

    #BOTONES
    Button(cursor="hand2", 
     bd=1, #Profundidad del boton
     bg ="white smoke", 
     text="Iniciar sesion", 
     width="30", #ancho
     height="3", #altura
     command=menu_inicio_sesion # llamo a la funcion inicio_sesion
     ).pack() #creo boton iniciar sesion
    Label(text="").pack()

    Button(cursor="hand2", bd=1, bg ="white smoke", text="Registrar", width="30", height="3", command=menu_registrar).pack() #creo boton para registrar un usuario nuevo
    
    Label(text="").pack() #creo un Label con texto en blanco para dar un salto de linea y los muestro
    Label(text="").pack() # =
    Label(text= "© Vassallo M. Nicolas").pack()

    pantalla.mainloop()
    pantalla.destroy()
    
#PANTALLA DE INICIO DE SESION // BOTON INICIO DE SESION
def menu_inicio_sesion():
    
    global pantalla1 #creo variable global para pantalla1
    pantalla1 = Toplevel(pantalla)
    pantalla1.geometry("300x250")
    pantalla1.title("Inicio de sesion") 
    try: 
        pantalla1.iconbitmap("loginuser.ico") #Icono .ico
    except:
        pass
    pantalla1.configure(bg='ghost white')
    center(pantalla1)#Uso esta funcion para centrar la pantalla

    Label(pantalla1, text="Ingrese su usuario y contraseña", bg="orange", width="300" ).pack()
    Label(pantalla1, text="", bg='ghost white').pack()
    pantalla1.resizable(0,0)#remuevo el botón maximizar

    global nombreusuario_verify
    global contraseñausuario_verify
    nombreusuario_verify = StringVar() #Declaro la variable como tipo cadena
    contraseñausuario_verify = StringVar()

    global nombre_usuario_entry
    global contraseña_usuario_entry

    Label(pantalla1, text="Usuario", bg='ghost white').pack()
    nombre_usuario_entry = Entry(pantalla1, textvariable=nombreusuario_verify) #Caja de texto
    nombre_usuario_entry.pack()
    Label(pantalla1, bg='ghost white').pack()

    Label(pantalla1, text="Contraseña", bg='ghost white').pack()
    contraseña_usuario_entry = Entry(pantalla1, show="*", textvariable=contraseñausuario_verify) #Con show="*" hacemos que no se vea la contraseña
    contraseña_usuario_entry.pack()
    Label(pantalla1, bg='ghost white').pack()

    Button(pantalla1, cursor="hand2", bd=1, bg ="white smoke", text="Iniciar Sesion", command = validacion).pack()
    
#PANTALLA DE REGISTRO
def menu_registrar():
    global pantalla2
    pantalla2=Toplevel(pantalla)
    pantalla2.geometry("300x250")
    pantalla2.title("Registro de usuario")  
    pantalla2.iconbitmap("loginuser.ico") #Icono .ico
    pantalla2.configure(bg='ghost white') #Color de panatlla2

    center(pantalla2)#Uso esta funcion para centrar la pantalla
    pantalla2.resizable(0,0)#remuevo el botón maximizar

    global nombreusuario_entry
    global contraseña_entry

    nombreusuario_entry = StringVar()
    contraseña_entry = StringVar()

    Label(pantalla2, text="Ingrese un usuario y contraseña de su eleccion,\n para registrarce al sistema", bg="orange", width="300").pack()
    Label(pantalla2, text="", bg='ghost white').pack()

    Label(pantalla2, text="Usuario", bg='ghost white').pack()
    nombreusuario_entry = Entry(pantalla2)
    nombreusuario_entry.pack()
    Label(pantalla2, bg='ghost white').pack()

    Label(pantalla2, text="Contraseña", bg='ghost white').pack()
    contraseña_entry = Entry(pantalla2, show="*")
    contraseña_entry.pack()
    Label(pantalla2, bg='ghost white').pack()

    Button(pantalla2, cursor="hand2", bd=1, bg ="white smoke", text="Registrar", command = insertar).pack()

'''
#CONTROL DE REGISTRO
def control_reg():

    conexion = sqlite3.connect('../login/login.db')#Conexion sqlite
    c = conexion.cursor() #Creo cursor
    
    user = nombreusuario_entry.get()
    
    c.execute("SELECT nombre FROM login")

    filas=c.fetchall()

    print(filas)
    #print(user)
    
    while filas == True:
        print(filas)
        if filas[0] == user:
            messagebox.showerror(title="Usuario existente", message="Usuario existente")
            
        else:
            pass
    
    for fila in filas:
        print (fila)
        if fila[0] == user:
            messagebox.showerror(title="Usuario existente", message="Usuario existente")
            
        else:
            insertar()
    
    conexion.close()#cierro coneccion
'''
#REGISTRO DE USUARIO
def insertar(): 
       
    conexion = sqlite3.connect('login.db')#Conexion sqlite
    c = conexion.cursor() #Creo cursor
          
    datos = (nombreusuario_entry.get(),contraseña_entry.get()) #get se utiliza para capturar datos de ntro de un entry
    #cursor.execute('INSERT INTO login (nombre,contrasena) VALUES (?,?)', datos)#Ingreso a la db los datos suministrados por el usr
    #conexion.commit() #Guardo cambios

    try: #Utilizo la palabra reservada try para hcaer una excepcion
        c.execute('INSERT INTO login (nombre, contrasena) VALUES (?, ?)', datos) 
        conexion.commit()#Guardo los cambios
         
    except sqlite3.IntegrityError:
        messagebox.showerror(title="Usuario existente", message="Ya existe este usuario")
        pantalla2.destroy()
        menu_registrar()
        #conexion.rollback()#revisa que no haya ningun error en la db
        #messagebox.showinfo(message="ERROR", title="AVISO")
    else:
        messagebox.showinfo(title="Bienvenido", message=("Usuario creado correctamente "))
        pantalla2.destroy()
        menu_inicio_sesion()
        
    conexion.close()#cierro coneccion

#VALIDACION-LOGIN
def validacion():

    conexion = sqlite3.connect('login.db')#Conexion sqlite
    c = conexion.cursor() #Creo cursor
    
    datos = (nombreusuario_verify.get(),contraseñausuario_verify.get())
     
    c.execute("SELECT * FROM login WHERE nombre = ? AND contrasena = ?", datos)

    if c.fetchall():
        if (nombreusuario_verify.get() == "adm"):
            #messagebox.showinfo(title="Login Correcto", message=("ADM "))
            pantalla1.destroy()
            pantalla.destroy()
            
            import avanzado #importo programa para administrador
        else:
            messagebox.showinfo(title="Login Correcto", message=("Bienvenido Usuario"))
            pantalla1.destroy()
            pantalla.destroy()
            try:
                import main
            except ModuleNotFoundError:
                import main
                
        
    else:
        messagebox.showerror(title="Login inorrecto", message="Usuario o contraseña incorrecta")
        pantalla1.destroy()
        menu_inicio_sesion()

    conexion.close()#cierro coneccion
 
menu_pantalla() #llamo a la funcion menu_pantalla