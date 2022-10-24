from distutils.command.config import config
from tkinter import*
from tkinter import ttk
from turtle import left, right, st, width
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

#Consulta la info en la base de datos y los muestra en forma de tabla. 
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

    articulos = cur.fetchall()

    i=0
    for articulo in articulos:
        tree.insert("", i, text='', values=(articulo[0], articulo[1],articulo[2], articulo[3], articulo[4],
                                            articulo[5], articulo[6], articulo[7], articulo[8], articulo[9], articulo[10]))
        i = i + 1
        

    conexion.close()
    return articulos

def check(e):
    typed = entry.get()
    if typed == '':
        data = datos
    else:
        data = []
        for item in datos:
            if typed.lower() in item.lower():
                data.append(item)
                print(data)

    
def query():
    mainQuery()
    
#Frame para el filtro
frame1 = Frame(root, height=200)
frame1.pack(fill="x")
frame1.config(borderwidth=10,highlightbackground="black", highlightthickness=1, bg="green")
#Label, entry y button para el frame1
label = Label(frame1, text="Ingresar codigo", bg="blue")
label.pack(side= LEFT, anchor= W, pady=10, padx=10)
entry = Entry(frame1)
entry.pack(side=LEFT, anchor=W, pady=10, padx=10)
button = Button(frame1, text="Mas informacion", bg="yellow")
button.pack(side=RIGHT, anchor=E, pady=10, padx=10)

columns = ['descripcion', 'cod_articulo','talle', 'familia', 'pedidos', 'cant_pedidos',
            'expedicion','depo_facturacion' ,'bolsas_linea', 'bolsas_tejeduria', 'medida']

tree = ttk.Treeview(root, columns=columns, show='headings')

tree.column('medida', width=100)
tree.column('talle', width=100)

tree.heading('descripcion', text='Descripcion')
tree.heading('cod_articulo', text='Codigo articulo')
tree.heading('talle', text='Talle')
tree.heading('familia', text='Familia')
tree.heading('pedidos', text='Pedidos')
tree.heading('cant_pedidos', text='Cantidad pedidos')
tree.heading('expedicion', text='Expedicion')
tree.heading('depo_facturacion', text='Deposito facturacion')
tree.heading('bolsas_linea', text='Bolsas en linea')
tree.heading('bolsas_tejeduria', text='Bolsas en tejeduria')
tree.heading('medida', text='Medida')

tree.pack()

scrollbarx = ttk.Scrollbar(root, orient=HORIZONTAL)
scrollbarx.configure(command=tree.xview)
tree.configure(xscrollcommand=scrollbarx.set)
scrollbarx.pack(side=BOTTOM, fill="x")

scrollbary = ttk.Scrollbar(root, orient=VERTICAL)
scrollbary.configure(command=tree.yview)
tree.configure(yscrollcommand=scrollbary.set)
scrollbary.pack(side= RIGHT, fill=Y, ipady=40)


tree.place(x=50, y=100,width=1300, height=500)

entry.bind("<KeyRelease>", check)


datos = mainQuery()
entry.bind("<KeyRelease>", check)

root.mainloop()

