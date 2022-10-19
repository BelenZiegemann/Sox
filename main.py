from tkinter import*
from tkinter import ttk
from turtle import right, st
import pyodbc


root = Tk()
root.geometry('1430x300')
#root.resizable(0,0)
#root.config(bg="")
root.title('Sox')


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

def machineQuery():
    for i in tree.get_children():
        tree.delete(i)

    conexion = connectMe()
    cur = conexion.cursor()
    cur.execute(" SELECT DISTINCT (RTRIM(STA11.DESCRIPCIO) + ' - ' + STA11.DESC_ADIC) AS [DESCRIPCION] ,STA11.COD_ARTICU AS [COD ARTICULO] ,STA11.VALOR1 AS [TALLE],(SELECT TOP 1 (CASE IDPARENT WHEN 2 THEN UPPER(LTRIM(SUBSTRING(DESCRIP, 5, LEN(DESCRIP)))) WHEN 49 THEN ('SUBLIMADO - ' + UPPER(LTRIM(DESCRIP))) ELSE 'SIN DEFINIR' END) FROM STA11ITC CLASIFICACION LEFT JOIN STA11FLD FOLDER ON CLASIFICACION.IDFOLDER = FOLDER.IDFOLDER WHERE (IDPARENT = 2 OR IDPARENT = 49) AND CLASIFICACION.CODE = COD_ARTICU) AS [FAMILIA],ISNULL((SELECT SUM(CANT_PEN_D) FROM GVA03 DETALLEPEDIDO LEFT JOIN GVA21 PEDIDO ON DETALLEPEDIDO.NRO_PEDIDO = PEDIDO.NRO_PEDIDO AND DETALLEPEDIDO.TALON_PED = PEDIDO.TALON_PED WHERE DETALLEPEDIDO.COD_ARTICU = STA11.COD_ARTICU AND PEDIDO.FECHA_INGRESO > DATEADD(DD, -65, GETDATE()) AND PEDIDO.ESTADO IN (1,2) AND PEDIDO.COD_CLIENT NOT IN ('002042','Z02042','227') GROUP BY DETALLEPEDIDO.COD_ARTICU), 0) AS [PEDIDOS],ISNULL((SELECT COUNT(DISTINCT PEDIDO.NRO_PEDIDO) FROM GVA03 DETALLEPEDIDO LEFT JOIN GVA21 PEDIDO ON DETALLEPEDIDO.NRO_PEDIDO = PEDIDO.NRO_PEDIDO AND DETALLEPEDIDO.TALON_PED = PEDIDO.TALON_PED WHERE DETALLEPEDIDO.COD_ARTICU = STA11.COD_ARTICU AND PEDIDO.FECHA_INGRESO > DATEADD(DD, -65, GETDATE()) AND PEDIDO.ESTADO IN (1,2) AND PEDIDO.COD_CLIENT NOT IN ('002042','Z02042', '227') AND DETALLEPEDIDO.CANT_PEN_D > 0 GROUP BY DETALLEPEDIDO.COD_ARTICU), 0) AS [CANT_PEDIDOS],ISNULL((SELECT CANT_STOCK FROM STA19 WHERE COD_ARTICU = STA11.COD_ARTICU AND COD_DEPOSI = '30'), 0) AS [EXPEDICION], ISNULL((SELECT CANT_STOCK FROM STA19 WHERE COD_ARTICU = STA11.COD_ARTICU AND COD_DEPOSI = '90'), 0) AS [DEPOSITO FACTURACION], ISNULL((SELECT CONVERT(INT, MIN(CANT_STOCK)/MAX(STA03.CANTIDAD)) FROM STA19 INNER JOIN STA03 ON STA19.COD_ARTICU = STA03.COD_INSUMO WHERE COD_DEPOSI = '20' AND STA03.COD_ARTICU = STA11.COD_ARTICU),0) AS [BOLSAS_POSIBLES_LINEA], ISNULL((SELECT MIN(CANT_STOCK) FROM STA19 INNER JOIN STA03 ON STA19.COD_ARTICU = STA03.COD_INSUMO WHERE COD_DEPOSI = '10' AND STA03.COD_ARTICU = STA11.COD_ARTICU),0) AS [BOLSAS_POSIBLES_TEJEDURIA], (SELECT COD_MEDIDA FROM MEDIDA WHERE ID_MEDIDA = STA11.ID_MEDIDA_STOCK) AS [MEDIDA]	FROM STA11 WHERE STA11.COD_ARTICU LIKE 'S%'AND STA11.DESCRIPCIO NOT LIKE '%NO USAR%' AND USA_ESC = 'S' AND STA11.COD_ARTICU <> 'SERVICIO' GROUP BY STA11.COD_ARTICU, STA11.DESCRIPCIO, STA11.VALOR1, STA11.DESC_ADIC, STA11.ID_MEDIDA_STOCK ORDER BY [BOLSAS_POSIBLES_LINEA] DESC ")

    articulos = cur.fetchall()

    i=0
    for articulo in articulos:
        tree.insert("", i, text='', values=(articulo[0], articulo[1],articulo[2], articulo[3], articulo[4],
                                            articulo[5], articulo[6], articulo[7], articulo[8], articulo[9]))
        i = i + 1

    conexion.close()


#Metodo principal
def query():
    machineQuery()


#Configuraciones de la ventana y el arbol. 
tree = ttk.Treeview(root, columns=('descripcion', 'cod_articulo','talle', 'familia', 'pedidos', 'cant_pedidos',
                                    'expedicion','depo_facturacion' ,'bolsas_linea', 'bolsas_tejeduria', 'medida' ))
                                
tree.place(x=20, y=20)

tree['show'] = 'headings'


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





query()

root.mainloop()

