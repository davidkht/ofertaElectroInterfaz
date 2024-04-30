import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import sp
import os
import sys
import pandas as pd

carpetas={
    'PHY':'COTIZACIONES/PHYWE',
    'ELECTRO':'COTIZACIONES/ELECTRO',
    '3B':'COTIZACIONES/3B',
    'LN':'COTIZACIONES/LUCAS NULLE',
    'TER':'COTIZACIONES/TERCEROS',
    'EU':'COTIZACIONES/EUROMEX',
    'PT': 'COTIZACIONES/PT'
}

def get_resource_path():
    """ Retorna la ruta absoluta al recurso, para uso en desarrollo o en el ejecutable empaquetado. """
    if getattr(sys, 'frozen', False):
        # Si el programa ha sido empaquetado, el directorio base es el que PyInstaller proporciona
        base_path = sys._MEIPASS
    else:
        # Si estamos en desarrollo, utiliza la ubicación del script
        base_path = os.path.dirname(os.path.realpath(__file__))

    return base_path

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
    for i in selected[::-1]:  # Revertir para manejar múltiples selecciones correctamente
        item = ref_listbox.get(i)
        selected_listbox.insert(tk.END, item)
        # No eliminar el ítem de ref_listbox para cumplir con el reque

def move_to_references():
    selected = selected_listbox.curselection()
    for i in selected[::-1]:  # Revertir para manejar múltiples selecciones correctamente
        selected_listbox.delete(i)

def on_combobox_change(event,combobox_var,values):
    # Obtiene el texto actual del combobox
    current_text = combobox_var.get()
    
    # Encuentra la coincidencia más cercana de la lista de valores
    closest_match = find_closest_match(current_text, values)
    
    # Si hay una coincidencia cercana, actualiza el texto del combobox con ese valor
    if closest_match:
        combobox_var.set(closest_match)
    else:
        # Si no hay ninguna coincidencia, limpia el combobox
        combobox_var.set('')

def find_closest_match(text, values_list):
    # Encuentra el valor más cercano que comience con el texto ingresado
    for value in values_list:
        if value.lower().startswith(text.lower()):
            return value
    return None

def actualizar_referencias_por_seleccion(event):
    seleccion = marca.get()  # Obtiene el valor actual seleccionado en la Combobox
    global lista_completa_referencias  # Declara que se modificará la variable global
    lista_completa_referencias = list(sp.nombres_de_basedeDatos(seleccion))
    actualizar_ref_listbox()  # Actualiza la listbox con las referencias correspondientes

def extraer_informacion():
    datos = {
        "Comercial": controlLabel.get(),
        "Imprevistos": improvistosVariable.get(),
        "Estampillas": estampillasVariable.get(),
        "Institucion": institucionVariable.get(),
        "Trimestre": combovar.get(),
        "Ciudad": comboovar.get(),
        "Carpeta": nombreCarpetaFinalVariable.get(),
        "Tipo": radio_values["Tipo"].get(),
        "Requerimiento": radio_values["Requerimiento"].get(),
        "Canal": radio_values["Canal"].get(),
        "Presupuesto": presupuestoVar.get(),
        "Consecutivo": consecutivo,
        "Profesionales": num_pro_var.get(),
        "Dias": num_dias_var.get(),
        "Moneda":monedacomboVar.get()
    }
    return datos

def preparar_valor(valor):
    """
    Convierte NaN a cadena vacía y mantiene el resto de los valores.
    """
    if pd.isna(valor):
        return ""
    else:
        return valor
    
def ajustar_altura_treeview(treeview, min_height=15, max_height=30):
    """Ajusta la altura del TreeView basado en el número de ítems, con un mínimo y un máximo."""
    num_items = len(treeview.get_children())
    new_height = min(max(num_items, min_height), max_height)
    treeview.config(height=new_height)

