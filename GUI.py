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
root.geometry("1350x400")
root.resizable(False,False)
root.iconbitmap(r"C:\Users\K\Documents\Proyectos\ofertaElectroInterfaz\imagen.ico")


colordefondo='#2b394a'
foregroundvariable='grey85'
root.configure(background=colordefondo)
# Configurar un estilo para los labels
style = ttk.Style()
style.configure("Large.TLabel", font=("Arial", 14), foreground=foregroundvariable,
                background=colordefondo)

style.configure('Custom.TFrame', foreground=foregroundvariable,
                background=colordefondo)

style.configure('Custom.TRadiobutton', font=('Arial', 14), foreground=foregroundvariable,
                background=colordefondo)

style.configure("Bold.TLabel", font=("Arial", 18,'bold'), foreground=foregroundvariable,
                background=colordefondo)

style.configure("dis.TLabel", font=("Arial", 18,'bold'), foreground='grey50',
                background=colordefondo)

style.configure('Custom.TButton', font=('Arial', 13,'bold'), 
                foreground='grey15',background=colordefondo)

style.configure('Custom.TEntry', 
                font=('Arial', 25), 
                fieldbackground='black', 
                foreground='black', 
                background=colordefondo)
style.configure("Switch.TCheckbutton", background=colordefondo, 
                foreground=foregroundvariable)

# root.tk.call("source", r"C:\Users\K\Documents\Proyectos\Forest-ttk-theme\forest-dark.tcl")
# # Create a style
# style = ttk.Style(root)
# # Set the theme with the theme_use method
# style.theme_use("forest-dark")

# Layout configuration
root.grid_rowconfigure(0, weight=2)
root.grid_columnconfigure(0, weight=2)
root.grid_rowconfigure(1, weight=2)
root.grid_columnconfigure(1, weight=5)
root.grid_columnconfigure(2, weight=2)


# Frame for the left side inputs
left_frame = ttk.Frame(root,style='Custom.TFrame')
left_frame.grid(row=0, column=0, sticky="nwes", padx=10, pady=10)
left_frame.grid_rowconfigure(0,weight=1)
left_frame.grid_rowconfigure(1,weight=1)
left_frame.grid_rowconfigure(2,weight=1)
left_frame.grid_rowconfigure(3,weight=1)
left_frame.grid_rowconfigure(4,weight=1)
left_frame.grid_rowconfigure(5,weight=1)
left_frame.grid_rowconfigure(6,weight=1)
left_frame.grid_rowconfigure(7,weight=1)
left_frame.grid_rowconfigure(8,weight=1)
left_frame.grid_rowconfigure(9,weight=1)
left_frame.grid_columnconfigure(0,weight=1)
left_frame.grid_columnconfigure(1,weight=1)

#######################################################
#SECCION COMERCIAL#
#######################################################

commercial_label = ttk.Label(left_frame,text='Comercial/KAM: ',style="Large.TLabel")

commercial_label.grid(row=3, column=0, columnspan=2, sticky="w",pady=(0, 10))

# "Selecciona FSC" label and input
variableControl = tk.StringVar()
fsc=ttk.Label(left_frame, text="Selecciona FSC",style="Bold.TLabel")
fsc.grid(row=1, column=0, sticky="ew")


fsc_entry = ttk.Entry(left_frame,textvariable=variableControl , state='readonly',style='Custom.TEntry')
fsc_entry.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 10))

controlLabel=tk.StringVar()
controlLabel.set('')
com_entry = ttk.Entry(left_frame,textvariable=controlLabel , state='readonly',style='Custom.TEntry')
com_entry.grid(row=3, column=1, sticky="ew", pady=(0, 10))

examine_button = ttk.Button(left_frame, text="Examinar",command=browse_file,style="Custom.TButton")
examine_button.grid(row=1, column=1, sticky='ew',pady=(0, 10))

#########################################################
#SECCION ENCABEZADO
#########################################################


valores_para_listas=[['Q3-2024','Q4-2024','Q1-2025','Q2-2025','Q3-2025','Q4-2025']]
vcmd = (root.register(on_validate), '%P')
labels = ["Improvistos:", "Estampillas:", "Trimestre Esperado:", "Ciudad:", "Institución:"]
for i, label in enumerate(labels, 4):
    ttk.Label(left_frame, text=label,style="Large.TLabel").grid(row=i, column=0, sticky="w",pady=(0, 10))
    if i < 6:
        entry = ttk.Entry(left_frame,validate='key',validatecommand=vcmd,style='Custom.TEntry')
        entry.grid(row=i, column=1, sticky="ew", pady=(0, 10))
    else:
        combobox = ttk.Combobox(left_frame)
        combobox.grid(row=i, column=1, sticky="ew", pady=(0, 10))


