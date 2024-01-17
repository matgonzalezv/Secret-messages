import csv
import doctest
from os import remove
from os import rename
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


def validar_usuario(usuario):
    """ 
    >>> validar_usuario("juan_perez")
    True
    >>> validar_usuario("maria.23")
    True
    >>> validar_usuario("nombre@usuario")
    False
    >>> validar_usuario("corto")
    True
    >>> validar_usuario("usuario_largo_nombre")
    False
    >>> validar_usuario("usuario.nombre")
    True
    >>> validar_usuario("usuario-nombre")
    True
    >>> validar_usuario("usuario123")
    True
    >>> validar_usuario("usuario#nombre")
    False
    >>> validar_usuario("usuario_________")
    False
    >>> validar_usuario("usuario123456789012345")
    False
    """
    
    caracteres_validos = ["_","-","."]
    LONGITUD_MINIMA = 5
    LONGITUD_MAXIMA = 15
    usuario_valido = True
    longitud_usuario = len(usuario)

    longitud_valida = LONGITUD_MINIMA <= longitud_usuario <= LONGITUD_MAXIMA

    if longitud_valida: 
        i = 0
        while usuario_valido and i < longitud_usuario:
            if usuario[i].isalnum():
                pass
            elif usuario[i] in caracteres_validos:
                pass
            else:
                usuario_valido = False
            i+=1
    else:
        usuario_valido = False
    
    return usuario_valido

def validar_clave(clave):
    """    
    >>> validar_clave("Clave#123")
    True
    >>> validar_clave("AbcdEfgh")
    False
    >>> validar_clave("clave123")
    True
    >>> validar_clave("Passw0rd")
    False
    >>> validar_clave("clave--#")
    False
    >>> validar_clave("Aa1#Aa1#")
    True
    >>> validar_clave("clave")
    False
    >>> validar_clave("ClaveSecreta")
    False
    >>> validar_clave("C*ontr@aseñ@")
    False
    >>> validar_clave("12--34")
    False
    >>> validar_clave("Clav3#")
    True
    
    """
    caracteres_pedidos = ["-","#","*"]

    LONGITUD_MINIMA = 4
    LONGITUD_MAXIMA = 8

    longitud_clave = len(clave)

    tiene_mayuscula = False
    tiene_minuscula = False
    tiene_numero = False
    tiene_caracter_pedido = False
    adyacente = False
    caracter_invalido = False
    longitud_valida = LONGITUD_MINIMA <= longitud_clave <= LONGITUD_MAXIMA
    
    if longitud_valida:
        i=0
        caracter_anterior = ""
        while not adyacente and i < longitud_clave:
            if clave[i] == caracter_anterior:
                adyacente = True
            elif clave[i].isalpha():
                if clave[i].islower():
                    tiene_minuscula = True
                else:
                    tiene_mayuscula = True
            elif clave[i].isnumeric():
                tiene_numero = True
            elif clave[i] in caracteres_pedidos:
                tiene_caracter_pedido = True
            else:
                caracter_invalido = True
            caracter_anterior = clave[i]
            i+=1
        
    return tiene_mayuscula and tiene_minuscula and tiene_numero and tiene_caracter_pedido and longitud_valida and not caracter_invalido and not adyacente

def leer_usuario(archivo):
    linea = archivo.readline()

    if linea:   
        devolver = linea.rstrip("\n").split(",")
    else:
        devolver = "","","","",""

    return devolver

def leer_preguntas(archivo):
    linea = archivo.readline()

    if linea:
        devolver = linea.rstrip("\n").split(",")
    else:
        devolver = "",""
    return devolver


def crear_usuario(usuario,clave,id_pregunta_seguridad, respuesta):
    usuario_valido = validar_usuario(usuario)
    clave_valida = validar_clave(clave)
    
    usuario_existente = False
    usuario_insertado = False
    
    if usuario_valido and clave_valida:

        archivo_usuarios=open("usuario_clave.csv") 
        nuevo_archivo_usuarios =open("nuevo_usuario_clave.csv","w")

        usuario_archivo,clave_archivo,id_pregunta_seguridad_archivo,respuesta_archivo,intentos = leer_usuario(archivo_usuarios)

        while usuario_archivo != "":

            if usuario_archivo == usuario:
                usuario_existente = True
                nuevo_archivo_usuarios.write(f"{usuario_archivo},{clave_archivo},{id_pregunta_seguridad_archivo},{respuesta_archivo},{intentos}\n")
            elif usuario < usuario_archivo and not usuario_existente and not usuario_insertado:
                usuario_insertado = True

                nuevo_archivo_usuarios.write(f"{usuario},{clave},{id_pregunta_seguridad},{respuesta},0\n")
                nuevo_archivo_usuarios.write(f"{usuario_archivo},{clave_archivo},{id_pregunta_seguridad_archivo},{respuesta_archivo},{intentos}\n")
                messagebox.showinfo("completado","Identificador guardado")
            else:
                nuevo_archivo_usuarios.write(f"{usuario_archivo},{clave_archivo},{id_pregunta_seguridad_archivo},{respuesta_archivo},{intentos}\n")
                
            usuario_archivo,clave_archivo,id_pregunta_seguridad_archivo,respuesta_archivo,intentos = leer_usuario(archivo_usuarios)
            
        if usuario_archivo == "":
            if not usuario_existente and not usuario_insertado:
                usuario_insertado = True
                nuevo_archivo_usuarios.write(f"{usuario},{clave},{id_pregunta_seguridad},{respuesta},0\n")
                messagebox.showinfo("completado","Identificador guardado")
            elif not usuario_insertado and usuario_existente:
                messagebox.showwarning("error","Identificador en uso")
                    
        archivo_usuarios.close()
        nuevo_archivo_usuarios.close()
        remove("usuario_clave.csv")
        rename("nuevo_usuario_clave.csv","usuario_clave.csv")
    
    elif not usuario_valido or not clave_valida:
        messagebox.showwarning("eror","clave o usuario invalidos")

    return usuario_insertado
        
