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

def move_to_selected():
    selected = ref_listbox.curselection()
    for i in selected:
        selected_listbox.insert(tk.END, ref_listbox.get(i))
        ref_listbox.delete(i)

def move_to_references():
    selected = selected_listbox.curselection()
    for i in selected:
        ref_listbox.insert(tk.END, selected_listbox.get(i))
        selected_listbox.delete(i)

root = tk.Tk()
root.title("Crear Oferta")

root.tk.call("source", r"C:\Users\K\Documents\Proyectos\Forest-ttk-theme\forest-dark.tcl")
# Create a style
style = ttk.Style(root)
# Set the theme with the theme_use method
style.theme_use("forest-dark")

# Layout configuration
root.grid_rowconfigure(1, weight=2)
root.grid_columnconfigure(1, weight=2)

# Frame for the left side inputs
left_frame = ttk.Frame(root)
left_frame.grid(row=0, column=0, sticky="nwes", padx=10, pady=10)

#######################################################
#SECCION COMERCIAL#
#######################################################

commercial_label = tk.Label(left_frame,text='Comercial/KAM: ')

commercial_label.grid(row=3, column=0, columnspan=2, sticky="w",pady=(0, 10))

# "Selecciona FSC" label and input
variableControl = tk.StringVar()
ttk.Label(left_frame, text="Selecciona FSC").grid(row=1, column=0, sticky="w")


fsc_entry = ttk.Entry(left_frame,textvariable=variableControl , state='readonly')
fsc_entry.grid(row=2, column=0, sticky="ew", pady=(0, 10))

controlLabel=tk.StringVar()
controlLabel.set('')
com_entry = ttk.Entry(left_frame,textvariable=controlLabel , state='readonly')
com_entry.grid(row=3, column=1, sticky="ew", pady=(0, 10))

examine_button = ttk.Button(left_frame, text="Examinar", command=browse_file,style="ToggleButton")
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
        entry = ttk.Entry(left_frame,validate='key',validatecommand=vcmd)
        entry.grid(row=i, column=1, sticky="ew", pady=(0, 10))
    else:
        combobox = ttk.Combobox(left_frame)
        combobox.grid(row=i, column=1, sticky="ew", pady=(0, 10))


#########################################################
#SECCION REFERENCIAS
#########################################################

right_frame = ttk.Frame(root)
right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

right_frame.grid_columnconfigure(0, weight=1)
ttk.Label(right_frame, text="Referencias").grid(row=0, column=0, pady=(0, 10))
search_entry = ttk.Entry(right_frame)
search_entry.grid(row=1, column=0, sticky="ew", pady=(0, 10))

# Listboxes with scrollbar
listbox_frame = ttk.Frame(right_frame)
listbox_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
right_frame.grid_rowconfigure(2, weight=1)

scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical")
scrollbar.grid(row=0, column=1, sticky="ns")


ref_listbox = tk.Listbox(listbox_frame, exportselection=False, yscrollcommand=scrollbar.set)
ref_listbox.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
scrollbar.config(command=ref_listbox.yview)

selected_listbox = tk.Listbox(listbox_frame, exportselection=False)
selected_listbox.grid(row=0, column=2, sticky="nsew", pady=(0, 10))

#Buttons to move items between listboxes
btn_frame = ttk.Frame(listbox_frame)
btn_frame.grid(row=0, column=1, sticky="ns")

move_to_selected_button = ttk.Button(btn_frame, text=" -> ", command=move_to_selected, width=5,style="Accent.TButton")
move_to_selected_button.pack()

move_to_references_button = ttk.Button(btn_frame, text=" <- ", command=move_to_references, width=5,style="Accent.TButton")
move_to_references_button.pack()


# Start the application
root.mainloop()