#########################################################
#SECCION REFERENCIAS
#########################################################

right_frame = ttk.Frame(root,style='Custom.TFrame')
right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
right_frame.grid_rowconfigure(2, weight=1)
right_frame.grid_rowconfigure(1, weight=1)
right_frame.grid_rowconfigure(0, weight=1)
right_frame.grid_rowconfigure(3, weight=1)
right_frame.grid_columnconfigure(0, weight=1)
ttk.Label(right_frame, text="Referencias",style="Bold.TLabel").grid(row=0, column=0)
search_entry = ttk.Entry(right_frame)
search_entry.grid(row=1, column=0, sticky="ew")

# Listboxes with scrollbar
listbox_frame = ttk.Frame(right_frame,style='Custom.TFrame')
listbox_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(10, 10))

listbox_frame.grid_rowconfigure(0,weight=1)
listbox_frame.grid_columnconfigure(0,weight=1)
listbox_frame.grid_columnconfigure(1,weight=0)
listbox_frame.grid_columnconfigure(2,weight=1)
listbox_frame.grid_columnconfigure(3,weight=1)
listbox_frame.grid_columnconfigure(4,weight=0)


scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical")
scrollbar.grid(row=0, column=1, sticky="ns")

scrollbar2=ttk.Scrollbar(listbox_frame, orient="vertical")
scrollbar2.grid(row=0, column=4, sticky="ns")


ref_listbox = tk.Listbox(listbox_frame, exportselection=False, yscrollcommand=scrollbar.set)
ref_listbox.grid(row=0, column=0, sticky="nsew")
scrollbar.config(command=ref_listbox.yview)

selected_listbox = tk.Listbox(listbox_frame, exportselection=False,yscrollcommand=scrollbar2.set)
selected_listbox.grid(row=0, column=3, sticky="nsew")
scrollbar2.config(command=selected_listbox.yview)

#Buttons to move items between listboxes
btn_frame = ttk.Frame(listbox_frame,style='Custom.TFrame')
btn_frame.grid(row=0, column=2, sticky="nsew",padx=(9,9))

# Configurar las filas del frame de botones para que se expandan igualmente
btn_frame.grid_rowconfigure(0, weight=1)  # Fila por encima de los botones
btn_frame.grid_rowconfigure(2, weight=1)  # Fila por encima de los botones
btn_frame.grid_rowconfigure(4, weight=1)  # Fila por encima de los botones
btn_frame.grid_rowconfigure(1, weight=1)  # Puedes ajustar este peso si necesitas más control sobre la posición de los botones
btn_frame.grid_rowconfigure(3, weight=1)  # Fila entre los botones (si deseas espacio entre ellos)
btn_frame.grid_rowconfigure(5, weight=1)  # Fila por debajo de los botones
btn_frame.grid_columnconfigure(0,weight=1)

move_to_selected_button = ttk.Button(btn_frame, text=" → ", 
                                     command=move_to_selected, width=2,
                                     style="Custom.TButton")
move_to_selected_button.grid(row=2,column=0,sticky='nsew')

move_to_references_button = ttk.Button(btn_frame, text=" ← ",
                                       command=move_to_references, width=2,
                                       style="Custom.TButton")

move_to_references_button.grid(row=4,column=0,sticky='nsew')

###############################################
#RADIO BUTTONS FOR OFFER AND OPERATIVE EXPENSES
###############################################


# Radio button options (independent groups)
radio_values = {
    "Tipo": tk.StringVar(value="Público"),
    "Requerimiento": tk.StringVar(value="Normal"),
    "Canal": tk.StringVar(value="Institucional")
}


# Creating the radio buttons for each option
options_frame = ttk.Frame(right_frame,style='Custom.TFrame')
options_frame.grid(row=3, column=0, sticky="ew")
options_frame.grid_columnconfigure(0,weight=1)
options_frame.grid_columnconfigure(1,weight=1)
options_frame.grid_columnconfigure(2,weight=1)
options_frame.grid_columnconfigure(3,weight=1)