def manejar_advertencias():
    if nombreCarpetaFinalVariable.get() == '':
        messagebox.showerror("Error","La carpeta debe tener un nombre no-vacio.")
    elif selected_listbox.size()==0:
        respuesta=messagebox.askyesno("Advertencia","No hay referencias seleccionadas en la lista. \n¿Continuar?")
        if respuesta:
            respuestass=messagebox.askokcancel("Creación de Solicitud",f"""
                                        Se creara una solicitud con el nombre:\n
                                        {nombreCarpetaFinalVariable.get()}\n
                                        Presione 'Ok' para continuar, o 'Cancelar'\n
                                        para corregir alguna información""")
            if respuestass:
                crear_SP()
    else:
        respuestass=messagebox.askokcancel("Creación de Solicitud",f"""
                                        Se creara una solicitud con el nombre:\n
                                        {nombreCarpetaFinalVariable.get()}\n
                                        Presione 'Aceptar' para continuar, o 'Cancelar' para corregir alguna información""")
        if respuestass:
            crear_SP()

def crear_SP():
    datos=extraer_informacion()
 
    nombre_carpeta=datos['Carpeta']
    carpeta_mitad=carpetas[carpetaVariable.get()]
    ventana_tabla = tk.Toplevel()
    ventana_tabla.title(nombre_carpeta)
    ventana_tabla.iconbitmap(os.path.join(script_directory,"imagen.ico"))
    ventana_tabla.configure(background=colordefondo)
    # ventana_tabla.geometry("400x250")
    frameIzquierdo=ttk.Frame(ventana_tabla,style='Custom.TFrame')
    frameIzquierdo.grid(row=0,column=0,padx=10,pady=10,sticky='nsew')
    frameDerecho=ttk.Frame(ventana_tabla,style='Custom.TFrame')
    frameDerecho.grid(row=0,column=1,padx=(10,20))
 

    referencias=sp.extraer_referencias_de_base_de_datos(referencias_seleccionadas())
    pdfTrue=sp.crear_carpeta_y_archivos(nombre_carpeta,variableControl.get(),carpeta_mitad)

    if pdfTrue:
        label = ttk.Label(frameDerecho, text="Carpeta creada exitósamente",style="Bold.TLabel")
        label.grid(row=0, column=0,pady=20)
    else:
        label = ttk.Label(frameDerecho, text="Carpeta creada sin FSC\nni información de comercial",style="Bold.TLabel")
        label.grid(row=0, column=0,pady=20)

    labelInfo=ttk.Label(frameDerecho, text="Porfavor confirme cantidades y guardelas.",style="Large.TLabel")
    labelInfo.grid(row=1, column=0)
    labelInfo2=ttk.Label(frameDerecho, text="Finalice con el botón 'Electro'",style="Large.TLabel")
    labelInfo2.grid(row=2, column=0,pady=(0,30))


    tree=ttk.Treeview(frameIzquierdo)
    tree.grid(row=0,column=0,sticky='nsew')

    for i in tree.get_children():
        tree.delete(i)
    

    columnas_a_mostrar=['DESCRIPCION','CANTIDAD','MONEDA','PRECIO']
    columnas_mostrar_treeview = ['REFERENCIA']+columnas_a_mostrar
    # Configurar las columnas en el Treeview
    tree['columns'] = columnas_mostrar_treeview

    # Ocultar la columna de árbol (tree) para no tener una columna vacía al inicio
    tree['show'] = 'headings'  # Esto hace que solo se muestren las columnas definidas, sin la columna de árbol
    
    # Configurar las columnas en el Treeview
    for columna in columnas_mostrar_treeview:
        tree.heading(columna, text=columna)
        tree.column(columna, anchor=tk.CENTER)

    # Insertar los datos del DataFrame en el Treeview, incluido el índice
    for indice, fila in referencias.iterrows():
        valores = [indice] + [preparar_valor(fila[col]) for col in columnas_a_mostrar]
        tree.insert("", tk.END, values=valores)

    # Configurar las cabeceras y el ancho de las columnas
    tree.column('REFERENCIA', width=80)
    tree.column('DESCRIPCION', width=500)
    tree.column('CANTIDAD', width=75)
    tree.column('MONEDA',  width=60)
    tree.column('PRECIO',  width=80)

    def on_double_click(event):
        """Manejador para el evento de doble clic en una celda de 'CANTIDADES'."""
        item = tree.selection()[0]  # Obtener el ítem seleccionado
        column = tree.identify_column(event.x)  # Identificar la columna clickeada

        # Si se clickea la columna de 'CANTIDADES', permitir editar
        if tree.heading(column)['text'] == 'CANTIDAD':
            entry_popup(item, column)
    def entry_popup(item, column):
        """Crea un Entry para editar el valor de la celda."""
        # Crear y posicionar el Entry widget
        x, y, width, height = tree.bbox(item, column)
        entry = tk.Entry(tree, width=width,validate='key',validatecommand=vcmd)
        entry.place(x=x, y=y, width=width, height=height)
        
        # Función para reemplazar el valor de la celda al presionar Enter
        def save_edit(event):
            tree.set(item, column=tree.heading(column)['text'], value=entry.get())
            entry.destroy()  # Eliminar el Entry después de guardar el valor
        
        entry.bind("<Return>", save_edit)
        entry.focus()
    def guardar_cantidades():
        cantidades = []
        for item in tree.get_children():
            # Asumiendo que 'CANTIDAD' es la tercera columna, puedes ajustar el índice [2] según sea necesario
            cantidad = tree.item(item, 'values')[2] 
            cantidades.append(cantidad)
        
        return cantidades
    def click_cantidades():
        global cantidades 
        try:
            if selected_listbox.size()==0:
                cantidades=True
                messagebox.showinfo("Información","No hay elementos. Presione el botón 'ELECTRO'",parent=ventana_tabla)
            else:
                cantidades=guardar_cantidades()
                
                messagebox.showinfo("Información","Cantidades guardadas",parent=ventana_tabla)
        except Exception as e:
            messagebox.showerror("Error","ERROR",parent=ventana_tabla)
    
    def click_final():    
        try:
            if cantidades and all(cantidad.strip() for cantidad in cantidades):
                
                try:
                    sp.manejar_SP(datos,referencias,cantidades,carpeta_mitad)
                    sp.crear_csv_cot(os.path.join(script_directory,carpeta_mitad,nombre_carpeta))
                    messagebox.showinfo("Éxito","Solicitud creada exitósamente\nPresione Aceptar para salir.",parent=ventana_tabla)
                    ventana_tabla.destroy()
                except Exception as e:
                    messagebox.showerror("Error",str(e),parent=ventana_tabla)
            else:
                messagebox.showwarning("Advertencia","No se olvide de GUARDAR las cantidades!",parent=ventana_tabla)
        except NameError:
            messagebox.showwarning("Advertencia","No se olvide de guardar las cantidades!",parent=ventana_tabla)
        except TypeError:
            messagebox.showwarning("Advertencia","La solicitud se guardará sin ítems",parent=ventana_tabla)
            try:
                sp.manejar_SP(datos,referencias,cantidades,carpeta_mitad)
                sp.crear_csv_cot(os.path.join(script_directory,carpeta_mitad,nombre_carpeta))
                messagebox.showinfo("Éxito","Solicitud creada exitósamente\nPresione Aceptar para salir.",parent=ventana_tabla)
                ventana_tabla.destroy()
            except Exception as e:
                messagebox.showerror("Error",str(Exception),parent=ventana_tabla)


    tree.bind("<Double-1>", on_double_click)
    ajustar_altura_treeview(tree)
    boton_guardar=ttk.Button(frameDerecho,text='Guardar Cantidades',command=click_cantidades,style='Custom.TButton')
    boton_guardar.grid(row=3,column=0,sticky='ew',padx=20)

    botonFinal=ttk.Button(frameDerecho,image=mi_imagen,command=click_final,style='Custom.TButton')
    botonFinal.grid(row=5,column=0, sticky='s',pady=(50,15))

