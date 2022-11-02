from distutils.command.config import config
from hashlib import new
from tkinter import *
from tkinter import ttk
from turtle import heading, left, right, st, width
import pyodbc
import articulo


root = Tk()
root.geometry('1430x700')
root.resizable(0,0)
#root.config(bg="")
root.title('Sox-Control de Stock')


#Conexion a la base de datos. 
def connectMe():
    server = 'localhost'
    bd = 'SOX_PIGUE_SA'
    user = 'sa'
    password = '#SQLserver2022'

    try:
        connection = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server}; SERVER='+server+'; DATABASE='+bd+';UID='+user+'; pwd='+password+';TrustServerCertificate=yes;')
        print('conexion exitosa')
        return connection

    except Exception as ex:
        print(ex)

#Ejecuta la query. 
def mainQuery():
    for i in tree.get_children():
        tree.delete(i)
        print(i)
    conexion = connectMe()
    cur = conexion.cursor()
    
    cur.execute(" SELECT DESCRIPCION, VISTA.COD_ARTICU, CONVERT(INT,STOCKEXPEDICION), CONVERT(INT,STOCKRESERVADO), CONVERT(INT, (MIN(STOCKLINEA) / MAX(NECESITALINEA))) AS MAX_BOLSAS_POSIBLES_LINEA, "+
                " ORDEN.fecha_prog, orden.cant "+
                " FROM VW_STOCKCOMPLETOARTICULOS2 VISTA "+
                " LEFT JOIN VW_ORDENFABRICACIONFUTURASOX2 ORDEN ON VISTA.COD_ARTICU = ORDEN.COD_ARTICU "+
                " GROUP BY DESCRIPCION, VISTA.COD_ARTICU, STOCKEXPEDICION, STOCKRESERVADO, ORDEN.fecha_prog, orden.cant ")
    articulos = cur.fetchall()
    
    i=0
    for articulo in articulos:
        tree.insert("", i, text='', values=(articulo[0], articulo[1],articulo[2], articulo[3], articulo[4],articulo[5], articulo[6]))
        i = i + 1
    #print(articulos)
        
    conexion.close()
    return articulos

#Se ejecuta cada vez que se ingresa una letra por telclado.
#Recorre todo el arbol buscando las coincidencias en la variable 'descripcion'
# y los posiciona al principio del arbol ademas de destacar toda la fila con otro color. 
def filter (*args):
    items = tree.get_children()
    selections = []
    search = entry_var.get()
    #print("search: ", search)
    for item in items:
        #print("tree.item(item)", tree.item(item)['values'][0])
        if search.upper() in tree.item(item)['values'][0]:
            #print("Entro al if")
            #print("search: ", search)
            search_var = tree.item(item)['values']
            #print("search var: ", search_var)
            tree.delete(item)
            aux = tree.insert("", 0, values=search_var)
            selections.append(aux)
    tree.selection_set(selections)
    #print("SELEC: ",selections)

#Vacia el entry para una futura busqueda. Crea una nueva ventana. Deshanilita la ventana principal.
#Obtiene el codigo de articulo('S') que selecciono el usuario.
#Busca la informacion de los 'L' y los 'T' del articulo 'S'.
#Crea un nuevo Treeview e inserta la nueva informacion. 
def moreInformation(event):
    print("funciona")
    
    newWindow = Toplevel(root)
    newWindow.title('New')
    newWindow.geometry('1300x600')    
    newWindow.grab_set()
    item = tree.focus()
    print('lo que selecciono: ', tree.item(item)['values'][1])
    entry.delete(0, END)
    selectionsaux = []
    tree.selection_set(selectionsaux)
    #Creo el arbol donde se mostrara la informacion.
    columns = ['Descripcion', 'Codigo articulo','Talle', 'Familia', 'Pedidos', 'Cantidad pedidos',
            'Expedicion','Deposito facturacion' ,'Bolsas en linea', 'Bolsas en tejeduria', 'Medida']

    tree2 = ttk.Treeview(newWindow)
    tree2["columns"] = columns
    for i in columns:
        tree2.column(i)
        tree2.heading(i, text=i.capitalize())
    tree2["show"] = "headings"
    tree2.pack()

    
def query():
    mainQuery()
    
#-----------------------------------------------------------------------------------------------------------------------------
#Frame para el filtro
frame1 = Frame(root, height=200)
frame1.pack(fill="x")
frame1.config(borderwidth=10,highlightbackground="black", highlightthickness=1)
#Label, entry y button para frame1
label = Label(frame1, text="Ingresar codigo")
label.pack(side= LEFT, anchor= W, pady=10, padx=10)

entry_var = StringVar()
entry = Entry(frame1, textvariable=entry_var)
entry_var.trace("w", filter)
entry.pack(side=LEFT, anchor=W, pady=10, padx=10)

button = Button(frame1, text="Mas informacion", bg="yellow")
button.pack(side=RIGHT, anchor=E, pady=10, padx=10)

#Creo el arbol donde se mostrara la informacion.
columns = ['Descripcion', 'Codigo articulo','Stock expedicion', 'Stock reservado', 
            'Maximas bolsas posibles en linea','Fecha programada' ,'Cantidad']

tree = ttk.Treeview(root)
tree["columns"] = columns
for i in columns:
    tree.column(i)
    tree.heading(i, text=i.capitalize())
tree["show"] = "headings"
tree.pack()
tree.place(x=50, y=100,width=1300, height=550)
tree.column('Descripcion', width=310)
tree.column('Codigo articulo', width=150)
tree.column('Stock expedicion', width=100, anchor=CENTER)
tree.column('Stock reservado', width=100, anchor=CENTER)
tree.column('Maximas bolsas posibles en linea', width=160, anchor=CENTER)
tree.column('Cantidad', width=100, anchor=CENTER)
tree.bind('<Double-1>', moreInformation)

#Creo los scrollbars para el arbol en root. 
scrollbarx = ttk.Scrollbar(root, orient=HORIZONTAL)
scrollbarx.configure(command=tree.xview)
tree.configure(xscrollcommand=scrollbarx.set)
scrollbarx.pack(side=BOTTOM, fill="x")

scrollbary = ttk.Scrollbar(root, orient=VERTICAL)
scrollbary.configure(command=tree.yview)
tree.configure(yscrollcommand=scrollbary.set)
scrollbary.pack(side= RIGHT, fill=Y, ipady=40)


query()


root.mainloop()