for i, (label, var) in enumerate(radio_values.items()):
    ttk.Label(options_frame, text=label,style="Large.TLabel").grid(row=i, column=0, sticky="w")
    options_frame.grid_rowconfigure(i, weight=1)

    if label == "Tipo":
        choices = ["Público", "Privado", "Mixto"]
    elif label == "Requerimiento":
        choices = ["Urgente", "Normal"]
    else: # Canal
        choices = ["Institucional", "Proyectos", "Presidencia"]

    # Creating the radio buttons
    for j, choice in enumerate(choices):
        radio_btn = ttk.Radiobutton(options_frame, text=choice, 
                                    variable=var, value=choice,style='Custom.TRadiobutton')
        radio_btn.grid(row=i, column=j+1, sticky="w", padx=5)



###################
#GASTOS OPERATIVOS
###################

def on_switch():
    # Esta función se llama cada vez que el estado del switch cambia.
    # Puedes añadir aquí la lógica que necesites ejecutar cuando el switch cambia.
    if switch_var.get():
        for widget in widgets_to_control:
            widget.configure(state='normal')
    else:
        for widget in widgets_to_control:
            widget.delete(0,'end')
            widget.configure(state='disabled')

switch_var = tk.BooleanVar()


right_right_frame=ttk.Frame(root,style='Custom.TFrame')
right_right_frame.grid(row=0,column=2,sticky="nsew", padx=10, pady=10)
right_right_frame.grid_columnconfigure(0,weight=1)
right_right_frame.grid_rowconfigure(0,weight=1)
right_right_frame.grid_rowconfigure(1,weight=0)
right_right_frame.grid_rowconfigure(2,weight=1)
right_right_frame.grid_rowconfigure(3,weight=1)

firstframe=ttk.Frame(right_right_frame,style='Custom.TFrame')
firstframe.grid(row=1,column=0,sticky='ns',pady=(10,10))
secondframe=ttk.Frame(right_right_frame,style='Custom.TFrame')
secondframe.grid(row=2,column=0,sticky='ns')
thirdframe=ttk.Frame(right_right_frame,style='Custom.TFrame')
thirdframe.grid(row=3,column=0,sticky='nsew')

thirdframe.grid_columnconfigure(0,weight=1)
thirdframe.grid_rowconfigure(0,weight=1)

dobutton=ttk.Button(thirdframe, text="Crear SP",command=browse_file,style="Custom.TButton")
dobutton.grid(row=0, column=0, sticky='ew',pady=(0, 10))


gastosope=ttk.Label(firstframe, text="Gastos Operativos",style="Bold.TLabel")
gastosope.grid(row=0, column=0,sticky='ew')

switch_button=ttk.Checkbutton(firstframe,style="Switch.TCheckbutton", text="", 
                              variable=switch_var, 
                              onvalue=True, offvalue=False, command=on_switch)
switch_button.grid(row=0,column=1,padx=10)

num_pro=ttk.Label(secondframe,text='Número de profesionales: ',style="Large.TLabel")
num_pro.grid(row=0,column=0,sticky='ew',pady=(0,10))

num_dias=ttk.Label(secondframe,text='Días: ',style="Large.TLabel")
num_dias.grid(row=1,column=0,sticky='ew',pady=(0,10))

interm=ttk.Label(secondframe,text='Transporte intermunicipal: ',style="Large.TLabel")
interm.grid(row=2,column=0,sticky='ew',pady=(0,10))

gastos=ttk.Label(secondframe,text='Otros gastos',style="Large.TLabel")
gastos.grid(row=3,column=0,sticky='ew',pady=(0,10))


profesionales=ttk.Entry(secondframe,validate='key',validatecommand=vcmd)
profesionales.grid(row=0,column=1,sticky='ew',pady=(0,10))

dias=ttk.Entry(secondframe,validate='key',validatecommand=vcmd)
dias.grid(row=1,column=1,sticky='ew',pady=(0,10))

tinter=ttk.Entry(secondframe)
tinter.grid(row=2,column=1,sticky='ew',pady=(0,10))

gastoss=ttk.Entry(secondframe)
gastoss.grid(row=3,column=1,sticky='ew',pady=(0,10))


widgets_to_control=[profesionales,dias,tinter,gastoss]
on_switch()

# Start the application
root.mainloop()