import os  # Importa el módulo os para interactuar con el sistema operativo
import pandas as pd  # Importa pandas para la manipulación de datos
import openpyxl  # Importa openpyxl para trabajar con archivos Excel
from openpyxl.utils.dataframe import dataframe_to_rows  # Función para convertir un DataFrame de pandas en filas para Excel
from openpyxl.styles import Font  # Importa Font para estilizar las celdas de Excel
from openpyxl.drawing.image import Image  # Importa Image para añadir imágenes a los archivos Excel

ARCHIVO_ESPECIFICACIONES_EXCEL = 'Especificaciones_SPPHYWE2024.xlsx'  # Define el nombre del archivo de especificaciones
# Bloque de código para definir rutas de archivos y directorios, y ejecutar las funciones definidas anteriormente
script_actual = os.path.realpath(__file__)  # Obtiene la ruta absoluta del script en ejecución
script_directory = os.path.dirname(script_actual)  # Obtiene el directorio donde se encuentra el script

# Función para solicitar al usuario que ingrese un número dentro de un conjunto de opciones válidas
def solicitar_entrada_numerica(mensaje, opciones_validas):
    """
    Solicita al usuario una entrada numérica válida y repite hasta que se obtenga una respuesta adecuada.
    
    :param mensaje: El mensaje a mostrar al usuario.
    :param opciones_validas: Una lista de enteros que son las opciones válidas.
    :return: Un entero que es la entrada válida del usuario.
    """
    while True:
        try:
            entrada = int(input(mensaje))
            if entrada in opciones_validas:
                return entrada
            else:
                print(f"Por favor, ingrese un número válido: {', '.join(map(str, opciones_validas))}.")
        except ValueError:
            print("Eso no parece ser un número válido. Por favor, intente de nuevo.")

# Función para extraer datos del usuario mediante entradas por teclado
def extraer_datos_Usuario():
    """
    Extrae información del encabezado SP a partir de entradas del usuario.
    """
    imprevistos=input("Ingrese los siguientes datos:\nImprevistos(%): ")
    estampillas=input("Estampillas(%): ")
    presupuesto=input("Presupuesto (si no aplica presione Enter): ")
    trimestre=input("Trimestre Esperado Oportunidad: ")
    ciudad=input("Ciudad: ")
    print("\n")
    return imprevistos,estampillas,presupuesto,trimestre,ciudad

# Función para encontrar un archivo PDF que comience con 'FSC' y extraer un nombre comercial basado en un código presente en el nombre del archivo
def encontrar_pdf_y_extraer_nombre(archivo):

    nombres_Comercial = {
        'CG': 'CAROLINA GAITAN',
        'ER': 'ESTEBAN RAMIREZ',
        'JO': 'JIMMY ORTIZ',
        'NF': 'NELIS FABREGAS',
        'JC': 'JEIMY CADENA',
        'CR': 'CHRISTIAN ROMERO',
        'RB': 'ROCÍO BARÓN',
        'DC': 'DANIELA CRISTANCHO',
        'AC': 'ANDRES CUESTAS'
    }
    
    archivo=archivo.split('/')[-1]
    
    if archivo.startswith('FSC'):
        return nombres_Comercial[archivo.split('-')[1]]  # Extracts the code from the filename and returns the corresponding commercial name.
    return None

# Función para buscar en un DataFrame de pandas las referencias proporcionadas y notificar cuáles se encontraron y cuáles no
def extraer_referencias_de_base_de_datos(df, referencias):
    """
    Busca en un DataFrame de pandas las referencias proporcionadas. 
    Devuelve las referencias encontradas y notifica de las no encontradas.
    """
    referencias_existentes = []
    referencias_no_encontradas = []

    for ref in referencias:
        if ref in df.index:
            referencias_existentes.append(ref)  # Adds the reference to the list of existing ones if found in the DataFrame's index.
        else:
            referencias_no_encontradas.append(ref)  # Adds the reference to the list of not found in the opposite case.

    if referencias_no_encontradas:
        print("References not found: " + ", ".join(referencias_no_encontradas)+'\n')  # Prints the references not found.
    if not referencias_existentes:
        print("No references found")
    return df.loc[referencias_existentes]  # Returns the rows of the DataFrame corresponding to the existing references.