def referencias_seleccionadas():
    # Obteniendo el número total de elementos en el listbox
    total_elementos = selected_listbox.size()    
    # Extrayendo todos los elementos desde el primero (0) hasta el último
    elementos = selected_listbox.get(0, total_elementos)
    referencias= [elemento.split(" - ")[0] for elemento in elementos]
    return referencias

script_directory =get_resource_path()  # Obtiene el directorio donde se encuentra el script

root = tk.Tk()
root.title("Crear Oferta")
root.geometry("1360x400")
root.resizable(False,False)
root.iconbitmap(os.path.join(script_directory,"imagen.ico"))
imagen_ico = Image.open(os.path.join(script_directory,"imagen.ico"))
mi_imagen=imagen_ico.resize((48,48))
mi_imagen = ImageTk.PhotoImage(mi_imagen)

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

style.configure("Bold.TLabel", font=("Arial", 17,'bold'), foreground=foregroundvariable,
                background=colordefondo)

style.configure("dis.TLabel", font=("Arial", 18), foreground='grey50',
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
fsc.grid(row=1, column=0, sticky="ew",pady=(0, 10))


fsc_entry = ttk.Entry(left_frame,textvariable=variableControl , state='readonly',style='Custom.TEntry')
fsc_entry.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 10))

controlLabel=tk.StringVar()
com_entry = ttk.Entry(left_frame,textvariable=controlLabel , state='readonly',style='Custom.TEntry')
com_entry.grid(row=3, column=1, sticky="ew", pady=(0, 10))

