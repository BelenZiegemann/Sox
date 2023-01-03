from tkinter import *
from tkinter import ttk
import pyodbc
import articulo as art

DESCRIPCION = 0
SALDO = 1
VENTAS_TRIM = 2
VENTAS_ANUAL = 3
PEND_PED = 4
EXPEDICION = 5
RESERVADO = 6
MAX_LINEA = 7
MAX_TEJEDURIA = 8
FECHA_PROGRAMADA = 9
CANT_PROG = 10
CODIGO_ARTICULO = 11

INSUMO_LINEA = 0
DESCRIP_INSUMO = 1
NECESITA_LINEA = 2
STOCK_LINEA = 3
INSUMO_TEJEDURIA = 4
DESCRIP_INSUMO_TEJ = 5
NECESITA_TEJEDURIA = 6
STOCK_TEJEDURIA = 7

ANCHO = 1350
ALTO = 600


root = Tk()
x = int((root.winfo_screenwidth()/2)-(ANCHO/2))
y = int((root.winfo_screenheight()/2)-(ALTO/2))
root.geometry("{}x{}+{}+{}".format(ANCHO, ALTO, x, y))
root.resizable(FALSE, FALSE)
root.title('Sox-Control de Stock')

# Columnas para la tabla correspondiente a la ventana princiapl.
columns = ['Descripcion', 'Saldo', 'Ventas trim', 'Ventas año', 'Pend ped', 'Expedicion', 'Reservado',
           'Max linea', 'Max tejeduria', 'Fecha programada', 'Cant prog', 'Codigo articulo']
# Columnas para la tabla correspondiente a la segunda ventana (o ventana que brinda mas informacion).
columns2 = ['Insumo Linea', 'Descripcion de insumo', 'Necesita linea', 'Stock linea', 'Insumo tejeduria',
            'Descripcion insumo tejeduria', 'Necesita tejeduria', 'Stock tejeduria']

listArticulos = []
listArticulosAux = []

tree = ttk.Treeview(root)
style = ttk.Style()
style.configure("Treeview.Heading", font=('Calibri', 10, 'bold'))
tree.tag_configure('uno', foreground='black', background='white')
tree.tag_configure('dos', foreground='black', background='#F0EDEC')

# ---------------------------------------------------------------------------------------------------------------------------------
# Conexion a la base de datos.


def connectMe():
    server = 'localhost'
    bd = 'SOX_PIGUE_SA'
    user = 'sa'
    password = '#SQLserver2022'
    try:
        connection = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server}; SERVER='+server+'; DATABASE='+bd+';UID=' +
                                    user+'; pwd='+password+';TrustServerCertificate=yes;')
        return connection

    except Exception as ex:
        print(ex)


# Realiza la consulta a la base de datos. Por cada fila que retorna la consulta: si no existe el S lo crea. Si existe,
# Consulta si existe su hijo L. Si existe L, solo crea los T. Si no existe, Crea L y T.
# Cada articulo S tiene una lista de hijos correspondientes a los articulos L y una lista de nietos correspondientes a los articulos T.
# listArticulos es una lista que mantiene todos los objetos correspondientes a los articulos S.
def mainQuery():
    conexion = connectMe()
    cur = conexion.cursor()
    cur.execute(" SELECT * FROM VW_STOCKCOMPLETOARTICULOS ")
    items = cur.fetchall()
    conexion.close()
    for item in items:
        # Consulta si el articuloS ya fue creado.
        existS = next((e for e in listArticulos if e.cod_articulo == item[0]), NONE)
        if existS is NONE:
            artT = art.ArticuloT(item[8], item[9], item[11])
            artL = art.ArticuloL(item[4], item[5], item[7], item[10], artT)
            artS = art.ArticuloS(item[0], item[1], item[2], item[3], item[6], artL, artT, item[12], item[13], item[14],
                                 item[15], item[16], item[17], item[18], item[19], item[20], item[21])
            listArticulos.append(artS)
        else:
            # Consulta si el articuloL ya fue creado.
            existL = next((e for e in existS.hijos if e.cod_articulo == item[4]), NONE)
            if existL is NONE:
                artT = art.ArticuloT(item[8], item[9], item[11])
                artL = art.ArticuloL(item[4], item[5], item[7], item[10], artT)
                existS.agregarHijo(artL)
            else:
                artT = art.ArticuloT(item[8], item[9], item[11])
                existS.agregarNieto(artT)
                existL.agregarHijo(artT)

