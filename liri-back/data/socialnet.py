class SocialOkData:
    def __init__(self, estado=None, mensaje=None):
        self.estado = estado
        self.mensaje = mensaje

    def dataString(self) -> dict:
        return {"estado": self.estado, "mensaje": self.mensaje}


class SocialError:
    def __init__(self,estado=None,mensaje=None):
        self.estado =estado
        self.mensaje =  mensaje

    def errorSocial(self):
        return {"estado":self.estado,"mensaje":self.mensaje}