examine_button = ttk.Button(left_frame, text="Examinar",command=browse_file,style="Custom.TButton")
examine_button.grid(row=1, column=1, sticky='ew',pady=(0, 10))

#########################################################
#SECCION ENCABEZADO
#########################################################


valores_para_listas=[['Q2-2024','Q3-2024','Q4-2024','Q1-2025','Q2-2025','Q3-2025','Q4-2025'],
                     sp.gastos_de_viaje()]
vcmd = (root.register(on_validate), '%P')
label = ["Improvistos:", "Estampillas:","Institución", "Trimestre Esperado:", 
          "Ciudad:","Presupuesto: ","Moneda Requerida:"]

improvistosVariable=tk.StringVar()
improvistos=ttk.Label(left_frame, text=label[0],style="Large.TLabel")
improvistos.grid(row=4, column=0, sticky="w",pady=(0, 10))

estampillasVariable=tk.StringVar()
estampillas=ttk.Label(left_frame, text=label[1],style="Large.TLabel")
estampillas.grid(row=5, column=0, sticky="w",pady=(0, 10))

institucionVariable=tk.StringVar()
institucion=ttk.Label(left_frame, text=label[2],style="Large.TLabel")
institucion.grid(row=6, column=0, sticky="w",pady=(0, 10))


trimistre=ttk.Label(left_frame, text=label[3],style="Large.TLabel")
trimistre.grid(row=8, column=0, sticky="w",pady=(0, 10))

ciudad=ttk.Label(left_frame, text=label[4],style="Large.TLabel")
ciudad.grid(row=9, column=0, sticky="w",pady=(0, 10))

presupuestoVar=tk.StringVar()
presupuestoL=ttk.Label(left_frame, text=label[5],style="Large.TLabel")
presupuestoL.grid(row=7, column=0, sticky="w",pady=(0, 10))
presupuestoEntry=ttk.Entry(left_frame,validate='key',validatecommand=vcmd,
                           style='Custom.TEntry',textvariable=presupuestoVar)
presupuestoEntry.grid(row=7, column=1, sticky="ew", pady=(0, 10))

improvistosEntry=ttk.Entry(left_frame,validate='key',validatecommand=vcmd,
                           style='Custom.TEntry',textvariable=improvistosVariable)
improvistosEntry.grid(row=4, column=1, sticky="ew", pady=(0, 10))

estampillasEntry=ttk.Entry(left_frame,validate='key',validatecommand=vcmd,
                           style='Custom.TEntry',textvariable=estampillasVariable)
estampillasEntry.grid(row=5, column=1, sticky="ew", pady=(0, 10))

institucionEntry=ttk.Entry(left_frame,style='Custom.TEntry',textvariable=institucionVariable)
institucionEntry.grid(row=6, column=1, sticky="ew", pady=(0, 10))

combovar=tk.StringVar()
comboovar=tk.StringVar()