# Crea la ventana principal en forma de arbol. Muestra informacion correspondiente a columns.
# El contador i genera el color intercalado de las filas.


def insertTree(list):
    i = 0
    for articulo in list:
        if i % 2 == 0:
            tree.insert("", i, text='', values=(articulo.descripcion, articulo.saldo, articulo.vendidoTrimestral,
                                                articulo.vendidoAnual, articulo.pedido, articulo.stockExpedicion,
                                                articulo.stockReservado, articulo.max_bolsasL,
                                                articulo.max_bolsasT, articulo.fecha, articulo.cant,
                                                articulo.cod_articulo,), tags='uno')
        else:
            tree.insert("", i, text='', values=(articulo.descripcion, articulo.saldo, articulo.vendidoTrimestral,
                                                articulo.vendidoAnual, articulo.pedido, articulo.stockExpedicion,
                                                articulo.stockReservado, articulo.max_bolsasL,
                                                articulo.max_bolsasT, articulo.fecha, articulo.cant,
                                                articulo.cod_articulo,), tags='dos')
        i = i + 1


# Se ejecuta cada vez que se ingresa una letra por telclado.
# Si el usuario no ingresa nada, se mantiene el arbol.
# Si no, almacena en una lista auxiliar las coincidencias y luego actualiza el arbol.
def filter(*args):
    search = entry_var.get()
    if search == ' ':
        listArticulosAux = listArticulos
    else:
        listArticulosAux = []
        for item in listArticulos:
            if search.upper() in item.getDescripcion():
                listArticulosAux.append(item)
    update(listArticulosAux)

# Elimina todo el arbol y muestra solo aquellos objetos que coinciden segun la busqueda del usuario.


def update(list):
    items = tree.get_children()
    for item in items:
        tree.delete(item)
    insertTree(list)


# Vacia el entry para una futura busqueda. Crea una nueva ventana. Deshanilita la ventana principal.
# Obtiene el codigo de articulo('S') que selecciono el usuario.
# Busca la informacion de los 'L' y los 'T' del articulo 'S'.
# Crea un nuevo Treeview e inserta la nueva informacion.


def moreInformation(event):
    newWindow = Toplevel(root)
    newWindow.title('Sox-Informacion detallada')
    newWindow.geometry("{}x{}+{}+{}".format(ANCHO, 300, x, y))  
    newWindow.grab_set()
    item = tree.focus()
    seleccionado = tree.item(item)['values'][CODIGO_ARTICULO]
    tree2 = ttk.Treeview(newWindow)
    tree2.bind('<Button-1>', handle_click)
    tree2["columns"] = columns2
    for i in columns2:
        tree2.column(i)
        tree2.heading(i, text=i.capitalize())
    tree2["show"] = "headings"
    tree2.pack()
    tree2.place(x=30, y=20, width=1300, height=700)
    scrollbarx = ttk.Scrollbar(newWindow, orient=HORIZONTAL)
    scrollbarx.configure(command=tree2.xview)
    tree2.configure(xscrollcommand=scrollbarx.set)
    scrollbarx.pack(side=BOTTOM, fill="x")
    tree2.column(DESCRIP_INSUMO, width=250)
    tree2.column(NECESITA_LINEA, width=100, anchor=CENTER)
    tree2.column(STOCK_LINEA, width=90, anchor=CENTER)
    tree2.column(DESCRIP_INSUMO_TEJ, width=250)
    tree2.column(NECESITA_TEJEDURIA, width=110, anchor=CENTER)
    tree2.column(STOCK_TEJEDURIA, width=90, anchor=CENTER)
    # Recupero el objeto S para poder consultar dos atributos.
    articuloS = next((e for e in listArticulos if e.cod_articulo == seleccionado), NONE)
    articuloL = buscarSelect(seleccionado)
    i = 0
    for l in articuloL:
        for t in l.hijos:
            tree2.insert("", i, text='', values=(l.cod_articulo, l.descripcion, articuloS.necesitaL, l.stockExpedicion,
                                                 t.cod_articulo, t.descripcion, l.necesitaT, t.stockExpedicion))
            i = i + 1
    