def comprobar_usuario_clave_correctos(usuario,clave): 

    archivo = open("usuario_clave.csv")
    usuario_archivo,clave_archivo,id_pregunta_seguridad_archivo,respuesta_archivo,intentos = leer_usuario(archivo)
    encontrado = False

    while usuario_archivo != "" and not encontrado:

        if usuario == usuario_archivo:
            if clave == clave_archivo:
                encontrado = True

        usuario_archivo,clave_archivo,id_pregunta_seguridad_archivo,respuesta_archivo,intentos = leer_usuario(archivo)
        
    return encontrado


def actualizar_intentos(usuario,intentos_actualizado):

    archivo_usuarios = open("usuario_clave.csv")
    nuevo_archivo_usuarios = open("nuevo_usuario_clave.csv","w")

    usuario_archivo,clave_archivo,id_pregunta_seguridad_archivo,respuesta_archivo,intentos = leer_usuario(archivo_usuarios)

    
    while usuario_archivo != "":

        if usuario_archivo == usuario:
            nuevo_archivo_usuarios.write(f"{usuario},{clave_archivo},{id_pregunta_seguridad_archivo},{respuesta_archivo},{intentos_actualizado}\n")
        else:
            nuevo_archivo_usuarios.write(f"{usuario_archivo},{clave_archivo},{id_pregunta_seguridad_archivo},{respuesta_archivo},{intentos}\n")

        usuario_archivo,clave_archivo,id_pregunta_seguridad_archivo,respuesta_archivo,intentos = leer_usuario(archivo_usuarios)
    
    
    
    archivo_usuarios.close()
    nuevo_archivo_usuarios.close()

    messagebox.showwarning("warning","Incorrect answer")

    remove("usuario_clave.csv")
    rename("nuevo_usuario_clave.csv","usuario_clave.csv")



def recuperar_contraseña(usuario,id_pregunta,respuesta_pregunta):

    INTENTOS_MAXIMOS = 3
    encontrado = False
    terminar = False
    exitoso = False

    archivo_usuarios = open("usuario_clave.csv")
    usuario_archivo,clave_archivo,id_pregunta_seguridad_archivo,respuesta_archivo,intentos = leer_usuario(archivo_usuarios)
    
    
    while usuario_archivo != "" and not encontrado:

            if  usuario == usuario_archivo:
                encontrado = True
                if id_pregunta == id_pregunta_seguridad_archivo:
                    if int(intentos) < INTENTOS_MAXIMOS:
                        if respuesta_pregunta == respuesta_archivo:
                            messagebox.showinfo("completado",f"usuario:{usuario_archivo} clave:{clave_archivo}")
                            archivo_usuarios.close()
                            terminar = True
                            exitoso = True
                            
                        else:
                            archivo_usuarios.close()
                            intentos_actualizado = str(int(intentos)+1)
                            actualizar_intentos(usuario,intentos_actualizado)                    
                    else:
                        messagebox.showerror("error","User blocked")
                        archivo_usuarios.close() 
                        terminar = True   
                        exitoso = False
            else:
                usuario_archivo,clave_archivo,id_pregunta_seguridad_archivo,respuesta_archivo,intentos = leer_usuario(archivo_usuarios)
                if usuario_archivo == "":
                    messagebox.showerror("error","User not found")
                    archivo_usuarios.close()

    return terminar,exitoso

            
def normalizar_mensaje(mensaje):
    vocales_tildadas = ['á', 'é', 'í', 'ó', 'ú','Á','É','Í','Ó','Ú']
    vocales_sin_tildar = ['a', 'e', 'i', 'o', 'u','A','E','I','O','U']
    
    mensaje_a_analizar=""
    
    for caracter in mensaje:
        if caracter == "ñ":
            nuevo_caracter = "ni"
        elif caracter == "Ñ":
            nuevo_caracter = "NI"
        elif caracter in vocales_tildadas:
                indice = vocales_tildadas.index(caracter)
                nuevo_caracter = vocales_sin_tildar[indice]
        else:
            nuevo_caracter = caracter
        mensaje_a_analizar += nuevo_caracter
        
    return mensaje_a_analizar


def cifrado_cesar(mensaje, clave):    
    """  
    >>> cifrado_cesar("holaaBa##12",3)
    'kroddEd##45'

    >>> cifrado_cesar("kroddEd##45",-3)
    'holaaBa##12'

    >>> cifrado_cesar("algoritmos y programacion 1",4)
    'epksvmxqsw c tvskveqegmsr 5'

    >>> cifrado_cesar("epksvmxqsw c tvskveqegmsr 5",-4)
    'algoritmos y programacion 1'

    >>> cifrado_cesar("cifrado_cesar",17)
    'tzwiruf_tvjri'

    >>> cifrado_cesar("tzwiruf_tvjri",-17)
    'cifrado_cesar'

    >>> cifrado_cesar("mensajé_secreto N° 1222",18)
    'ewfksbw_kwujwlg F° 9000'

    >>> cifrado_cesar("ewfksbw_kwujwlg F° 9000",-18)
    'mensaje_secreto N° 1222'

    >>> cifrado_cesar("Hóla Este es mi menSaj3 secret0!",7)
    'Ovsh Lzal lz tp tluZhq0 zljyla7!'

    >>> cifrado_cesar("Ovsh Lzal lz tp tluZhq0 zljyla7!",-7)
    'Hola Este es mi menSaj3 secret0!'
    """

    LONGITUD_ALFABETO = 26
    LONGITUD_NUMEROS = 10

    mensaje_cifrado=""
    
    mensaje_a_analizar = normalizar_mensaje(mensaje)
    for caracter in mensaje_a_analizar:
        
        if caracter.isalpha():

            if caracter.islower():  
                nuevo_caracter = chr(ord("a") + ((ord(caracter)- ord("a")+clave) % LONGITUD_ALFABETO))  
            else:
                nuevo_caracter = chr(ord("A") + ((ord(caracter)- ord("A")+clave) % LONGITUD_ALFABETO))  

        elif caracter.isnumeric():
            nuevo_caracter = str((int(caracter)+clave)%LONGITUD_NUMEROS)
            
        else:
            nuevo_caracter = caracter

        mensaje_cifrado += nuevo_caracter

    return mensaje_cifrado


