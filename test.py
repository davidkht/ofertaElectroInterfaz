import tkinter as tk

root = tk.Tk()
root.geometry("300x200")  # Tamaño inicial de la ventana

# Configurando las filas y columnas para que se expandan
for i in range(2):  # Asumiendo que tienes 2 filas y 2 columnas
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)

# Creando y agregando widgets
widget1 = tk.Label(root, text="Widget 1", bg="red")
widget1.grid(row=0, column=0, sticky='nsew')

widget2 = tk.Label(root, text="Widget 2", bg="green")
widget2.grid(row=0, column=1, sticky='nsew')

widget3 = tk.Label(root, text="Widget 3", bg="blue")
widget3.grid(row=1, column=0, sticky='nsew')

widget4 = tk.Label(root, text="Widget 4", bg="yellow")
widget4.grid(row=1, column=1, sticky='nsew')

root.mainloop()