# Busca el articulo S seleccionado en la lista de articulos.
# Retorna la lista de hijos (articulosL) correspondietes al articuloS.


def buscarSelect(select):
    for i in listArticulos:
        if i.cod_articulo == select:
            return i.hijos

# Evita que el usuario pueda modificar el ancho de las columnas.


def handle_click(event):
    if tree.identify_region(event.x, event.y) == "separator":
        return "break"

# Configuracion del arbol de la ventana principal.
# Se ajusta el ancho de las columnas. 


def createTree():
    tree["columns"] = columns
    for i in columns:
        tree.column(i)
        tree.heading(i, text=i.capitalize())
    tree["show"] = "headings"
    tree.pack()
    tree.place(x=40, y=100, width=1250, height=470)
    tree.column(DESCRIPCION, minwidth=300, width=300)
    tree.column(SALDO, width=100, anchor=CENTER)
    tree.column(VENTAS_TRIM, width=100, anchor=CENTER)
    tree.column(VENTAS_ANUAL, width=100, anchor=CENTER)
    tree.column(PEND_PED, width=110, anchor=CENTER)
    tree.column(EXPEDICION, width=100, anchor=CENTER)
    tree.column(RESERVADO, width=100, anchor=CENTER)
    tree.column(MAX_LINEA, width=110, anchor=CENTER)
    tree.column(MAX_TEJEDURIA, width=110, anchor=CENTER)
    tree.column(FECHA_PROGRAMADA, width=160, anchor=CENTER)
    tree.column(CANT_PROG, width=100, anchor=CENTER)
    tree.column(CODIGO_ARTICULO, minwidth=130, width=130)
    tree.bind('<Double-1>', moreInformation)
    tree.bind('<Button-1>', handle_click)
# -----------------------------------------------------------------------------------------------------------------------------


def query():
    createTree()
    mainQuery()
    insertTree(listArticulos)
    #root.after(30000, query)
     
# -----------------------------------------------------------------------------------------------------------------------------
# Widgets para la ventana principal.


frame1 = Frame(root, height=200)
frame1.pack(fill="x")
frame1.config(borderwidth=10, highlightbackground="black", highlightthickness=1)
# Label, entry y button para frame1
label = Label(frame1, text="Ingresar codigo")
label.pack(side=LEFT, anchor=W, pady=10, padx=10)

entry_var = StringVar()
entry = Entry(frame1, textvariable=entry_var)
entry_var.trace("w", filter)
entry.pack(side=LEFT, anchor=W, pady=10, padx=10)

# Creo los scrollbars para el arbol en root.
scrollbarx = ttk.Scrollbar(root, orient=HORIZONTAL)
scrollbarx.configure(command=tree.xview)
tree.configure(xscrollcommand=scrollbarx.set)
scrollbarx.pack(side=BOTTOM, fill="x")

scrollbary = ttk.Scrollbar(root, orient=VERTICAL)
scrollbary.configure(command=tree.yview)
tree.configure(yscrollcommand=scrollbary.set)
scrollbary.pack(side=RIGHT, fill=Y, ipady=40)


query()

# Cierra la ventana en 10 segundos. 
# root.after(10000, root.destroy)

root.mainloop()