combobox = ttk.Combobox(left_frame,values=valores_para_listas[0],textvariable=combovar)
combobox.grid(row=8, column=1, sticky="ew", pady=(0, 10))
comboobox = ttk.Combobox(left_frame,values=valores_para_listas[1],textvariable=comboovar)
comboobox.grid(row=9, column=1, sticky="ew", pady=(0, 10))

combobox.bind('<FocusOut>', 
              lambda event, a=combovar,b=valores_para_listas[0]:on_combobox_change(event,a,b))
combobox.bind('<Return>', 
              lambda event, a=combovar,b=valores_para_listas[0]:on_combobox_change(event,a,b))
comboobox.bind('<FocusOut>', 
              lambda event, a=comboovar,b=valores_para_listas[1]:on_combobox_change(event,a,b))
comboobox.bind('<Return>', 
              lambda event, a=comboovar,b=valores_para_listas[1]:on_combobox_change(event,a,b))

monedaLabel=ttk.Label(left_frame, text=label[6],style="Large.TLabel")
monedaLabel.grid(row=10, column=0, sticky="w",pady=(0, 10))
monedacomboVar=tk.StringVar()
valores_moneda=['COP','USD','EUR']
monedacombo=ttk.Combobox(left_frame,values=valores_moneda,textvariable=monedacomboVar)
monedacombo.grid(row=10, column=1, sticky="ew", pady=(0, 10))

monedacombo.bind('<FocusOut>', 
              lambda event, a=monedacomboVar,b=valores_moneda:on_combobox_change(event,a,b))
monedacombo.bind('<Return>', 
              lambda event, a=monedacomboVar,b=valores_moneda:on_combobox_change(event,a,b))

#########################################################
#SECCION REFERENCIAS Y MARCA
#########################################################

right_frame = ttk.Frame(root,style='Custom.TFrame')
right_frame.grid(row=0, column=1, padx=0, pady=10)
right_frame.grid_rowconfigure(2, weight=1)
right_frame.grid_rowconfigure(1, weight=1)
right_frame.grid_rowconfigure(0, weight=1)
right_frame.grid_rowconfigure(3, weight=1)
right_frame.grid_columnconfigure(0, weight=1)
right_frame.grid_columnconfigure(1, weight=1)

top_frame= ttk.Frame(right_frame,style='Custom.TFrame')
top_frame.grid(row=0,column=0,sticky='ew')
top_frame.grid_columnconfigure(0, weight=1)
top_frame.grid_columnconfigure(1, weight=1)
top_frame.grid_rowconfigure(1, weight=1)
top_frame.grid_rowconfigure(0, weight=1)

carpetasPosibles=['PHY','TER','3B','ELECTRO','LN','EU','PT']
carpetaVariable=tk.StringVar()
nombreCarpeta=ttk.Label(top_frame,text="Carpeta",style="Bold.TLabel")
nombreCarpeta.grid(row=0, column=2,sticky='w',pady=(0,10))
carpeta=ttk.Combobox(top_frame,style='Custom.TCombobox',values=carpetasPosibles,
                   textvariable=carpetaVariable)
carpeta.grid(row=0,column=3,padx=(30,0),pady=(0,10),sticky='w')
carpeta.set(carpetasPosibles[3])
carpeta.bind('<FocusOut>', 
              lambda event, a=carpetaVariable,b=carpetasPosibles:on_combobox_change(event,a,b))
carpeta.bind('<Return>', 
              lambda event, a=carpetaVariable,b=carpetasPosibles:on_combobox_change(event,a,b))

marcalabel=ttk.Label(top_frame, text="Marca",style="Bold.TLabel")
marcalabel.grid(row=0, column=0,sticky='ns',pady=(0,10))
reflabel=ttk.Label(top_frame, text="Referencias",style="Bold.TLabel")
reflabel.grid(row=1, column=0,sticky='ns',pady=(0,10))

marcaslista=['PHYWE','EUROMEX']
marcavariable=tk.StringVar()
marca=ttk.Combobox(top_frame,style='Custom.TCombobox',values=marcaslista,
                   textvariable=marcavariable)
marca.grid(row=0,column=1,padx=(30,0),pady=(0,10),sticky='w')