# Función para manejar el llenado de un archivo SP con información específica
def manejar_SP(rutaSP, df, header, referencias):
    """
    Llena el encabezado del SP. Extrae del nombre del archivo el nombre de universidad y consecutivo,
    los cuales retorna para posterior uso.
    Extrae referencias de la base de datos y la llena en la tabla del SP.
    La única columna que queda por llenar es CANTIDADES, las cuales las pide al Usuario.
    Por último, llena la segunda hoja del excel SP con datos del usuario también
    """
    wb_sp = openpyxl.load_workbook(rutaSP)
    hoja_SP = wb_sp.worksheets[0]

    hoja_SP['E2'] = header[1]
    hoja_SP['E3'] = header[0]
    hoja_SP['E14'] = header[4]
    hoja_SP['E15'] = header[3]
    hoja_SP['E16'] = header[2]

    # Updates cell E6 with the university name.
    nombre_archivo = rutaSP.split("/")[-1].split(" ")

    nombre_universidad=nombre_archivo[3:]
    nombre_universidad=" ".join(nombre_universidad)[:-5]

    hoja_SP['E6'] = nombre_universidad

    consecutivo=nombre_archivo[1:3]
    consecutivo= " ".join(consecutivo)


    if header[5] in ['JIMMY ORTIZ', 'JEIMY CADENA']:
        hoja_SP['E8'] = header[5]  # Updates cell E8 with the commercial name if it's Ortiz or Cadena.
    else:
        hoja_SP['E9'] = header[5]  # Updates cell E9 with the commercial name for other cases.

    df_SP = extraer_referencias_de_base_de_datos(df, referencias)  # Retrieves the references from the database.

    # Iterates through the rows of the DataFrame and inserts them into the Excel sheet.
    for r_idx, row in enumerate(dataframe_to_rows(df_SP, index=True, header=False), 19):
        if r_idx == 19:
            continue  # Skips the first row (DataFrame indices).
        for c_idx, value in enumerate(row, 1):
            hoja_SP.cell(row=r_idx, column=c_idx, value=value)  # Inserts each value into the corresponding cell.


    df_show = df_SP[['DESCRIPCION','PROVEEDOR','PRECIO']]

    print("\nPor favor escriba las cantidades de los productos escogidos.\n")
    print("-----------------------------------------------------------------------------------")
    cantidades=[]
    for i in range(len(df_show)):
        fila=df_show.iloc[i,:]
        print("\n")
        print(fila)
        cantidad=int(input("CANTIDAD DEL PRODUCTO: "))
        cantidades.append(cantidad)
        print("\n-----------------------------------------------------------------------------------")
        

    for j, valor in enumerate(cantidades, 20):
        hoja_SP.cell(row=j, column=9, value=valor)
    
    #Ahora llena la segunda hoja del excel
    hoja_SP_gastos=wb_sp.worksheets[1]

    respuestaValida=False
    print("\nVamos a estimar los gastos operativos de capacitación...\n")
    capa=solicitar_entrada_numerica("Hay capacitación presencial fuera de Bogotá?: (1:Si, 0:No)", [0,1])

    if capa == 0:
        print("No hay gastos operativos\n")
    else:       
        while not respuestaValida:
            dias=input("\n Número de días de capacitación: ")
            profesionales=input("\n Número de profesionales: ")
            intermunicipal=input("\n Transporte intermunicipal? (50kCOP c/u) (Presiona Enter si no aplica): ")
            trans_personal=1
            vuelos=1
            taxis=4
            hotel=1
            alimentacion=1
            gastos=input("\n Gastos adicionales/Otros?: (30kCOP c/u): ")

            try:
                dias=int(dias)
                profesionales=int(profesionales)
                hoja_SP_gastos["D6"]= dias
                hoja_SP_gastos["D7"]= profesionales
                if intermunicipal:
                    hoja_SP_gastos["D11"]= int(intermunicipal)
                else:
                    hoja_SP_gastos["D11"]= 0
                hoja_SP_gastos["D12"]= trans_personal
                hoja_SP_gastos["D13"]= vuelos
                hoja_SP_gastos["D14"]= taxis/profesionales
                hoja_SP_gastos["D15"]= hotel*(dias-1)*profesionales
                hoja_SP_gastos["D16"]= alimentacion*dias
                hoja_SP_gastos["D17"]= int(gastos)
                respuestaValida=True
            except Exception as e:
                print("\nAlguno de los datos es erróneo (No es un número). Intente nuevamente")

    wb_sp.save(rutaSP)  # Saves the changes made in the Excel file.

    return nombre_universidad,consecutivo

