from tkinter import *
from tkinter import ttk
import pyodbc
import articulo as art


root = Tk()
root.geometry('1430x700')
root.resizable(0,0)
root.title('Sox-Control de Stock')

#Columnas para la tabla correspondiente a la ventana princiapl.
columns = ['Descripcion', 'Codigo articulo','Saldo','Stock expedicion', 'Stock reservado', 
            'Maximas bolsas posibles','Fecha programada' ,'Cantidad', 'Vendido', 'Pendiente pedido']
#Columnas para la tabla correspondiente a la segunda ventana (o ventana que brinda mas informacion).
columns2 = ['Insumo en Linea', 'Descripcion de insumo','Necesita linea', 'Stock en linea', 'Insumo tejeduria', 
            'Descripcion insumo tejeduria', 'Necesita tejeduria', 'Stock tejeduria']

listArticulos = []

tree = ttk.Treeview(root)
tree.tag_configure('uno', foreground='black', background='white')
#tree.tag_configure('dos', foreground='black', background='#E7E3E1')
tree.tag_configure('dos', foreground='black', background='#F0EDEC')

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


#Realiza la consulta a la base de datos. Por cada fila que retorna la consulta: si no existe el S lo crea. Si existe,
#Consulta si existe su hijo L. Si existe L, solo crea los T. Si no existe, Crea L y T. 
#Cada articulo S tiene una lista de hijos correspondientes a los articulos L y una lista de nietos correspondientes a los articulos T.
#listArticulos es una lista que mantiene todos los objetos correspondientes a los articulos S. 
def mainQuery():
    conexion = connectMe()
    cur = conexion.cursor()
    cur.execute(" SELECT * FROM VW_STOCKCOMPLETOARTICULOS ")
    items = cur.fetchall()
    conexion.close()
    for item in items:
        #Consulta si el articuloS ya fue creado. 
        existS = next((e for e in listArticulos if e.cod_articulo==item[0]), NONE)
        if existS is NONE:
            artT = art.ArticuloT(item[8], item[9], item[11])
            artL = art.ArticuloL(item[4], item[5], item[7], item[10],artT)
            artS = art.ArticuloS(item[0],item[1],item[2],item[3],item[6],artL,artT,item[12],item[13],item[14],item[15],item[16],item[17],item[18],item[19])
            listArticulos.append(artS)
        else:
            #Consulta si el articuloL ya fue creado. 
            existL = next((e for e in existS.hijos if e.cod_articulo==item[4]), NONE)
            if existL is NONE:
                artT = art.ArticuloT(item[8], item[9], item[11])
                artL = art.ArticuloL(item[4], item[5], item[7], item[10], artT)
                existS.agregarHijo(artL)
            else:
                artT = art.ArticuloT(item[8], item[9], item[11])
                existS.agregarNieto(artT)
                existL.agregarHijo(artT)
    print(len(listArticulos))

#Crea la ventana principal en forma de arbol. Muestra informacion correspondiente a columns.
def auxQuery():
    i=0
    for articulo in listArticulos:
        if(i%2==0):
            tree.insert("", i, text='', values=(articulo.descripcion, articulo.cod_articulo, articulo.saldo, articulo.stock, articulo.stockReservado, 
                                            articulo.max_bolsas, articulo.fecha, articulo.cant,articulo.vendido, articulo.pedido),tags='uno')
        else:
            tree.insert("", i, text='', values=(articulo.descripcion, articulo.cod_articulo, articulo.saldo, articulo.stock, articulo.stockReservado, 
                                            articulo.max_bolsas, articulo.fecha, articulo.cant,articulo.vendido, articulo.pedido),tags='dos')
        i = i + 1

   
#Se ejecuta cada vez que se ingresa una letra por telclado.
#Recorre todo el arbol de articulos buscando las coincidencias en la variable 'descripcion'
# y los posiciona al principio del arbol, ademas de destacar toda la fila con otro color. 
def filter (*args):
    items = tree.get_children()
    selections = []
    search = entry_var.get()
    for item in items:
        if search.upper() in tree.item(item)['values'][0]:
            search_var = tree.item(item)['values']
            tree.delete(item)
            aux = tree.insert("", 0, values=search_var)
            selections.append(aux)
    tree.selection_set(selections)

