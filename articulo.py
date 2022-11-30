
class Articulo:

    def __init__(self, cod, des, stock):
        self.cod_articulo = cod
        self.descripcion = des
        self.stock = stock


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
        