def boton_cifrado_cesar(inputMensaje, inputClave, resultado_text):
    mensaje = inputMensaje.get()
    clave = int(inputClave.get())
    mensaje_cifrado = cifrado_cesar(mensaje, clave)
    mostrar_resultado(resultado_text, "Texto cifrado (Cesar):", mensaje_cifrado)

def boton_descifrado_cesar(inputMensaje, inputClave, resultado_text):
    mensaje = inputMensaje.get()
    clave = int(inputClave.get())
    mensaje_descifrado = cifrado_cesar(mensaje, -clave)
    mostrar_resultado(resultado_text, "Texto descifrado (Cesar):", mensaje_descifrado)


def boton_ingreso(raiz,input_usuario, input_clave):
    usuario = input_usuario.get()
    clave = input_clave.get()

    if comprobar_usuario_clave_correctos(usuario,clave):
        raiz.destroy()
        interfaz_mensajes(usuario)
    else: 
        messagebox.showwarning("No identifier or wrong password","If you are not registered you must register first or if you forgot your password press the password recovery button")
        

def cargar_preguntas():
    lista = []

    archivo_preguntas=open("preguntas.csv")
    num_pregunta,pregunta =leer_preguntas(archivo_preguntas)

    while num_pregunta != "":
        lista.append(f" {num_pregunta}-{pregunta}")
        num_pregunta,pregunta =leer_preguntas(archivo_preguntas)
    
    return lista


def boton_registro(raiz):
    raiz.destroy()
    lista_preguntas = cargar_preguntas()
    interfaz_registro(lista_preguntas)

def boton_recuperacion_contraseña(raiz):
    raiz.destroy()
    lista_preguntas = cargar_preguntas()
    interfaz_recuperacion_contraseña(lista_preguntas)


def boton_recuperar_contraseña(raiz,input_usuario,combo_var,input_respuesta):
    usuario = input_usuario.get()
    id_pregunta_seguridad = combo_var.get().split("-")[0]
    respuesta = input_respuesta.get()

    terminar,exitoso = recuperar_contraseña(usuario,id_pregunta_seguridad,respuesta)

    if terminar:
        raiz.destroy()
        if exitoso:
            interfaz_login()
        else:
            interfaz_inicial()

def boton_ingresar_registro(raiz,input_usuario,input_contraseña,combo_var,input_respuesta):

    usuario = input_usuario.get()
    clave= input_contraseña.get()
    id_pregunta_seguridad = combo_var.get().split("-")[0]
    respuesta = input_respuesta.get()
    
    usuario_insertado = crear_usuario(usuario,clave,id_pregunta_seguridad, respuesta)
    
    if usuario_insertado:
        raiz.destroy()
        interfaz_login()



# objetivo 2: cifrado atbash
def cifrado_atbash(cadena):
    lista_caracteres = []
    numeros = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    numeros_invertidos = ["9", "8", "7", "6", "5", "4", "3", "2", "1", "0"]
    letras_minuscula = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    letras_invertidas_mayuscula = ["Z", "Y", "X", "W", "V", "U", "T", "S", "R", "Q", "P", "O", "N", "M", "L", "K", "J", "I", "H", "G", "F", "E", "D", "C", "B", "A"]
    for letra in cadena:
        if letra.islower():
            lista_caracteres.append(letras_invertidas_mayuscula[letras_minuscula.index(letra)])
        elif letra.isupper():
            lista_caracteres.append(letras_minuscula[letras_invertidas_mayuscula.index(letra)])
        elif letra.isdigit():
            lista_caracteres.append(numeros[numeros_invertidos.index(letra)])
        else:
            lista_caracteres.append(letra)
    nueva_cadena = "".join(lista_caracteres)
    return nueva_cadena

mensaje_cifrado_global = "" #Variable global

def boton_interfaz_login(raiz):
    raiz.destroy()
    interfaz_login()


def interfaz_inicial():
    raiz = Tk()
    raiz.title('Secret messages') 
    raiz.resizable(True, True)
    raiz.geometry("1024x768")
    raiz.config(bg="#9ED8F9")

    mi_frame = Frame(raiz,bg="#9ED8F9")
    mi_frame.config(bd=10,relief="groove")
    mi_frame.pack(pady=100)

    label_bienvenida = Label(mi_frame,font=('Courier',12),bg="#9ED8F9",text="Welcome to the secret messaging app. \n Press 'Login' to enter, or press 'Register' to create a new account.")
    label_bienvenida.grid(row=0,column=0,padx=10,pady=10, columnspan=2)

    boton_continuar = Button(mi_frame,text="Login",bg="#D5CF13",command=lambda:boton_interfaz_login(raiz))
    boton_continuar.grid(row=1,column=0,pady=10,padx=(250, 5))

    boton_registrar = Button(mi_frame,text="Register",bg="#D5CF13", command=lambda: boton_registro(raiz))
    boton_registrar.grid(row=1,column=1, pady=10, padx=(5, 250))

    label_integrantes = Label(mi_frame,font=('Courier',12),bg="#9ED8F9",text="Built by:\n \n Matías Gonzalez Vieyra \n Brian Agustín Conde \n Leandro Contestabile")
    label_integrantes.grid(row=2,column=0,pady=10,columnspan=2)

    raiz.mainloop()

def interfaz_login():
    raiz_login = Tk()
    raiz_login.title("Identification for access")
    raiz_login.resizable(True, True)
    raiz_login.geometry("1024x768")
    raiz_login.config(bg="#9ED8F9")
    frame_login = Frame(raiz_login,bg="#9ED8F9")
    frame_login.config(bd=10,relief="groove")
    frame_login.pack(pady=100)

    label_usuario = Label(frame_login,font=('Courier',12),bg="#9ED8F9",text="User:")
    label_usuario.grid(row=0,column=0,padx=5,pady=10)
    
    label_contraseña = Label(frame_login,font=('Courier',12),bg="#9ED8F9",text="Password:")
    label_contraseña.grid(row=1,column=0,padx=5,pady=10)
    
    input_usuario=Entry(frame_login)
    input_usuario.grid(row=0,column=1,padx=10)
    
    input_contraseña=Entry(frame_login)
    input_contraseña.grid(row=1,column=1,padx=10)

    frame_botones = Frame(raiz_login, bg="#9ED8F9")
    frame_botones.pack(pady=15)

    boton_ingresar = Button(frame_botones,text="Login",bg="#856ff8", bd=5, command=lambda: boton_ingreso(raiz_login,input_usuario,input_contraseña))
    boton_ingresar.grid(row=0,column=0, padx=5)


    boton_recuperar = Button(frame_botones,text="Retrieve",bg="#856ff8", bd=5, command=lambda: boton_recuperacion_contraseña(raiz_login))
    boton_recuperar.grid(row=0,column=2, padx=5)
    
    
    raiz_login.mainloop()

