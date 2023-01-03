
class Articulo:

    def __init__(self, cod, des, stock):
        self.cod_articulo = cod
        self.descripcion = des
        self.stockExpedicion = stock

    def getStock(self):
        return self.descripcion


class ArticuloS(Articulo):

    hijos = []
    nietos = []

    def __init__(self, cod, des, stockE, stockR, necesitaL, hijos, nietos, fecha_prog, orden, cant,
                 estado, max_bolsas_linea, max_bolsas_tejeduria, vendido, pedido, saldo, vendidoAnual):
        super().__init__(cod, des, stockE)
        self.stockReservado = stockR
        self.necesitaL = necesitaL
        self.hijos = [hijos]
        self.nietos = [nietos]
        self.fecha = fecha_prog
        self.orden = orden
        self.cant = cant
        self.estado = estado
        self.max_bolsasL = max_bolsas_linea
        self.max_bolsasT = max_bolsas_tejeduria
        self.vendidoTrimestral = vendido
        self.pedido = pedido
        self.saldo = saldo
        self.vendidoAnual = vendidoAnual
    
    def agregarHijo(self, hijo=[]):
        self.hijos.append(hijo)
    
    def agregarNieto(self, nieto=[]):
        self.nietos.append(nieto)


class ArticuloL(Articulo):

    hijos = []

    def __init__(self, cod, des, stock, necesitaT, hijos):
        super().__init__(cod, des, stock)
        self.necesitaT = necesitaT
        self.hijos = [hijos]

    def agregarHijo(self, hijo=[]):
        self.hijos.append(hijo)
        

class ArticuloT(Articulo):

    def __init__(self, cod, des, stock):
        super().__init__(cod, des, stock)
        
