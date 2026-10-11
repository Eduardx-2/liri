class MovDeuda:

    def __init__(self,factura=None,docId=None,monto=None,fecha=None, numCuenta=None,codResponse=None):
        self.factura = factura
        self.docId = docId
        self.monto = monto
        self.fecha = fecha
        self.numCuenta = numCuenta
        self.codResponse = codResponse


    def getFecha(self):
        return self.fecha

    def getMonto(self):
        return self.monto

    def getDoc(self):
        return self.docId

    def getFactura(self):
        return self.factura

    def getNumCuenta(self):
        return self.numCuenta

    def getCodResponse(self):
        return self.codResponse
class MovError:

    def __init__(self,mensaje,estado=None,codResponse=None):
        self.mensaje = mensaje
        self.estado = estado
        self.codResponse = codResponse

    def getMensaje(self):
        return self.mensaje

    def getCodResponse(self):
        return self.codResponse
    def getEstado(self) -> int:
        if self.estado == "error":
            return 1
        elif self.estado == "success":
            return 0

        return 2
