import tkinter as tk
from tkinter import Menu, PhotoImage, Toplevel, Button

# Variables globales
imagen_a_insertar = None
imagen_cambiada = False
puntos_canvas = []
elementos_insertados = []

def archivo_nuevo():
    print("Archivo nuevo seleccionado")

def cargar_archivo():
    print("Cargar archivo seleccionado")

def salir():
    root.quit()

def cambiar_imagen_boton1():
    global imagen_cambiada, boton1
    if not imagen_cambiada:
        boton1.config(image=img2)
        imagen_cambiada = True
        canvas.unbind("<Button-1>")  # Desvincula la capacidad de insertar imágenes
    else:
        boton1.config(image=img1)
        imagen_cambiada = False
        canvas.bind("<Button-1>", lambda event: insertar_imagen_click(event, img1, insertar_cuadro_abajo))

def cambiar_imagen_boton5():
    global imagen_cambiada, boton5
    if not imagen_cambiada:
        boton5.config(image=img7)  # Cambia a la nueva imagen img7
        imagen_cambiada = True
        canvas.unbind("<Button-1>")  # Desvincula la capacidad de insertar imágenes
    else:
        boton5.config(image=img6)  # Cambia de vuelta a la nueva imagen img6
        imagen_cambiada = False
        canvas.bind("<Button-1>", lambda event: insertar_imagen_click(event, img6, insertar_cuadro_abajo))

def preparar_insercion_imagen(imagen, cuadros_func):
    global imagen_a_insertar, imagen_cambiada, cuadros_alrededor
    if not imagen_cambiada:
        imagen_a_insertar = imagen  # Definir la imagen que se insertará al hacer clic
        cuadros_alrededor = cuadros_func  # Definir cómo se insertarán los cuadros
        canvas.bind("<Button-1>", lambda event: insertar_imagen_click(event, imagen, cuadros_func))
        canvas.bind("<Motion>", seguir_cursor_con_imagen)

def insertar_imagen_click(event, imagen, cuadros_func):
    global imagen_a_insertar
    if imagen_a_insertar:
        x, y = event.x, event.y
        punto_mas_cercano = min(puntos_canvas, key=lambda p: (p[0] - x) ** 2 + (p[1] - y) ** 2)
        
        # Insertar la imagen y asociarla con un tag único
        item_id = canvas.create_image(punto_mas_cercano[0], punto_mas_cercano[1], image=imagen, tags=("imagen",))
        elementos_insertados.append(item_id)
        canvas.tag_bind(item_id, "<Button-1>", lambda e, id=item_id: mostrar_ventana_opciones(id))
        
        # Insertar cuadros y asociarlos con el mismo tag
        cuadros_func(punto_mas_cercano[0], punto_mas_cercano[1], item_id)
        
        canvas.unbind("<Motion>")  # Dejar de seguir al cursor
        imagen_a_insertar = None  # Reiniciar la variable para desactivar la inserción

def seguir_cursor_con_imagen(event):
    global imagen_a_insertar
    if imagen_a_insertar:
        canvas.delete("cursor_image")
        x, y = event.x, event.y
        punto_mas_cercano = min(puntos_canvas, key=lambda p: (p[0] - x) ** 2 + (p[1] - y) ** 2)
        canvas.create_image(punto_mas_cercano[0], punto_mas_cercano[1], image=imagen_a_insertar, tags="cursor_image")

def mostrar_ventana_opciones(item_id):
    # Crear una ventana emergente
    ventana_opciones = Toplevel(root)
    ventana_opciones.title("Opciones")
    
    # Botón para borrar la imagen
    boton_borrar = Button(ventana_opciones, text="Borrar", command=lambda: borrar_imagen(item_id, ventana_opciones))
    boton_borrar.pack(pady=10)
    
    # Botón para aceptar y cerrar la ventana sin hacer nada
    boton_aceptar = Button(ventana_opciones, text="Aceptar", command=ventana_opciones.destroy)
    boton_aceptar.pack(pady=10)

def borrar_imagen(item_id, ventana):
    # Borrar la imagen y los cuadros asociados del canvas
    canvas.delete(item_id)
    canvas.delete("cuadro_" + str(item_id))
    elementos_insertados.remove(item_id)
    ventana.destroy()

def insertar_cuadro_abajo(x, y, item_id):
    cuadro_tamano = 5
    offset = 20  # La mitad del tamaño de la imagen (40px / 2)
    
    # Cuadro debajo de la imagen
    canvas.create_rectangle(x - cuadro_tamano/2, y + offset + 5, 
                            x + cuadro_tamano/2, y + offset + 5 + cuadro_tamano, 
                            fill="red", tags=("cuadro_" + str(item_id),))

