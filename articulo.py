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

    def __init__(self, cod, des, stockE, stockR, necesitaL, necesitaT, hijos, nietos):
        super().__init__(cod, des)
        self.stockExpedicion = stockE
        self.stockReservado = stockR
        self.necesitaLinea = necesitaL
        self.necesitaTejeduria = necesitaT
        self.hijos = [hijos]
        self.nietos = [nietos]
    
    def agregarHijo(self,hijo=[]):
        self.hijos.append(hijo)
        #print("hijos en agregar: ", self.hijos)
    
    def agregarNieto(self,nieto=[]):
        self.nietos.append(nieto)
        #print("nietos en agregar: ", self.nietos)

    def getHijos(self):
        return [self.hijos]


class ArticuloL(Articulo):

    hijos = []

    def __init__(self, cod, des, stock, hijos):
        super().__init__(cod, des)
        self.stockLinea = stock
        self.hijos = [hijos]

    def agregarHijo(self,hijo=[]):
        self.hijos.append(hijo)
        

class ArticuloT(Articulo):

    def __init__(self, cod, des, stock):
        super().__init__(cod, des)
        self.stockTejeduria = stock