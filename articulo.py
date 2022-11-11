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

    def __init__(self, cod, des, stockE, stockR, necesitaL, hijos, nietos, fecha_prog, orden, cant, estado, max_bolsas_linea):
        super().__init__(cod, des,stockE)
        self.stockReservado = stockR
        self.necesita = necesitaL
        #self.necesitaTejeduria = necesitaT
        self.hijos = [hijos]
        self.nietos = [nietos]
        self.fecha = fecha_prog
        self.orden = orden
        self.cant = cant
        self.estado = estado
        self.max_bolsas = max_bolsas_linea
    
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
#Modificar algunos atributos de los objetos (herencia). (Listo)
#Agregar a la ventana principal columnas: vendido y pedidos a entregar. 
#Agregar la nueva consulta.
#Realizar una sola consulta a la base de datos.
#Agregar atributos al articulo S: fecha de orden programada, cantidad, maximas bolsas posibles en linea.
#Agregar max bolsas posibles en linea a la nueva consulta. 