marca.bind('<FocusOut>', 
              lambda event, a=marcavariable,b=marcaslista:on_combobox_change(event,a,b))
marca.bind('<Return>', 
              lambda event, a=marcavariable,b=marcaslista:on_combobox_change(event,a,b))
marca.bind('<<ComboboxSelected>>', actualizar_referencias_por_seleccion)

searchVar=tk.StringVar()
search_entry = ttk.Entry(top_frame,style='Custom.TEntry',textvariable=searchVar)
search_entry.grid(row=1, column=1, columnspan=3, padx=(30,0), pady=(0,10),sticky='ew')
lista_completa_referencias = list(sp.nombres_de_basedeDatos('PHYWE'))
##########################
# Listboxes with scrollbar
##########################
listbox_frame = ttk.Frame(right_frame,style='Custom.TFrame')
listbox_frame.grid(row=2, column=0,  sticky="nsew", pady=(10, 10))

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


ref_listbox = tk.Listbox(listbox_frame, exportselection=False, 
                         yscrollcommand=scrollbar.set,width=50)
ref_listbox.grid(row=0, column=0, sticky="w")
scrollbar.config(command=ref_listbox.yview)

selected_listbox = tk.Listbox(listbox_frame, exportselection=False,
                              yscrollcommand=scrollbar2.set,width=50)
selected_listbox.grid(row=0, column=3, sticky="e")
scrollbar2.config(command=selected_listbox.yview)

#Buttons to move items between listboxes
btn_frame = ttk.Frame(listbox_frame,style='Custom.TFrame')
btn_frame.grid(row=0, column=2, sticky="nsew",padx=(5,5))

# Configurar las filas del frame de botones para que se expandan igualmente
btn_frame.grid_rowconfigure(0, weight=1)  # Fila por encima de los botones
btn_frame.grid_rowconfigure(2, weight=1)  
btn_frame.grid_rowconfigure(4, weight=1)  
btn_frame.grid_rowconfigure(1, weight=1)  # Puedes ajustar este peso si necesitas más control sobre la posición de los botones
btn_frame.grid_rowconfigure(3, weight=1)  # Fila entre los botones (si deseas espacio entre ellos)
btn_frame.grid_rowconfigure(5, weight=1)  # Fila por debajo de los botones
btn_frame.grid_columnconfigure(0,weight=1)

move_to_selected_button = ttk.Button(btn_frame, text=" → ", 
                                     command=move_to_selected, width=5,
                                     style="Custom.TButton")
move_to_selected_button.grid(row=2,column=0,sticky='ew')

move_to_references_button = ttk.Button(btn_frame, text=" X ",
                                       command=move_to_references, width=5,
                                       style="Custom.TButton")

move_to_references_button.grid(row=4,column=0,sticky='ew')

def actualizar_ref_listbox(search_text=''):
    ref_listbox.delete(0, tk.END)  # Limpia la listbox antes de actualizarla
    for indice, nombre in lista_completa_referencias:
        if search_text.lower() in str(nombre).lower() or search_text.lower() in str(indice).lower():
            ref_listbox.insert(tk.END, f"{indice} - {nombre}")

def on_search_entry_change(*args):
    search_text = searchVar.get()
    actualizar_ref_listbox(search_text)

actualizar_ref_listbox()

searchVar.trace_add("write", on_search_entry_change)
#########################
#RADIO BUTTONS FOR OFFER 
#########################


# Radio button options (independent groups)
radio_values = {
    "Tipo": tk.StringVar(value="Público"),
    "Requerimiento": tk.StringVar(value="Normal"),
    "Canal": tk.StringVar(value="Institucional")
}

# Creating the radio buttons for each option
options_frame = ttk.Frame(right_frame,style='Custom.TFrame')
options_frame.grid(row=3, column=0)
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
right_right_frame.grid(row=0,column=2,sticky="nsew", pady=10)
right_right_frame.grid_columnconfigure(0,weight=1)
right_right_frame.grid_rowconfigure(0,weight=1)
right_right_frame.grid_rowconfigure(1,weight=0)
right_right_frame.grid_rowconfigure(2,weight=1)
right_right_frame.grid_rowconfigure(3,weight=1)

