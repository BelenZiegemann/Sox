
from distutils.command.config import config
from hashlib import new
from operator import truediv
from time import process_time_ns
from tkinter import *
from tkinter import ttk
from traceback import print_tb
from turtle import heading, left, right, st, width
import pyodbc
import articulo as art


root = Tk()
root.geometry('1430x700')
root.resizable(0,0)
#root.config(bg="")
root.title('Sox-Control de Stock')

#Columnas para la tabla correspondiente a la ventana princiapl.
columns = ['Descripcion', 'Codigo articulo','Stock expedicion', 'Stock reservado', 
            'Maximas bolsas posibles en linea','Fecha programada' ,'Cantidad']
#Columnas para la tabla correspondiente a la segunda ventana (o ventana que brinda mas informacion).
columns2 = ['Insumo en Linea', 'Descripcion de insumo','Necesita linea', 'Stock en linea', 'Insumo tejeduria', 
            'Descripcion insumo tejeduria', 'Necesita tejeduria']

listArticulos = []

#---------------------------------------------------------------------------------------------------------------------------------
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

#Crea la ventana principal en forma de arbol. Muestra informacion correspondiente a columns.
def mainQuery():
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
    conexion.close()
    return articulos

#Realiza la consulta a la base de datos. Por cada fila que retorna la consulta: si no existe el S lo crea. Si existe,
#Consulta si existe su hijo L. Si existe L, solo crea los T. Si no existe, Crea L y T. 
#Cada articulo S tiene una lista de hijos correspondientes a los articulos L y una lista de nietos correspondientes a los articulos T.
#listArticulos es una lista que mantiene todos los objetos correspondientes a los articulos S. 
def auxQuery():
    conexion = connectMe()
    cur = conexion.cursor()
    cur.execute(" SELECT * FROM VW_STOCKCOMPLETOARTICULOS2 ")
    items = cur.fetchall()
    conexion.close()

    for item in items:
        auxS = item[0]
        auxL = item[4]
        #print('Item: ', item[1],item[5],item[9])
        existS = next((e for e in listArticulos if e.cod_articulo==auxS), NONE)
        #print("resp: ", resp)
        if existS is NONE:
            #print("Significa que el s NO existe. Creo el S: ", item[1], item[0])
            artL = art.ArticuloL(item[4], item[5], item[7])
            #print("Creo el L: ", item[4])
            artT = art.ArticuloT(item[8], item[9], item[11])
            #print("Creo el T: ", item[8])
            artS = art.ArticuloS(item[0],item[1],item[2],item[3],item[6],item[10],artL,artT)
            listArticulos.append(artS)
        else:
            #print('El S existe y es: ', existS.cod_articulo)
            existL = existeL(existS.hijos, auxL)
            if existL is NONE:
                #print('El L NO existe. Lo creo: ', item[5])
                artL = art.ArticuloL(item[4], item[5], item[7])
                existS.agregarHijo(artL)
            #print('Creo el T: ', item[9])
            artT = art.ArticuloT(item[8], item[9], item[11])
            existS.agregarNieto(artT)
            print('Los hijos de S son: ', existS.hijos)
            print('Los nietos de S son: ', existS.nietos)
    print(len(listArticulos))

#Busca en la lista de hijos de un dado articulo S.
#Si hijo L existe, retorna TRUE. Caso contrario, retorna FALSE. 
def existeL(hijos, aux):
    for i in hijos:
        if i.cod_articulo==aux:
            print('Existe L: ', i)
            return i
            break
    return NONE
   
#Se ejecuta cada vez que se ingresa una letra por telclado.
#Recorre todo el arbol de articulos buscando las coincidencias en la variable 'descripcion'
# y los posiciona al principio del arbol, ademas de destacar toda la fila con otro color. 
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
    newWindow.title('Informacion detallada-Sox')
    newWindow.geometry('1400x300')    
    newWindow.grab_set()
    item = tree.focus()
    print('lo que selecciono: ', tree.item(item)['values'][1])
    entry.delete(0, END)
    selectionsaux = []
    tree.selection_set(selectionsaux)
    #Creo el arbol donde se mostrara la informacion.
    tree2 = ttk.Treeview(newWindow)
    tree2["columns"] = columns2
    for i in columns2:
        tree2.column(i)
        tree2.heading(i, text=i.capitalize())
    tree2["show"] = "headings"
    tree2.pack()
    articuloS = buscarSelect(tree.item(item)['values'][1])
    print(articuloS.cod_articulo)
    print(articuloS.stockReservado)
    for j in articuloS.hijos:
        print("hijo insumo: ", j.cod_articulo)
        print("hijo descrp: ", j.descripcion)
        print("necesita linea: ", articuloS.necesitaLinea)
        print("stock linea: ", j.stockLinea)
    for h in articuloS.nietos:
        print("nieto insumo: ", h.cod_articulo)
        print("nieto descrp: ", h.descripcion)
        print("necesita tejeduria: ", articuloS.necesitaTejeduria)
        print("stock tejeduria: ", h.stockTejeduria)
    i=0
    for l in articuloS.nietos:
        tree2.insert("", i, text='' ,values=('-', '-', '-', '-', l.cod_articulo, l.descripcion, articuloS.necesitaTejeduria, l.stockTejeduria))
        i = i + 1

        



#Busca el articulo S seleccionado en la lista de articulos. 
def buscarSelect(select):
    for i in listArticulos:
        if i.cod_articulo == select:
            return i
            break

#-----------------------------------------------------------------------------------------------------------------------------   
def query():
    mainQuery()
    auxQuery()
    
#-----------------------------------------------------------------------------------------------------------------------------
#Widgets para la ventana principal. 
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