def interfaz_registro(lista_preguntas):
    raiz = Tk()
    raiz.title("Register")
    raiz.resizable(True, True)
    raiz.geometry("1024x768")
    raiz.config(bg="#9ED8F9")
    frame_registro = Frame(raiz,bg="#9ED8F9")
    frame_registro.config(bd=10,relief="groove")
    frame_registro.pack(pady=100)

    label_usuario = Label(frame_registro,font=('Courier',12),bg="#9ED8F9",text="User:")
    label_usuario.grid(row=0,column=0,padx=5,pady=10)
    
    label_contraseña = Label(frame_registro,font=('Courier',12),bg="#9ED8F9",text="Password:")
    label_contraseña.grid(row=1,column=0,padx=5,pady=10)

    label_pregunta = Label(frame_registro,font=('Courier',12),bg="#9ED8F9",text="Security question:")
    label_pregunta.grid(row=2,column=0,padx=5,pady=10)

    label_respuesta = Label(frame_registro,font=('Courier',12),bg="#9ED8F9",text="Answer:")
    label_respuesta.grid(row=3,column=0,padx=5,pady=10)
    
    input_usuario=Entry(frame_registro)
    input_usuario.grid(row=0,column=1,padx=10)
    
    input_contraseña=Entry(frame_registro)
    input_contraseña.grid(row=1,column=1,padx=10)

    combo_var = tk.StringVar()
    combobox = ttk.Combobox(frame_registro, textvariable=combo_var,values=lista_preguntas)
    combobox.grid(row=2,column=1,padx=10)

    input_respuesta=Entry(frame_registro)
    input_respuesta.grid(row=3,column=1,padx=10)

    frame_botones = Frame(raiz, bg="#9ED8F9")
    frame_botones.pack(pady=15)

    boton_ingresar = Button(frame_botones,text="Login",bg="#D5CF13", command=lambda: boton_ingresar_registro(raiz,input_usuario,input_contraseña,combo_var,input_respuesta))
    boton_ingresar.grid(row=0,column=1, padx=5)


def interfaz_recuperacion_contraseña(lista_preguntas):
    raiz = Tk()
    raiz.title("Retrieve password")
    raiz.resizable(0,0)
    raiz.geometry("750x500")
    raiz.config(bg="#9ED8F9")
    frame_recuperar = Frame(raiz,bg="#9ED8F9")
    frame_recuperar.config(bd=10,relief="groove")
    frame_recuperar.pack(pady=100)

    label_usuario = Label(frame_recuperar,font=('Courier',12),bg="#9ED8F9",text="User:")
    label_usuario.grid(row=0,column=0,padx=5,pady=10)
    
    label_pregunta = Label(frame_recuperar,font=('Courier',12),bg="#9ED8F9",text="Security question:")
    label_pregunta.grid(row=2,column=0,padx=5,pady=10)

    label_respuesta = Label(frame_recuperar,font=('Courier',12),bg="#9ED8F9",text="Answer:")
    label_respuesta.grid(row=3,column=0,padx=5,pady=10)
    
    input_usuario=Entry(frame_recuperar)
    input_usuario.grid(row=0,column=1,padx=10)

    combo_var = tk.StringVar()
    combobox = ttk.Combobox(frame_recuperar, textvariable=combo_var,values=lista_preguntas)
    combobox.grid(row=2,column=1,padx=10)

    input_respuesta=Entry(frame_recuperar)
    input_respuesta.grid(row=3,column=1,padx=10)

    frame_botones = Frame(raiz, bg="#9ED8F9")
    frame_botones.pack(pady=15)

    boton_recuperar = Button(frame_botones,text="retrieve",bg="#D5CF13", command=lambda: boton_recuperar_contraseña(raiz,input_usuario,combo_var,input_respuesta))
    boton_recuperar.grid(row=0,column=1, padx=5)


def cifrar_atbash(texto):
    texto_cifrado = cifrado_atbash(texto) 
    return texto_cifrado

def cifrar(inputMensaje, resultado_text):
    global mensaje_cifrado_global 
    mensaje = inputMensaje.get()
    mensaje_cifrado = cifrar_atbash(mensaje)
    mensaje_cifrado_global = mensaje_cifrado 
    mostrar_resultado(resultado_text, "Texto cifrado (Atbash):", mensaje_cifrado)

def descifrar(inputMensaje, resultado_text):
    global mensaje_cifrado_global  
    mensaje_descifrado = cifrar_atbash(mensaje_cifrado_global) 
    mostrar_resultado(resultado_text, "Texto descifrado (Atbash):", mensaje_descifrado)


def comprobar_solo_usuario(usuario): 
    archivo = open("usuario_clave.csv")
    usuario_archivo,clave_archivo,id_pregunta_seguridad_archivo,respuesta_archivo,intentos = leer_usuario(archivo)
    encontrado_id = False

    while usuario_archivo != "" and not encontrado_id:

        if usuario == usuario_archivo:
            encontrado_id = True
        

        usuario_archivo,clave_archivo,id_pregunta_seguridad_archivo,respuesta_archivo,intentos = leer_usuario(archivo)
        
    return encontrado_id

def botones_solo_usuario(raiz, inputDestinatario):
    usuario = inputDestinatario.get()

    if comprobar_solo_usuario(usuario):
        raiz.destroy()
        interfaz_mensajes(usuario)
    else:
        messagebox.showwarning("Id does not exist")