#Vacia el entry para una futura busqueda. Crea una nueva ventana. Deshanilita la ventana principal.
#Obtiene el codigo de articulo('S') que selecciono el usuario.
#Busca la informacion de los 'L' y los 'T' del articulo 'S'.
#Crea un nuevo Treeview e inserta la nueva informacion. 
def moreInformation(event):
    print("funciona")
    newWindow = Toplevel(root)
    newWindow.title('Sox-Informacion detallada')
    newWindow.geometry('1400x300')    
    newWindow.grab_set()
    item = tree.focus()
    seleccionado = tree.item(item)['values'][1]
    entry.delete(0, END)
    selectionsaux = []
    tree.selection_set(selectionsaux)
    tree2 = ttk.Treeview(newWindow)
    tree2["columns"] = columns2
    for i in columns2:
        tree2.column(i)
        tree2.heading(i, text=i.capitalize())
    tree2["show"] = "headings"
    tree2.pack()
    scrollbarx = ttk.Scrollbar(newWindow, orient=HORIZONTAL)
    scrollbarx.configure(command=tree2.xview)
    tree2.configure(xscrollcommand=scrollbarx.set)
    scrollbarx.pack(side=BOTTOM, fill="x")
    tree2.column('Descripcion de insumo',width=290)
    tree2.column('Descripcion insumo tejeduria',width=290)
    tree2.column('Necesita linea', width=100, anchor=CENTER)
    tree2.column('Stock en linea', width=100, anchor=CENTER)
    tree2.column('Necesita tejeduria', width=100, anchor=CENTER)
    tree2.column('Stock tejeduria', width=100, anchor=CENTER)
    #Recupero el objeto S para poder consultar dos atributos. 
    articuloS = next((e for e in listArticulos if e.cod_articulo==seleccionado), NONE)
    print("El s: ", articuloS.cod_articulo)
    articuloL = buscarSelect(seleccionado)
    print("devuelta: ", articuloL)
    i = 0
    for l in articuloL:
        print("hijo insumo: ", l.cod_articulo)
        print("hijo descrp: ", l.descripcion)
        print("hijos: ", l.hijos)
        for t in l.hijos:
            print("T: ", t.cod_articulo)
            tree2.insert("", i, text='', values=(l.cod_articulo, l.descripcion, articuloS.necesita, l.stock, t.cod_articulo, t.descripcion, l.necesita, t.stock))
            i = i + 1
    
#Busca el articulo S seleccionado en la lista de articulos. 
#Retorna la lista de hijos (articulosL) correspondietes al articuloS. 
def buscarSelect(select):
    for i in listArticulos:
        if i.cod_articulo == select:
            return i.hijos
            break

#Configuracion del arbol de la ventana principal. 
def createTree():
    tree["columns"] = columns
    for i in columns:
        tree.column(i)
        tree.heading(i, text=i.capitalize())
    tree["show"] = "headings"
    tree.pack()
    tree.place(x=50, y=100,width=1300, height=550)
    tree.column('Codigo articulo', width=150)
    tree.column('Descripcion', width=310)
    tree.column('Saldo', width=100, anchor=CENTER)
    tree.column('Stock expedicion', width=100, anchor=CENTER)
    tree.column('Stock reservado', width=100, anchor=CENTER)
    tree.column('Maximas bolsas posibles', width=150, anchor=CENTER)
    tree.column('Fecha programada', width=160, anchor=CENTER)
    tree.column('Cantidad', width=100, anchor=CENTER)
    tree.column('Vendido', width=100, anchor=CENTER)
    tree.column('Pendiente pedido', width=110, anchor=CENTER)
    tree.bind('<Double-1>', moreInformation)
#-----------------------------------------------------------------------------------------------------------------------------   
def query():
    createTree()
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