# Función para llenar el encabezado de un archivo de oferta con datos específicos
def llenar_encabezado_oferta(rutaof,datos):
    """
    Escribe el encabezado en el archivo de oferta a partir de datos
    rutaof: ruta del archivo de oferta
    datos: tupla de datos
    """
    wb_OF = openpyxl.load_workbook(rutaof)  # Loads the Excel workbook.
    hoja_destino= wb_OF.worksheets[0]

    #Llena y formatea el encabezado
    celda_cliente=hoja_destino['B17:D17']
    celda_cliente[0][0].value= f"NOMBRE DE CLIENTE: {datos[1]}"

    celda_consecutivo=hoja_destino['E17:F17']
    celda_consecutivo[0][0].value= f"OFERTA N°: {datos[0]}"
    
    celda_ciudad=hoja_destino['G17:H17']
    celda_ciudad[0][0].value= f"CIUDAD: {datos[2]}"
    
    celda_comercial=hoja_destino['B18:D18']
    celda_comercial[0][0].value= f"COMERCIAL: {datos[3]}"

    celda_estampillas=hoja_destino['K17:L17']
    celda_estampillas[0][0].value= f"% ESTAMPILLAS: {datos[4]} %"

    celda_imprevistos=hoja_destino['K18:L18']
    celda_imprevistos[0][0].value= f"% IMPREVISTOS: {datos[5]} %"


    # Aplicar formato (negrita y Arial Narrow) a las celdas
    for celda in ['B17', 'G17', 'B18', 'K17', 'K18', 'E17']:
        hoja_destino[celda].font = Font(bold=True, name='Arial Narrow')


    # Preguntas adicionales
    tipo_requerimiento = solicitar_entrada_numerica("¿Qué tipo de requerimiento es? (Ingrese el número correspondiente: 1. Normal, 2. Urgente): ", [1, 2])
    tipo_cliente = solicitar_entrada_numerica("¿Qué tipo de cliente es? (Ingrese el número correspondiente: 1. Privado, 2. Público, 3. Mixto): ", [1, 2, 3])
    tipo_proceso = solicitar_entrada_numerica("¿Qué tipo de proceso es? (Ingrese el número correspondiente: 1. Institucional, 2. Con proyectos, 3. Presidencia): ", [1, 2, 3])

    # Mapear las respuestas a las etiquetas correspondientes
    etiquetas_requerimiento = {1: "Normal", 2: "Urgente"}
    etiquetas_cliente = {1: "Privado", 2: "Público", 3: "Mixto"}
    etiquetas_proceso = {1: "Institucional", 2: "Con proyectos", 3: "Presidencia"}

    # Colocar las respuestas en las celdas correspondientes
    hoja_destino['F18'] = etiquetas_requerimiento[tipo_requerimiento]
    hoja_destino['H18'] = etiquetas_cliente[tipo_cliente]
    hoja_destino['J18'] = etiquetas_proceso[tipo_proceso]


    img = Image(os.path.join(script_directory, 'second.png'))
    hoja_destino.add_image(img, 'B1')
    wb_OF.save(rutaof)

