import mysql.connector
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

conn = mysql.connector.connect(
    host='localhost', 
    user='root',  
    password='', 
    database='oxxo',
    port="3306" 
)
cursor = conn.cursor()

def mostrar_carrito():
    for widget in frame_contenido.winfo_children():
        widget.pack_forget()

    frame_carrito = Frame(frame_contenido, bg="white")
    frame_carrito.pack(fill=BOTH, expand=True, pady=20, padx=20)

    titulo = Label(frame_carrito, text="Carrito de Compras", font=("Arial", 20, "bold"), bg="white")
    titulo.pack(pady=10)

    cursor.execute('''
    SELECT p.nombre, p.precio
    FROM carrito c
    JOIN productos p ON c.producto_id = p.id
    ''')
    items_carrito = cursor.fetchall()

    if not items_carrito:
        mensaje_vacio = Label(frame_carrito, text="Tu carrito está vacío", font=("Arial", 15), bg="white")
        mensaje_vacio.pack(pady=10)
    else:
        for nombre, precio in items_carrito:
            label_producto = Label(frame_carrito, text=f"{nombre} - ${precio}", font=("Arial", 15), bg="white")
            label_producto.pack(pady=5)
        
        boton_comprar = Button(frame_carrito, text="Comprar", command=calcular_total)
        boton_comprar.pack(pady=5)

def calcular_total():
    cursor.execute('''
    SELECT SUM(p.precio)
    FROM carrito c
    JOIN productos p ON c.producto_id = p.id
    ''')
    total = cursor.fetchone()[0]
    messagebox.showinfo("Total de la Compra", f"El total de tu compra es: ${total}")

def añadir(producto_id):
    cursor.execute('INSERT INTO carrito (producto_id) VALUES (%s)', (producto_id,))
    conn.commit()
    messagebox.showinfo("Éxito", "El producto se ha añadido al carrito correctamente")

def productos():
    for widget in frame_contenido.winfo_children():
        widget.pack_forget()

    cursor.execute('SELECT id, nombre, precio FROM productos')
    productos = cursor.fetchall()

    canvas = Canvas(frame_contenido, bg="white")
    scrollbar = Scrollbar(frame_contenido, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="white")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    titulo = Label(scrollable_frame, text="Productos Disponibles", font=("Arial", 20, "bold"), bg="red", fg="gold")
    titulo.pack(pady=10)

    for producto_id, nombre, precio in productos:
        frame_actividad = Frame(scrollable_frame, bg="red", bd=2, relief=SOLID)
        frame_actividad.pack(pady=10, fill=X, padx=10)

        label_actividad = Label(frame_actividad, text=f"{nombre} - ${precio}", font=("Arial", 15), bg="red")
        label_actividad.pack(side=LEFT, padx=10, pady=10)

        boton_registro = Button(frame_actividad, text="Añadir al carrito", bg="red", fg="white", font=("Arial", 12, "bold"), command=lambda p=producto_id: añadir(p))
        boton_registro.pack(side=RIGHT, padx=10, pady=10)

def mostrar_inicio():
    for widget in frame_contenido.winfo_children():
        widget.pack_forget()

    label_novedades = Label(frame_contenido, text="Oxxo", bg='red', font=("Arial", 19))
    label_novedades.pack(pady=10)

    texto_novedades = "¡Bienvenidos! Aquí encontrarás las últimas novedades del Oxxo."
    label_contenido_novedades = Label(frame_contenido, text=texto_novedades, bg='red', wraplength=480, justify=LEFT, font=("Arial", 13))
    label_contenido_novedades.pack(pady=10)

    lbl_imagen1.pack(side=LEFT, padx=5)
    lbl_imagen2.pack(side=LEFT, padx=5)
    lbl_imagen3.pack(side=LEFT, padx=5)

def mostrar_formulario_añadir():
    for widget in frame_contenido.winfo_children():
        widget.pack_forget()

    frame_formulario = Frame(frame_contenido, bg="white")
    frame_formulario.pack(fill=BOTH, expand=True, pady=20, padx=20)

    titulo = Label(frame_formulario, text="Añadir Producto", font=("Arial", 20, "bold"), bg="white")
    titulo.pack(pady=10)

    Label(frame_formulario, text="Nombre del producto:", font=("Arial", 15), bg="white").pack(pady=5)
    entry_nombre = Entry(frame_formulario, font=("Arial", 15), bg="white")
    entry_nombre.pack(pady=5)

    Label(frame_formulario, text="Precio del producto:", font=("Arial", 15), bg="white").pack(pady=5)
    entry_precio = Entry(frame_formulario, font=("Arial", 15), bg="white")
    entry_precio.pack(pady=5)

    def guardar_producto():
        nombre = entry_nombre.get()
        precio = float(entry_precio.get())

        cursor.execute('INSERT INTO productos (nombre, precio) VALUES (%s, %s)', (nombre, precio))
        conn.commit()
        messagebox.showinfo("Éxito", "El producto se ha añadido correctamente")

    Button(frame_formulario, text="Guardar", bg="red", fg="white", font=("Arial", 12, "bold"), command=guardar_producto).pack(pady=10)

pagina = Tk()
pagina.title("Oxxo")
pagina.geometry("500x300")
pagina.configure(bg='gold')
pagina.resizable(False, False)

menu_bar = Menu(pagina)
pagina.config(menu=menu_bar)

menu_opciones = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Opciones", menu=menu_opciones)
menu_opciones.add_command(label="Ver productos", command=productos)
menu_opciones.add_command(label="Ver carrito", command=mostrar_carrito)
menu_opciones.add_command(label="Añadir producto", command=mostrar_formulario_añadir)
menu_bar.add_command(label="Inicio", command=mostrar_inicio)

frame_contenido = Frame(pagina, bg='red')
frame_contenido.pack(expand=True, fill='both', padx=10, pady=10)


imagen1 = ImageTk.PhotoImage(Image.open("oxxo2.jpg").resize((150, 100), Image.LANCZOS))
imagen2 = ImageTk.PhotoImage(Image.open("oxxo3.jpg").resize((150, 100), Image.LANCZOS))
imagen3 = ImageTk.PhotoImage(Image.open("oxxo1.png").resize((150, 100), Image.LANCZOS))

lbl_imagen1 = Label(frame_contenido, image=imagen1, bg='white')
lbl_imagen2 = Label(frame_contenido, image=imagen2, bg='white')
lbl_imagen3 = Label(frame_contenido, image=imagen3, bg='white')

mostrar_inicio()

pagina.mainloop()
