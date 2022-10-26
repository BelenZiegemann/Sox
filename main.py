from distutils.command.config import config
from hashlib import new
from tkinter import*
from tkinter import ttk
from turtle import heading, left, right, st, width
import pyodbc


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
    
    cur.execute(" SELECT DISTINCT (RTRIM(STA11.DESCRIPCIO) + ' - ' + STA11.DESC_ADIC) AS [DESCRIPCION]," +
                 "STA11.COD_ARTICU AS [COD ARTICULO] ,STA11.VALOR1 AS [TALLE]," +
                 "(SELECT TOP 1 (CASE IDPARENT WHEN 2 THEN UPPER(LTRIM(SUBSTRING(DESCRIP, 5, LEN(DESCRIP)))) WHEN 49 THEN ('SUBLIMADO - ' + UPPER(LTRIM(DESCRIP))) ELSE 'SIN DEFINIR' END) "+
                 "FROM STA11ITC CLASIFICACION LEFT JOIN STA11FLD FOLDER ON CLASIFICACION.IDFOLDER = FOLDER.IDFOLDER WHERE (IDPARENT = 2 OR IDPARENT = 49) AND CLASIFICACION.CODE = COD_ARTICU) AS [FAMILIA]," +
                 "ISNULL((SELECT SUM(CANT_PEN_D) FROM GVA03 DETALLEPEDIDO LEFT JOIN GVA21 PEDIDO ON DETALLEPEDIDO.NRO_PEDIDO = PEDIDO.NRO_PEDIDO AND DETALLEPEDIDO.TALON_PED = PEDIDO.TALON_PED WHERE DETALLEPEDIDO.COD_ARTICU = STA11.COD_ARTICU AND PEDIDO.FECHA_INGRESO > DATEADD(DD, -65, GETDATE()) AND PEDIDO.ESTADO IN (1,2) AND PEDIDO.COD_CLIENT NOT IN ('002042','Z02042','227') GROUP BY DETALLEPEDIDO.COD_ARTICU), 0) AS [PEDIDOS],"+
                 "ISNULL((SELECT COUNT(DISTINCT PEDIDO.NRO_PEDIDO) FROM GVA03 DETALLEPEDIDO LEFT JOIN GVA21 PEDIDO ON DETALLEPEDIDO.NRO_PEDIDO = PEDIDO.NRO_PEDIDO AND DETALLEPEDIDO.TALON_PED = PEDIDO.TALON_PED WHERE DETALLEPEDIDO.COD_ARTICU = STA11.COD_ARTICU AND PEDIDO.FECHA_INGRESO > DATEADD(DD, -65, GETDATE()) AND PEDIDO.ESTADO IN (1,2) AND PEDIDO.COD_CLIENT NOT IN ('002042','Z02042', '227') AND DETALLEPEDIDO.CANT_PEN_D > 0 GROUP BY DETALLEPEDIDO.COD_ARTICU), 0) AS [CANT_PEDIDOS],"+
                 "ISNULL((SELECT CONVERT(INT,CANT_STOCK) FROM STA19 WHERE COD_ARTICU = STA11.COD_ARTICU AND COD_DEPOSI = '30'), 0) AS [EXPEDICION], ISNULL((SELECT CANT_STOCK FROM STA19 WHERE COD_ARTICU = STA11.COD_ARTICU AND COD_DEPOSI = '90'), 0) AS [DEPOSITO FACTURACION],"+
                 "ISNULL((SELECT CONVERT(INT, MIN(CANT_STOCK)/MAX(STA03.CANTIDAD)) FROM STA19 INNER JOIN STA03 ON STA19.COD_ARTICU = STA03.COD_INSUMO WHERE COD_DEPOSI = '20' AND STA03.COD_ARTICU = STA11.COD_ARTICU),0) AS [BOLSAS_POSIBLES_LINEA],"+
                 "ISNULL((SELECT MIN(CANT_STOCK) FROM STA19 INNER JOIN STA03 ON STA19.COD_ARTICU = STA03.COD_INSUMO WHERE COD_DEPOSI = '10' AND STA03.COD_ARTICU = STA11.COD_ARTICU),0) AS [BOLSAS_POSIBLES_TEJEDURIA],"+
                 "(SELECT COD_MEDIDA FROM MEDIDA WHERE ID_MEDIDA = STA11.ID_MEDIDA_STOCK) AS [MEDIDA]"+
                 "FROM STA11 WHERE STA11.COD_ARTICU LIKE 'S%'AND STA11.DESCRIPCIO NOT LIKE '%NO USAR%' AND USA_ESC = 'S' AND STA11.COD_ARTICU <> 'SERVICIO' "+
                 "GROUP BY STA11.COD_ARTICU, STA11.DESCRIPCIO, STA11.VALOR1, STA11.DESC_ADIC, STA11.ID_MEDIDA_STOCK ORDER BY [BOLSAS_POSIBLES_LINEA] DESC ")
    """
    cur.execute("SELECT STA11.COD_ARTICU, (RTRIM(STA11.DESCRIPCIO) + ' - ' + RTRIM(STA11.DESC_ADIC)) AS [DESCRIPCION], "+
                "ISNULL(STOCKEXP.CANT_STOCK, 0) AS [STOCKEXPEDICION],"+
                "ISNULL(STOCKRES.CANT_STOCK, 0) AS [STOCKRESERVADO], "+
                "INSUMOS.COD_INSUMO AS [INSUMOLINEA], "+
                "(RTRIM(ARTICULOLINEA.DESCRIPCIO) + ' - ' + RTRIM(ARTICULOLINEA.DESC_ADIC)) AS [DESCRIPCIONINSUMO], "+
                "ISNULL(STOCKLINEA.CANT_STOCK, 0) AS [STOCKLINEA],"+
                "INSUMOSTEJEDURIA.COD_INSUMO AS [INSUMOTEJEDURIA], "+
                "(RTRIM(ARTICULOTEJEDURIA.DESCRIPCIO) + ' - ' + RTRIM(ARTICULOTEJEDURIA.DESC_ADIC)) AS [DESCRIPCIONINSUMOTEJ], "+
                "ISNULL(STOCKTEJEDURIA.CANT_STOCK, 0) AS [STOCKTEJEDURIA]"+
                "FROM STA11ITC CATALOGO"+
                "INNER JOIN STA11 ON CATALOGO.CODE = STA11.COD_ARTICU"+
                "LEFT JOIN STA19 STOCKEXP ON STOCKEXP.COD_ARTICU = STA11.COD_ARTICU AND STOCKEXP.COD_DEPOSI = '30'"+
                "LEFT JOIN STA19 STOCKRES ON STOCKRES.COD_ARTICU = STA11.COD_ARTICU AND STOCKRES.COD_DEPOSI = '90'"+
                "LEFT JOIN STA03 INSUMOS ON INSUMOS.COD_ARTICU = STA11.COD_ARTICU AND COD_INSUMO LIKE 'L%' "+
                "LEFT JOIN STA19 STOCKLINEA ON STOCKLINEA.COD_ARTICU = INSUMOS.COD_INSUMO AND STOCKLINEA.COD_DEPOSI = '20' "+
                "LEFT JOIN STA11 ARTICULOLINEA ON ARTICULOLINEA.COD_ARTICU = INSUMOS.COD_INSUMO "+
                "LEFT JOIN STA03 INSUMOSTEJEDURIA ON INSUMOSTEJEDURIA.COD_ARTICU = INSUMOS.COD_INSUMO AND INSUMOSTEJEDURIA.COD_INSUMO LIKE 'T%' "+
                "LEFT JOIN STA19 STOCKTEJEDURIA ON STOCKTEJEDURIA.COD_ARTICU = INSUMOSTEJEDURIA.COD_INSUMO AND STOCKTEJEDURIA.COD_DEPOSI = '10' "+
                "LEFT JOIN STA11 ARTICULOTEJEDURIA ON ARTICULOTEJEDURIA.COD_ARTICU = INSUMOSTEJEDURIA.COD_INSUMO "+
                "WHERE STA11.COD_ARTICU LIKE 'S%' "+
                "AND STA11.DESCRIPCIO NOT LIKE '%NO USAR%' "+
                "AND CATALOGO.IDFOLDER = 90 "+
                "AND STA11.USA_ESC = 'S' ")
    """
    articulos = cur.fetchall()

    i=0
    for articulo in articulos:
        tree.insert("", i, text='', values=(articulo[0], articulo[1],articulo[2], articulo[3], articulo[4],
                                            articulo[5], articulo[6], articulo[7], articulo[8], articulo[9], articulo[10]))
        i = i + 1
        
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
columns = ['Descripcion', 'Codigo articulo','Talle', 'Familia', 'Pedidos', 'Cantidad pedidos',
            'Expedicion','Deposito facturacion' ,'Bolsas en linea', 'Bolsas en tejeduria', 'Medida']

tree = ttk.Treeview(root)
tree["columns"] = columns
for i in columns:
    tree.column(i)
    tree.heading(i, text=i.capitalize())
tree["show"] = "headings"
tree.pack()
tree.place(x=50, y=100,width=1300, height=550)
tree.column('Descripcion', width=350)
tree.column('Talle', width=100, anchor=CENTER)
tree.column('Medida', width=80, anchor=CENTER)
tree.column('Cantidad pedidos', width=100, anchor=CENTER)
tree.column('Expedicion', width=80, anchor=CENTER)
tree.column('Bolsas en linea', width=90, anchor=CENTER)
tree.column('Bolsas en tejeduria', width=100, anchor=CENTER)
tree.column('Pedidos', width=120, anchor=CENTER)

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