firstframe=ttk.Frame(right_right_frame,style='Custom.TFrame')
firstframe.grid(row=1,column=0,sticky='ns',pady=(10,10),padx=10)
secondframe=ttk.Frame(right_right_frame,style='Custom.TFrame')
secondframe.grid(row=2,column=0,sticky='ns',pady=(10,10),padx=10)
thirdframe=ttk.Frame(right_right_frame,style='Custom.TFrame')
thirdframe.grid(row=3,column=0,sticky='nsew',pady=(10,10),padx=10)

thirdframe.grid_columnconfigure(0,weight=1)
thirdframe.grid_rowconfigure(0,weight=1)

nombreFinal=ttk.Label(thirdframe, text="Nombre final de carpeta",style="Bold.TLabel")
nombreFinal.grid(row=0, column=0,sticky='ns',pady=(0, 0))

nombreCarpetaFinalVariable=tk.StringVar()

nombreCarpetaFinal=ttk.Entry(thirdframe,textvariable=nombreCarpetaFinalVariable)
nombreCarpetaFinal.grid(row=1,column=0,sticky='ew',pady=(0, 20))

dobutton=ttk.Button(thirdframe, text="Crear SP",command=manejar_advertencias,style="Custom.TButton")
dobutton.grid(row=2, column=0, sticky='ew',pady=(0, 10))

numero_consecutivo=tk.StringVar()
def actualizar_entry1(*args):
    # Concatenar los valores de Entry2, Entry3, Combobox1 y variable_uno
    global consecutivo
    prefijo = carpetaVariable.get()
    nombredelainstitucion=institucionVariable.get()
    comercial=variableControl.get().split('/')[-1][:-4]
    numeroCons=str(sp.obtener_nuevo_consecutivo(prefijo,carpetas[prefijo]))
    numero_consecutivo.set(numeroCons)
    consecutivo=prefijo+" "+numero_consecutivo.get()+"-24"
    if nombredelainstitucion== '':
        if comercial == '':
            valor_actualizado=consecutivo
        else:
            valor_actualizado=consecutivo+' '+comercial
    elif comercial== '':
        valor_actualizado=consecutivo+' '+nombredelainstitucion
    else:
        valor_actualizado = consecutivo+' '+comercial+' '+nombredelainstitucion
    # Actualizar el valor de Entry1
    nombreCarpetaFinalVariable.set(valor_actualizado)

carpetaVariable.trace_add('write', actualizar_entry1)
institucionVariable.trace_add('write', actualizar_entry1)
variableControl.trace_add('write', actualizar_entry1)
carpeta.bind('<<ComboboxSelected>>', actualizar_entry1)


gastosope=ttk.Label(firstframe, text="Gastos Operativos",style="Bold.TLabel")
gastosope.grid(row=0, column=0,sticky='ew',pady=(0, 10))

switch_button=ttk.Checkbutton(firstframe,style="Switch.TCheckbutton", text="", 
                              variable=switch_var, 
                              onvalue=True, offvalue=False, command=on_switch)
switch_button.grid(row=0,column=1,padx=10,pady=(0, 10))

num_pro_var=tk.StringVar()
num_pro=ttk.Label(secondframe,text='Número de profesionales: ',style="Large.TLabel")
num_pro.grid(row=0,column=0,sticky='ew',pady=(0,10))

num_dias_var=tk.StringVar()
num_dias=ttk.Label(secondframe,text='Días: ',style="Large.TLabel")
num_dias.grid(row=1,column=0,sticky='ew',pady=(0,10))

profesionales=ttk.Entry(secondframe,validate='key',validatecommand=vcmd,textvariable=num_pro_var)
profesionales.grid(row=0,column=1,sticky='ew',pady=(0,10))

dias=ttk.Entry(secondframe,validate='key',validatecommand=vcmd,textvariable=num_dias_var)
dias.grid(row=1,column=1,sticky='ew',pady=(0,10))


widgets_to_control=[profesionales,dias]
on_switch()

# Start the application
root.mainloop()