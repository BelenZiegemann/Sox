from re import S

class Articulo:

    def __init__(self, cod, des):
        self.cod_articulo = cod
        self.descripcion = des

    def getCodigo(self):
        return self.cod_articulo
    
    def getDescripcion(self):
        return self.descripcion

class ArticuloS(Articulo):

    hijos = []
    nietos = []

    def __init__(self, cod, des, stockE, stockR, necesitaL, necesitaT):
        super().__init__(cod, des)
        self.stockExpedicion = stockE
        self.stockReservado = stockR
        self.necesitaLinea = necesitaL
        self.necesitaTejedura = necesitaT

    
    def agregarHijo(self,hijo):
        self.hijos.append(hijo)
    


class ArticuloL(Articulo):

    def __init__(self, cod, des, stock):
        super().__init__(cod, des)
        self.stockLinea = stock

class ArticuloT(Articulo):

    def __init__(self, cod, des, stock):
        super().__init__(cod, des)
        self.stockTejeduria = stock