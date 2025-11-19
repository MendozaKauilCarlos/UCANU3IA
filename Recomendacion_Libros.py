import json
import tkinter as tk
from tkinter import ttk, messagebox

libros = []

# ==========================
# CARGA Y GUARDADO DE DATOS
# ==========================

def cargar_datos():
    global libros
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            libros = json.load(f)
    except:
        messagebox.showerror("Error", "No se pudo cargar data.json")

def guardar_sugerencia(texto, libro):
    try:
        with open("sugerencias.txt", "a", encoding="utf-8") as f:
            f.write(f"Libro seleccionado: {libro}\n")
            f.write(f"Sugerencia del usuario: {texto}\n")
            f.write("---\n\n")
        messagebox.showinfo("Guardado", "Sugerencia guardada correctamente.")
    except:
        messagebox.showerror("Error", "No se pudo guardar la sugerencia.")


# ==========================
# FUNCIONES DE RECOMENDACIÓN
# ==========================

def recomendar_por_etiquetas(libro_seleccionado):
    libro = next((l for l in libros if l["titulo"] == libro_seleccionado), None)
    base_et = set(libro["etiquetas"])

    similares = []
    for otro in libros:
        if otro["id"] == libro["id"]:
            continue
        if base_et.intersection(otro["etiquetas"]):
            similares.append(otro["titulo"])

    return similares


def recomendar_por_popularidad(libro_seleccionado):
    libro = next((l for l in libros if l["titulo"] == libro_seleccionado), None)
    base_et = set(libro["etiquetas"])

    recomendados = []
    for otro in libros:
        if otro["id"] == libro["id"]:
            continue
        if base_et.intersection(otro["etiquetas"]):
            prom = sum(otro["puntuaciones"]) / len(otro["puntuaciones"])
            recomendados.append((otro["titulo"], prom))

    return sorted(recomendados, key=lambda x: x[1], reverse=True)


# ==========================
# INTERFAZ GRÁFICA (Tkinter)
# ==========================

def mostrar_detalles(event=None):
    seleccion = combo_libros.get()
    if not seleccion:
        return

    libro = next((l for l in libros if l["titulo"] == seleccion), None)
    etiquetas_lbl.config(text=", ".join(libro["etiquetas"]))

    prom = sum(libro["puntuaciones"]) / len(libro["puntuaciones"])
    promedio_lbl.config(text=f"{prom:.2f}")


def boton_similares():
    seleccion = combo_libros.get()
    if not seleccion:
        return
    
    resultados_text.delete(1.0, tk.END)
    resultados = recomendar_por_etiquetas(seleccion)

    if not resultados:
        resultados_text.insert(tk.END, "No hay recomendaciones similares.")
    else:
        resultados_text.insert(tk.END, "\n".join(resultados))


def boton_popularidad():
    seleccion = combo_libros.get()
    if not seleccion:
        return
    
    resultados_text.delete(1.0, tk.END)
    resultados = recomendar_por_popularidad(seleccion)

    if not resultados:
        resultados_text.insert(tk.END, "No hay recomendaciones populares.")
    else:
        for titulo, prom in resultados:
            resultados_text.insert(tk.END, f"{titulo} - {prom:.2f}\n")


def boton_guardar_sugerencia():
    texto = sugerencia_entry.get("1.0", tk.END).strip()
    libro = combo_libros.get()

    if not texto:
        messagebox.showwarning("Aviso", "No puedes guardar una sugerencia vacía.")
        return

    guardar_sugerencia(texto, libro)
    sugerencia_entry.delete("1.0", tk.END)


# ==========================
# CONSTRUCCIÓN DE LA GUI
# ==========================

root = tk.Tk()
root.title("Sistema de Recomendación de Libros")

# Selección de libros
ttk.Label(root, text="Selecciona un libro:").pack()
combo_libros = ttk.Combobox(root, width=40, state="readonly")
combo_libros.pack()
combo_libros.bind("<<ComboboxSelected>>", mostrar_detalles)

# Detalles
frame = ttk.Frame(root)
frame.pack(pady=10)

ttk.Label(frame, text="Etiquetas:").grid(row=0, column=0, sticky="w")
etiquetas_lbl = ttk.Label(frame, text="")
etiquetas_lbl.grid(row=0, column=1)

ttk.Label(frame, text="Promedio:").grid(row=1, column=0, sticky="w")
promedio_lbl = ttk.Label(frame, text="")
promedio_lbl.grid(row=1, column=1)

# Botones
ttk.Button(root, text="Recomendar por etiquetas", command=boton_similares).pack(pady=3)
ttk.Button(root, text="Recomendar por popularidad", command=boton_popularidad).pack(pady=3)

# Resultados
ttk.Label(root, text="Resultados:").pack()
resultados_text = tk.Text(root, width=60, height=12)
resultados_text.pack()

# Sugerencias del usuario
ttk.Label(root, text="Tu recomendación para mejorar:").pack(pady=5)
sugerencia_entry = tk.Text(root, width=60, height=4)
sugerencia_entry.pack()

ttk.Button(root, text="Guardar sugerencia", command=boton_guardar_sugerencia).pack(pady=5)

# Iniciar
cargar_datos()
combo_libros["values"] = [l["titulo"] for l in libros]

root.mainloop()