def actualizar_intentos(usuario,intentos_actualizado):
    archivo_usuarios = open("usuario_clave.csv")
    nuevo_archivo_usuarios = open("nuevo_usuario_clave.csv","w")

    usuario_archivo,clave_archivo,id_pregunta_seguridad_archivo,respuesta_archivo,intentos = leer_usuario(archivo_usuarios)

    
    while usuario_archivo != "":

        if usuario_archivo == usuario:
            nuevo_archivo_usuarios.write(f"{usuario},{clave_archivo},{id_pregunta_seguridad_archivo},{respuesta_archivo},{intentos_actualizado}\n")
        else:
            nuevo_archivo_usuarios.write(f"{usuario_archivo},{clave_archivo},{id_pregunta_seguridad_archivo},{respuesta_archivo},{intentos}\n")

        usuario_archivo,clave_archivo,id_pregunta_seguridad_archivo,respuesta_archivo,intentos = leer_usuario(archivo_usuarios)
    
    
    
    archivo_usuarios.close()
    nuevo_archivo_usuarios.close()

    messagebox.showwarning("warning","Incorrect answer")

    remove("usuario_clave.csv")
    rename("nuevo_usuario_clave.csv","usuario_clave.csv")


def recuperar_contraseña(usuario,id_pregunta,respuesta_pregunta):
    INTENTOS_MAXIMOS = 3
    encontrado = False
    terminar = False
    exitoso = False

    archivo_usuarios = open("usuario_clave.csv")
    usuario_archivo,clave_archivo,id_pregunta_seguridad_archivo,respuesta_archivo,intentos = leer_usuario(archivo_usuarios)
    
    
    while usuario_archivo != "" and not encontrado:

            if  usuario == usuario_archivo:
                encontrado = True
                if id_pregunta == id_pregunta_seguridad_archivo:
                    if int(intentos) < INTENTOS_MAXIMOS:
                        if respuesta_pregunta == respuesta_archivo:
                            messagebox.showinfo("completado",f"usuario:{usuario_archivo} clave:{clave_archivo}")
                            archivo_usuarios.close()
                            terminar = True
                            exitoso = True
                            
                        else:
                            archivo_usuarios.close()
                            intentos_actualizado = str(int(intentos)+1)
                            actualizar_intentos(usuario,intentos_actualizado)                    
                    else:
                        messagebox.showerror("error","User blocked")
                        archivo_usuarios.close() 
                        terminar = True   
                        exitoso = False
            else:
                usuario_archivo,clave_archivo,id_pregunta_seguridad_archivo,respuesta_archivo,intentos = leer_usuario(archivo_usuarios)
                if usuario_archivo == "":
                    messagebox.showerror("error","User not found")
                    archivo_usuarios.close()

    return terminar,exitoso


def normalizar_mensaje(mensaje):
    vocales_tildadas = ['á', 'é', 'í', 'ó', 'ú','Á','É','Í','Ó','Ú']
    vocales_sin_tildar = ['a', 'e', 'i', 'o', 'u','A','E','I','O','U']
    
    mensaje_a_analizar=""
    
    for caracter in mensaje:
        if caracter == "ñ":
            nuevo_caracter = "ni"
        elif caracter == "Ñ":
            nuevo_caracter = "NI"
        elif caracter in vocales_tildadas:
                indice = vocales_tildadas.index(caracter)
                nuevo_caracter = vocales_sin_tildar[indice]
        else:
            nuevo_caracter = caracter
        mensaje_a_analizar += nuevo_caracter
        
    return mensaje_a_analizar


def cifrado_cesar(mensaje, clave):    
    """ 
    >>> cifrado_cesar("holaaBa##12",3)
    'kroddEd##45'

    >>> cifrado_cesar("kroddEd##45",-3)
    'holaaBa##12'

    >>> cifrado_cesar("algoritmos y programacion 1",4)
    'epksvmxqsw c tvskveqegmsr 5'

    >>> cifrado_cesar("epksvmxqsw c tvskveqegmsr 5",-4)
    'algoritmos y programacion 1'

    >>> cifrado_cesar("cifrado_cesar",17)
    'tzwiruf_tvjri'

    >>> cifrado_cesar("tzwiruf_tvjri",-17)
    'cifrado_cesar'

    >>> cifrado_cesar("mensajé_secreto N° 1222",18)
    'ewfksbw_kwujwlg F° 9000'

    >>> cifrado_cesar("ewfksbw_kwujwlg F° 9000",-18)
    'mensaje_secreto N° 1222'

    >>> cifrado_cesar("Hóla Este es mi menSaj3 secret0!",7)
    'Ovsh Lzal lz tp tluZhq0 zljyla7!'

    >>> cifrado_cesar("Ovsh Lzal lz tp tluZhq0 zljyla7!",-7)
    'Hola Este es mi menSaj3 secret0!'
    """

    LONGITUD_ALFABETO = 26
    LONGITUD_NUMEROS = 10

    mensaje_cifrado=""
    
    mensaje_a_analizar = normalizar_mensaje(mensaje)
    for caracter in mensaje_a_analizar:
        
        if caracter.isalpha():

            if caracter.islower():  
                nuevo_caracter = chr(ord("a") + ((ord(caracter)- ord("a")+clave) % LONGITUD_ALFABETO))  
            else:
                nuevo_caracter = chr(ord("A") + ((ord(caracter)- ord("A")+clave) % LONGITUD_ALFABETO))  

        elif caracter.isnumeric():
            nuevo_caracter = str((int(caracter)+clave)%LONGITUD_NUMEROS)
            
        else:
            nuevo_caracter = caracter

        mensaje_cifrado += nuevo_caracter

    return mensaje_cifrado


def boton_cifrado_cesar(inputMensaje, inputClave, resultado_text):
    mensaje = inputMensaje.get()
    clave = int(inputClave.get())
    mensaje_cifrado = cifrado_cesar(mensaje, clave)
    mostrar_resultado(resultado_text, "Texto cifrado (Cesar):", mensaje_cifrado)

def boton_descifrado_cesar(inputMensaje, inputClave, resultado_text):
    mensaje = inputMensaje.get()
    clave = int(inputClave.get())
    mensaje_descifrado = cifrado_cesar(mensaje, -clave)
    mostrar_resultado(resultado_text, "Texto descifrado (Cesar):", mensaje_descifrado)



