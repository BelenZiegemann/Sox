from re import S

class Articulo:

    def __init__(self, cod, des, stock):
        self.cod_articulo = cod
        self.descripcion = des
        self.stock = stock

    def getCodigo(self):
        return self.cod_articulo
    
    def getDescripcion(self):
        return self.descripcion

class ArticuloS(Articulo):

    hijos = []
    nietos = []

    def __init__(self, cod, des, stockE, stockR, necesitaL, hijos, nietos, fecha_prog, orden, cant, estado, max_bolsas_linea,vendido,pedido,saldo):
        super().__init__(cod, des,stockE)
        self.stockReservado = stockR
        self.necesita = necesitaL
        self.hijos = [hijos]
        self.nietos = [nietos]
        self.fecha = fecha_prog
        self.orden = orden
        self.cant = cant
        self.estado = estado
        self.max_bolsas = max_bolsas_linea
        self.vendido = vendido
        self.pedido = pedido
        self.saldo = saldo
    
    def agregarHijo(self,hijo=[]):
        self.hijos.append(hijo)
    
    def agregarNieto(self,nieto=[]):
        self.nietos.append(nieto)



class ArticuloL(Articulo):

    hijos = []

    def __init__(self, cod, des, stock, necesitaT, hijos):
        super().__init__(cod, des, stock)
        self.necesita = necesitaT
        self.hijos = [hijos]

    def agregarHijo(self,hijo=[]):
        self.hijos.append(hijo)
        

class ArticuloT(Articulo):

    def __init__(self, cod, des, stock):
        super().__init__(cod, des, stock)
        

#Correcciones:
#Modificar algunos atributos de los objetos (herencia). (Listo).
#Agregar a la ventana principal columnas: vendido y pedidos a entregar. (Listo).
#Agregar la nueva consulta. (Listo)
#Realizar una sola consulta a la base de datos. (Listo)
#Agregar atributos al articulo S: fecha de orden programada, cantidad, maximas bolsas posibles en linea. (Listo).
#Agregar max bolsas posibles en linea a la nueva consulta. (Listo).
#Agregar scrollbarx en la nueva ventana. (Listo)
#Agregar saldo. (como tercer columna). 
#Hacer consulta de vendido y pedido a entregar. 



#ARTICULO DE146C SURTIDO DEVUELVE TODOS NULLS.
#Articulo TE132B IGUAL. 
#Articulo DE01C TALLE 5 GRISMEL.