def insertar_cuadro_arriba(x, y, item_id):
    cuadro_tamano = 5
    offset = 20  # La mitad del tamaño de la imagen (40px / 2)
    
    # Cuadro arriba de la imagen
    canvas.create_rectangle(x - cuadro_tamano/2, y - offset - 5 - cuadro_tamano, 
                            x + cuadro_tamano/2, y - offset - 5, 
                            fill="red", tags=("cuadro_" + str(item_id),))

def insertar_cuadros_izquierda_derecha_abajo(x, y, item_id):
    cuadro_tamano = 5
    offset = 20  # La mitad del tamaño de la imagen (40px / 2)
    
    # Cuadro a la izquierda de la imagen
    canvas.create_rectangle(x - offset - 5 - cuadro_tamano, y - cuadro_tamano/2, 
                            x - offset - 5, y + cuadro_tamano/2, 
                            fill="red", tags=("cuadro_" + str(item_id),))
    
    # Cuadro a la derecha de la imagen
    canvas.create_rectangle(x + offset + 5, y - cuadro_tamano/2, 
                            x + offset + 5 + cuadro_tamano, y + cuadro_tamano/2, 
                            fill="red", tags=("cuadro_" + str(item_id),))
    
    # Cuadro debajo de la imagen
    canvas.create_rectangle(x - cuadro_tamano/2, y + offset + 5, 
                            x + cuadro_tamano/2, y + offset + 5 + cuadro_tamano, 
                            fill="red", tags=("cuadro_" + str(item_id),))

def ajustar_canvas(event):
    global puntos_canvas
    canvas.delete("all")
    puntos_canvas.clear()

    # Obtener el tamaño actual del canvas
    canvas_width = event.width
    canvas_height = event.height

    # Dibujar puntos cada 10px en el canvas y almacenar sus posiciones
    for x in range(0, canvas_width, 10):
        for y in range(0, canvas_height, 10):
            canvas.create_oval(x, y, x+1, y+1, fill="black", outline="black")
            puntos_canvas.append((x, y))

# Crear la ventana principal
root = tk.Tk()
root.title("Mi Aplicación")

# Configurar ventana maximizada
root.state('zoomed')

# Crear la barra de menú
menu_bar = Menu(root)

# Crear el menú de archivo
archivo_menu = Menu(menu_bar, tearoff=0)
archivo_menu.add_command(label="Archivo nuevo", command=archivo_nuevo)
archivo_menu.add_command(label="Cargar", command=cargar_archivo)
archivo_menu.add_separator()
archivo_menu.add_command(label="Salir", command=salir)

# Agregar el menú de archivo a la barra de menú
menu_bar.add_cascade(label="Archivo", menu=archivo_menu)

# Configurar la barra de menú
root.config(menu=menu_bar)

# Crear un frame para los botones
frame_botones = tk.Frame(root)
frame_botones.grid(row=1, column=0, sticky="w", padx=10, pady=10)

# Cargar las imágenes
img1 = PhotoImage(file="./Img/Run.png")  # Imagen Run
img2 = PhotoImage(file="./Img/Stop.png")  # Imagen Stop
img3 = PhotoImage(file="./Img/Gas.png")  # Imagen Generador
img4 = PhotoImage(file="./Img/Carga.png")  # Imagen Carga
img5 = PhotoImage(file="./Img/T.png")  # Imagen T
img6 = PhotoImage(file="./Img/Tuberia_1.png")  # Imagen Tuberia
img7 = PhotoImage(file="./Img/Tuberia_2.png")  # Nueva Imagen para boton5

# Crear los botones
boton1 = tk.Button(frame_botones, image=img1, command=cambiar_imagen_boton1)
boton1.grid(row=0, column=0, padx=5, pady=5)

boton2 = tk.Button(frame_botones, image=img3, command=lambda: preparar_insercion_imagen(img3, insertar_cuadro_abajo))
boton2.grid(row=0, column=1, padx=5, pady=5)

boton3 = tk.Button(frame_botones, image=img4, command=lambda: preparar_insercion_imagen(img4, insertar_cuadro_arriba))
boton3.grid(row=0, column=2, padx=5, pady=5)

boton4 = tk.Button(frame_botones, image=img5, command=lambda: preparar_insercion_imagen(img5, insertar_cuadros_izquierda_derecha_abajo))
boton4.grid(row=0, column=3, padx=5, pady=5)

boton5 = tk.Button(frame_botones, image=img6, command=cambiar_imagen_boton5)
boton5.grid(row=0, column=4, padx=5, pady=5)

# Crear un Canvas que cubra el resto de la ventana
canvas = tk.Canvas(root, bg="white")
canvas.grid(row=2, column=0, sticky="nsew")

# Hacer que el canvas cubra todo el espacio disponible
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

# Ajustar el canvas al tamaño de la ventana en tiempo real
canvas.bind("<Configure>", ajustar_canvas)

# Iniciar el bucle principal de la aplicación
root.mainloop()