def boton_ingreso(raiz,input_usuario, input_clave):
    usuario = input_usuario.get()
    clave = input_clave.get()

    if comprobar_usuario_clave_correctos(usuario,clave):
        raiz.destroy()
        interfaz_mensajes(usuario)
    else: 
        messagebox.showwarning("Non-existent identifier or wrong password","If you are not registered you must register first or if you forgot your password press the password recovery button")
        

def cargar_preguntas():
    lista = []

    archivo_preguntas=open("preguntas.csv")
    num_pregunta,pregunta =leer_preguntas(archivo_preguntas)

    while num_pregunta != "":
        lista.append(f" {num_pregunta}-{pregunta}")
        num_pregunta,pregunta =leer_preguntas(archivo_preguntas)
    
    return lista


def boton_registro(raiz):
    raiz.destroy()
    lista_preguntas = cargar_preguntas()
    interfaz_registro(lista_preguntas)

def boton_recuperacion_contraseña(raiz):
    raiz.destroy()
    lista_preguntas = cargar_preguntas()
    interfaz_recuperacion_contraseña(lista_preguntas)


def boton_recuperar_contraseña(raiz,input_usuario,combo_var,input_respuesta):
    usuario = input_usuario.get()
    id_pregunta_seguridad = combo_var.get().split("-")[0]
    respuesta = input_respuesta.get()

    terminar,exitoso = recuperar_contraseña(usuario,id_pregunta_seguridad,respuesta)

    if terminar:
        raiz.destroy()
        if exitoso:
            interfaz_login()
        else:
            interfaz_inicial()
            
def boton_ingresar_registro(raiz,input_usuario,input_contraseña,combo_var,input_respuesta):
    usuario = input_usuario.get()
    clave= input_contraseña.get()
    id_pregunta_seguridad = combo_var.get().split("-")[0]
    respuesta = input_respuesta.get()
    
    usuario_insertado = crear_usuario(usuario,clave,id_pregunta_seguridad, respuesta)
    
    if usuario_insertado:
        raiz.destroy()
        interfaz_login()


mensaje_cifrado_global = "" 

def boton_interfaz_login(raiz):
    raiz.destroy()
    interfaz_login()


def interfaz_inicial():
    raiz = Tk()
    raiz.title('Secret messages') 
    raiz.resizable(True, True)
    raiz.geometry("1024x768")
    raiz.iconbitmap("argentina.ico")
    raiz.config(bg="#9ED8F9")

    mi_frame = Frame(raiz,bg="#9ED8F9")
    mi_frame.config(bd=10,relief="groove")
    mi_frame.pack(pady=100)

    label_bienvenida = Label(mi_frame,font=('Courier',12),bg="#9ED8F9",text="Welcome to the secret messaging app.\n Press 'Login' to enter, or press 'Register' to create a new account.")
    label_bienvenida.grid(row=0,column=0,padx=10,pady=10, columnspan=2)

    boton_continuar = Button(mi_frame,text="Login",bg="#856ff8",command=lambda:boton_interfaz_login(raiz))
    boton_continuar.grid(row=1,column=0,pady=10,padx=(250, 5))

    boton_registrar = Button(mi_frame,text="Register",bg="#856ff8", command=lambda: boton_registro(raiz))
    boton_registrar.grid(row=1,column=1, pady=10, padx=(5, 250))

    label_integrantes = Label(mi_frame,font=('Courier',12),bg="#9ED8F9",text="Built by:\n \n Brian Agustín Conde \n Leandro Contestabile \n Matias Gonzalez Vieyra")
    label_integrantes.grid(row=2,column=0,pady=10,columnspan=2)

    raiz.mainloop()

def interfaz_login():
    raiz_login = Tk()
    raiz_login.title("Identification for access")
    raiz_login.resizable(True, True)
    raiz_login.geometry("1024x768")
    raiz_login.config(bg="#9ED8F9")
    frame_login = Frame(raiz_login,bg="#9ED8F9")
    frame_login.config(bd=10,relief="groove")
    frame_login.pack(pady=100)

    label_usuario = Label(frame_login,font=('Arial',12),bg="#9ED8F9",text="User:")
    label_usuario.grid(row=0,column=0,padx=5,pady=10)
    
    label_contraseña = Label(frame_login,font=('Arial',12),bg="#9ED8F9",text="Password:")
    label_contraseña.grid(row=1,column=0,padx=5,pady=10)
    
    input_usuario=Entry(frame_login, bd=7)
    input_usuario.grid(row=0,column=1,padx=10)
    
    input_contraseña=Entry(frame_login, bd=7)
    input_contraseña.grid(row=1,column=1,padx=10)

    frame_botones = Frame(raiz_login, bg="#9ED8F9")
    frame_botones.pack(pady=15)

    boton_ingresar = Button(frame_botones,text="Login",bg="#856ff8", bd=5, command=lambda: boton_ingreso(raiz_login,input_usuario,input_contraseña))
    boton_ingresar.grid(row=0,column=0, padx=5)


    boton_recuperar = Button(frame_botones,text="Retrieve",bg="#856ff8", bd=5, command=lambda: boton_recuperacion_contraseña(raiz_login))
    boton_recuperar.grid(row=0,column=2, padx=5)
    
    
    raiz_login.mainloop()

