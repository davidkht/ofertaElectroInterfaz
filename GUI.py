import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import sp

def on_validate(P):
    # P es el valor propuesto para el texto del Entry: acepta si es vacío (lo que permite borrar) o si es numérico
    return P == "" or P.isdigit()

def browse_file():
    filename = filedialog.askopenfilename()
    comercial= sp.encontrar_pdf_y_extraer_nombre(filename)
    if comercial:
        controlLabel.set(comercial)
        variableControl.set(filename)
    else:
        messagebox.showerror("¡Error!","¡Debe seleccionar un FSC!")

root = tk.Tk()
root.title("Crear Oferta")

# Layout configuration
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)

# Frame for the left side inputs
left_frame = tk.Frame(root)
left_frame.grid(row=0, column=0, sticky="nwes", padx=10, pady=10)

#######################################################
#SECCION COMERCIAL#
#######################################################

commercial_label = tk.Label(left_frame,text='Comercial/KAM: ')

commercial_label.grid(row=3, column=0, columnspan=2, sticky="w",pady=(0, 10))

# "Selecciona FSC" label and input
variableControl = tk.StringVar()
tk.Label(left_frame, text="Selecciona FSC").grid(row=1, column=0, sticky="w")


fsc_entry = tk.Entry(left_frame,textvariable=variableControl , state='readonly')
fsc_entry.grid(row=2, column=0, sticky="ew", pady=(0, 10))

controlLabel=tk.StringVar()
controlLabel.set('')
com_entry = tk.Entry(left_frame,textvariable=controlLabel , state='readonly')
com_entry.grid(row=3, column=1, sticky="ew", pady=(0, 10))

examine_button = tk.Button(left_frame, text="Examinar", command=browse_file)
examine_button.grid(row=2, column=1, padx=10, pady=(0, 10))

#########################################################
#SECCION ENCABEZADO
#########################################################


valores_para_listas=[['Q3-2024','Q4-2024','Q1-2025','Q2-2025','Q3-2025','Q4-2025']]
vcmd = (root.register(on_validate), '%P')
labels = ["Improvistos:", "Estampillas:", "Trimestre Esperado:", "Ciudad:", "Institución:"]
for i, label in enumerate(labels, 4):
    tk.Label(left_frame, text=label).grid(row=i, column=0, sticky="w",pady=(0, 10))
    if i < 6:
        entry = tk.Entry(left_frame,validate='key',validatecommand=vcmd)
        entry.grid(row=i, column=1, sticky="ew", pady=(0, 10))
    else:
        combobox = ttk.Combobox(left_frame)
        combobox.grid(row=i, column=1, sticky="ew", pady=(0, 10))



# Start the application
root.mainloop()