# Función para crear un archivo CSV de cotización a partir de un archivo SP
def crear_csv_cot(ruta_del_archivo):
    """
    Crea el csv de cotización de PHYWE a partir del SP. 
    Se utiliza Pandas para extraer del SP y escribir en el csv
    """
    df = pd.read_excel(ruta_del_archivo, skiprows=18, sheet_name='SOLICITUD')
    df_soloPhywe = df[(df['PROVEEDOR'] == 'PHYWE')]
    nuevoDF = pd.DataFrame({
        'Ref': df_soloPhywe['REFERENCIA'],
        'Qty': df_soloPhywe['CANTIDAD']
    }).replace(r'\s+', '', regex=True)

    output_file = os.path.join(script_directory, 'PHYWEQUOTE.csv')
    nuevoDF.to_csv(output_file, sep=';', index=False)

def gastos_de_viaje():
    ruta_gastos= os.path.join(script_directory, 'SP.xlsx')
    data=pd.read_excel(ruta_gastos,index_col=0,sheet_name='TARIFAS')
    return data.index.to_list()

def baseDeDatos_dataFrame():
    ruta_BasedeDatos = os.path.join(script_directory, ARCHIVO_ESPECIFICACIONES_EXCEL)
    df = pd.read_excel(ruta_BasedeDatos, index_col=0)
    df = df.drop(columns=['FILTRADO'])
    return df  
def nombres_de_basedeDatos():
    df=baseDeDatos_dataFrame()
    indices=df.index.tolist()
    nombres=df.loc[:,'DESCRIPCION']
    return nombres

import re
def obtener_nuevo_consecutivo(prefijo):
    """
    Dado un prefijo, esta función busca en el directorio actual por carpetas
    que comiencen con ese prefijo, extrae el número consecutivo, y devuelve
    el último consecutivo encontrado más uno.
    """
    consecutivo_maximo = 0
    pattern = re.compile(rf"^{prefijo}\s+(\d+)-")

    for carpeta in os.listdir(script_directory):
        full_path = os.path.join(script_directory, carpeta)
        if os.path.isdir(full_path):
            match = pattern.match(carpeta)
            if match:
                consecutivo_actual = int(match.group(1))
                consecutivo_maximo = max(consecutivo_maximo, consecutivo_actual)    
    return consecutivo_maximo + 1

def main():

    archivos = os.listdir(script_directory)  # Lista los archivos en el directorio del script

    # Encuentra el archivo que comienza con 'OFERTA' y construye la ruta completa al archivo encontrado
    archivo_of = next((archivo for archivo in archivos if archivo.startswith('OFERTA')), None)
    ruta_of = os.path.join(script_directory, archivo_of)

    # Encuentra el archivo que comienza con 'SP' y construye la ruta completa al archivo encontrado
    archivo_SP = next((archivo for archivo in archivos if archivo.startswith('SP')), None)
    ruta_SP = os.path.join(script_directory, archivo_SP)

    # Extrae datos manuales del usuario y encuentra el nombre comercial a partir de un archivo PDF
    imprevistos,estampillas,presupuesto,trimestre,ciudad=extraer_datos_Usuario()
    nombre_encontrado = encontrar_pdf_y_extraer_nombre(archivos)

    encabezado=(imprevistos,estampillas,presupuesto,trimestre,ciudad, nombre_encontrado)

    df=baseDeDatos_dataFrame()
    refs = input("Inserte la lista de referencias a buscar (separadas por espacio):\n").split(" ")

    # Llama a las funciones definidas para manejar el archivo SP y llenar el encabezado de la oferta, y para crear el CSV de cotización
    universidad,consecutivo=manejar_SP(ruta_SP,df,encabezado,refs)
    data=(consecutivo,universidad,ciudad,nombre_encontrado,estampillas,imprevistos)
    llenar_encabezado_oferta(ruta_of,data)
    crear_csv_cot(ruta_SP)
                   
if __name__ == '__main__':  
    main()              
                   