def interfaz_registro(lista_preguntas):
    raiz = Tk()
    raiz.title("Register")
    raiz.resizable(True, True)
    raiz.geometry("1024x768")
    raiz.config(bg="#9ED8F9")
    frame_registro = Frame(raiz,bg="#9ED8F9")
    frame_registro.config(bd=10,relief="groove")
    frame_registro.pack(pady=100)

    label_usuario = Label(frame_registro,font=('Arial',12),bg="#9ED8F9",text="User:")
    label_usuario.grid(row=0,column=0,padx=5,pady=10)
    
    label_contraseña = Label(frame_registro,font=('Arial',12),bg="#9ED8F9",text="Password:")
    label_contraseña.grid(row=1,column=0,padx=5,pady=10)

    label_pregunta = Label(frame_registro,font=('Arial',12),bg="#9ED8F9",text="Security question:")
    label_pregunta.grid(row=2,column=0,padx=5,pady=10)

    label_respuesta = Label(frame_registro,font=('Arial',12),bg="#9ED8F9",text="Answer:")
    label_respuesta.grid(row=3,column=0,padx=5,pady=10)
    
    input_usuario=Entry(frame_registro, bd=7)
    input_usuario.grid(row=0,column=1,padx=10)
    
    input_contraseña=Entry(frame_registro, bd=7)
    input_contraseña.grid(row=1,column=1,padx=10)

    combo_var = tk.StringVar()
    combobox = ttk.Combobox(frame_registro, textvariable=combo_var,values=lista_preguntas)
    combobox.grid(row=2,column=1,padx=10)

    input_respuesta=Entry(frame_registro, bd=7)
    input_respuesta.grid(row=3,column=1,padx=10)

    frame_botones = Frame(raiz, bg="#9ED8F9")
    frame_botones.pack(pady=15)

    boton_ingresar = Button(frame_botones,text="Login",bg="#856ff8", bd=5, command=lambda: boton_ingresar_registro(raiz,input_usuario,input_contraseña,combo_var,input_respuesta))
    boton_ingresar.grid(row=0,column=1, padx=5)


def interfaz_recuperacion_contraseña(lista_preguntas):
    raiz = Tk()
    raiz.title("Key Recovery")
    raiz.resizable(0,0)
    raiz.geometry("750x500")
    raiz.config(bg="#9ED8F9")
    frame_recuperar = Frame(raiz,bg="#9ED8F9")
    frame_recuperar.config(bd=10,relief="groove")
    frame_recuperar.pack(pady=100)

    label_usuario = Label(frame_recuperar,font=('Courier',12),bg="#9ED8F9",text="User:")
    label_usuario.grid(row=0,column=0,padx=5,pady=10)
    
    label_pregunta = Label(frame_recuperar,font=('Courier',12),bg="#9ED8F9",text="Security question:")
    label_pregunta.grid(row=2,column=0,padx=5,pady=10)

    label_respuesta = Label(frame_recuperar,font=('Courier',12),bg="#9ED8F9",text="Answer:")
    label_respuesta.grid(row=3,column=0,padx=5,pady=10)
    
    input_usuario=Entry(frame_recuperar)
    input_usuario.grid(row=0,column=1,padx=10)

    combo_var = tk.StringVar()
    combobox = ttk.Combobox(frame_recuperar, textvariable=combo_var,values=lista_preguntas)
    combobox.grid(row=2,column=1,padx=10)

    input_respuesta=Entry(frame_recuperar)
    input_respuesta.grid(row=3,column=1,padx=10)

    frame_botones = Frame(raiz, bg="#9ED8F9")
    frame_botones.pack(pady=15)

    boton_recuperar = Button(frame_botones,text="recovery",bg="#D5CF13", command=lambda: boton_recuperar_contraseña(raiz,input_usuario,combo_var,input_respuesta))
    boton_recuperar.grid(row=0,column=1, padx=5)

def cifrar_atbash(texto):
    texto_cifrado = cifrado_atbash(texto) 
    return texto_cifrado

def cifrar(inputMensaje, resultado_text):
    global mensaje_cifrado_global 
    mensaje = inputMensaje.get()
    mensaje_cifrado = cifrar_atbash(mensaje)
    mensaje_cifrado_global = mensaje_cifrado 
    mostrar_resultado(resultado_text, "Texto cifrado (Atbash):", mensaje_cifrado)

def consultar_mensajes(id_usuario):
    mensajes_generales = []
    mensajes_personales = []
    total_mensajes = 0

    with open("mensajes.csv", "r") as ar_mensajes:
        for linea in ar_mensajes:
            receptor, emisor, cifrado, mensaje_cifrado = linea.rstrip("\n").split(",")
            if (receptor == id_usuario):
                if (cifrado == "A"):
                    mensaje_descifrado = cifrado_atbash(mensaje_cifrado)
                    aux_mensaje = emisor +": " + mensaje_descifrado
                    mensajes_personales.append(aux_mensaje)
                else:
                    mensaje_descifrado = cifrado_cesar(mensaje_cifrado, -int(cifrado[1]))
                    aux_mensaje = emisor +": " + mensaje_descifrado
                    mensajes_personales.append(aux_mensaje)
                total_mensajes += 1
            elif (receptor == "*") and (emisor != id_usuario):
                if (cifrado == "A"):
                    mensaje_descifrado = cifrado_atbash(mensaje_cifrado)
                    aux_mensaje = "#" + emisor +": " + mensaje_descifrado
                    mensajes_generales.append(aux_mensaje)
                else:
                    mensaje_descifrado = cifrado_cesar(mensaje_cifrado, -int(cifrado[1]))
                    aux_mensaje = "#" + emisor +": " + mensaje_descifrado
                    mensajes_generales.append(aux_mensaje)
                total_mensajes += 1

    mensajes_usuario = mensajes_generales + mensajes_personales

    return mensajes_usuario, total_mensajes

def interfazConsulta(mensajes, cantidad):
    raiz = Tk()
    raiz.title('Secret Messages') 
    raiz.resizable(0, 0)
    raiz.geometry("750x500")
    raiz.iconbitmap("argentina.ico")
    raiz.config(bg="#9ED8F9")

    miFrame = Frame(raiz, bg="#9ED8F9")
    miFrame.config(bd=10, relief="groove")
    miFrame.pack(pady=100)

    labelLista = Label(miFrame, font=('Courier', 12), bg="#9ED8F9", text="List of messages:")
    labelLista.grid(row=0, column=0, padx=10, pady=10)

    lista = Listbox(miFrame, width=50, height=10)
    lista.grid(row=1, column=0, padx=10, pady=10)

    for mensaje in mensajes:
        lista.insert(END, mensaje)

    labelTotal = Label(miFrame, font=('Courier', 12), bg="#9ED8F9", text=f"Total messages: {cantidad}")
    labelTotal.grid(row=2, column=0, padx=10, pady=10)

    raiz.mainloop()
    
def boton_consulta(id_usuario):
    mensajes, cantidad = consultar_mensajes(id_usuario)
    interfazConsulta(mensajes, cantidad)

def interfaz_mensajes(id_usuario):
    raiz = Tk()
    raiz.title('Encrypting and sending messages') 
    raiz.resizable(True, True)
    raiz.geometry("1024x768")
    raiz.iconbitmap("argentina.ico")
    raiz.config(bg="#9ED8F9")

    miFrame = Frame(raiz, bg="#9ED8F9", bd=10, relief="groove")
    miFrame.pack(pady=(100, 0))

    destinatarioMensaje = Label(miFrame, font=('Georgia', 12), bg="#618282", text="Enter a valid recipient:")
    destinatarioMensaje.grid(row=0, column=0, padx=5, pady=10)

    inputDestinatario = Entry(miFrame, bd=7)
    inputDestinatario.grid(row=0, column=1, padx=10)

    TodosLosUsuarios = Label(miFrame, font=('Georgia', 12), bg="#618282", text="Enter * in case it is intended for all users.")
    TodosLosUsuarios.grid(row=0, column=2, padx=5, pady=10)

    labelMensaje = Label(miFrame, font=('Courier', 12), bg="#9ED8F9", text="Enter your message:")
    labelMensaje.grid(row=1, column=0, padx=5, pady=10)

    labelClave = Label(miFrame, font=('Courier', 12), bg="#9ED8F9", text="Enter key in Cesar's case:")
    labelClave.grid(row=2, column=0, padx=5, pady=10)

    inputMensaje = Entry(miFrame, bd=7)
    inputMensaje.grid(row=1, column=1, padx=10)

    inputClave = Entry(miFrame, bd=7)
    inputClave.grid(row=2, column=1, padx=10)

    frameBotones = Frame(raiz, bg="#9ED8F9")
    frameBotones.pack(pady=15)

    # Botones de cifrado Cesar
    botonCifrarCesar = Button(frameBotones, text="Encrypt Caesar", bg="#856ff8", bd=2, command=lambda: boton_cifrado_cesar(inputMensaje, inputClave, resultado_text))
    botonCifrarCesar.grid(row=0, column=0, padx=5)

    botonDescifrarCesar = Button(frameBotones, text="Decrypt Caesar", bg="#856ff8", bd=2, command=lambda: boton_descifrado_cesar(inputMensaje, inputClave, resultado_text))
    botonDescifrarCesar.grid(row=0, column=1, padx=5)

    # Botones de cifrado Atbash
    botonCifrarAtbash = Button(frameBotones, text="Encrypt Atbash", bg="#856ff8", bd=2, command=lambda: cifrar(inputMensaje, resultado_text))
    botonCifrarAtbash.grid(row=0, column=2, padx=5)

    botonDescifrarAtbash = Button(frameBotones, text="Decrypt Atbash", bg="#856ff8", bd=2, command=lambda: descifrar(inputMensaje, resultado_text))
    botonDescifrarAtbash.grid(row=0, column=3, padx=5)

    # Botones de envio
    botonEnviarCesar = Button(frameBotones, text="Send encrypted message Caesar", bg="#856ff8", bd=5, command=lambda: enviar_mensaje('C', inputDestinatario, id_usuario, inputMensaje, inputClave))
    botonEnviarCesar.grid(row=0, column=4, padx=5)

    botonEnviarAtbash = Button(frameBotones, text="Send Atbash encrypted message", bg="#856ff8", bd=5, command=lambda: enviar_mensaje('A', inputDestinatario, id_usuario, inputMensaje, None))
    botonEnviarAtbash.grid(row=0, column=5, padx=5)
    
    #Boton de consulta de mensajes
    botonConsultarMensajes = Button(frameBotones, text="Consult received messages", bg="#856ff8", bd=5, command=lambda: boton_consulta(id_usuario))
    botonConsultarMensajes.grid(row=0, column=6, padx=5)

    resultado_text = Text(miFrame, font=('Courier', 12), bg="white", height=5, width=40, state=DISABLED)
    resultado_text.grid(row=3, column=0, columnspan=3, padx=5, pady=10)

    raiz.mainloop()

def enviar_mensaje(cifrado, destinatario, remitente, mensaje, clave):
    destinatario = destinatario.get()
    mensaje_original = mensaje.get()
    clave = clave.get() if clave else None
    
    if destinatario == '*':
        # Enviar mensaje a todos los usuarios existentes
        with open('usuario_clave.csv', 'r', newline='', encoding='utf-8') as user_file:
            """reader = csv.reader(user_file)
            next(reader)  # Saltar la primera fila si contiene encabezados
            for row in reader:
                usuario = row[0]  # Ajusta el indice según la posición de la columna de usuarios en el CSV
                cifrar_y_guardar_mensaje(cifrado, usuario, mensaje_original, clave, remitente)"""
        
        cifrar_y_guardar_mensaje(cifrado, "*", mensaje_original, clave, remitente)
        print(f"Encrypted message ({cifrado}) sent to all users and saved in mensajes.csv")
    elif comprobar_solo_usuario(destinatario):
        # Enviar mensaje al destinatario específico
        cifrar_y_guardar_mensaje(cifrado, destinatario, mensaje_original, clave, remitente)
        
        print(f"Encrypted message  ({cifrado}) sent to {destinatario} and saved in mensajes.csv")
    else:
        messagebox.showwarning("Nonexistent identification", "Nonexistent identification")

def cifrar_y_guardar_mensaje(cifrado, destinatario, mensaje_original, clave, remitente):
    if cifrado == 'C':
        mensaje_cifrado = cifrado_cesar(mensaje_original, int(clave))
        cifrado = 'C' + str(clave)
    elif cifrado == 'A':
        mensaje_cifrado = cifrado_atbash(mensaje_original)
    else:
        print("Type of encryption not valid")
        return

    with open('mensajes.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([destinatario, remitente, cifrado, mensaje_cifrado]) 


def mostrar_resultado(texto_cuadro, titulo, texto):
    texto_cuadro.config(state=NORMAL)
    texto_cuadro.delete(1.0, END)
    texto_cuadro.insert(INSERT, titulo)
    texto_cuadro.insert(INSERT, "\n")
    texto_cuadro.insert(INSERT, texto)
    texto_cuadro.config(state=DISABLED)

interfaz_inicial()
















