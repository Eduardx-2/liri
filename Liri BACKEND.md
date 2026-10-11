
# data/mov

 Este archivo contiene dos clases:
 - MovError
 - MovDeuda
 MovDeuda: Está clase es la encargada de obtener los datos en dado caso el número contenga deudas, lo que quiere decir que va mostrar estos datos:
```
   self.factura = factura
   self.docId = docId
   self.monto = monto
   self.fecha = fecha
   self.numCuenta = numCuenta
   self.codResponse = codResponse
```

Cuál es la idea? Poder tener control de los datos, aquí se podría implementar un solo metodo que se encargue de retornar todos estos datos en forma de dict: {}, claro es posible, pero, tenga en cuenta que cada compañia muestra diferentes datos, unos pueden mostrar factura, otros no, por dicha razón, yo implemento:
```
 def __init__(self,factura=None,docId=None,monto=None,fecha=None, numCuenta=None,codResponse=None):
```

Los datos de entrada pueden variar por ende ocupo None, para especificar que dato entra y cuál obtiene None.

Tenér metodos de get definidos me da un control importante a la hora de crear los dict con información, al ser datos que pueden variar, no se puede tener una función que haga lo siguente:

```
def data_dicts(self):
     return {"compañia": getCompañia(),"numero": getNUmber()}
```

> [!Code]
> **Por lo antes dicho, los datos pueden variar dependiendo de la compañia, por eso los metodos get son importantes, si no, tendría que estar verificando compañia cada vez que de uso de dichas clases, lo cuál no combiene.**

# Instance

La instancia se crea apartir del script situado en la carpeta "data/", entonces en que se usa?  
```
  if isinstance(sendInfo,MovDeuda):
```
Las clases encargadas de recolectar la información devuelve lo siguente:

```
 -> MovDeuda | MovError:
```

>[!Rama]
>Vean las dos clases como dos ramas, (MovDeuda->Rama) (MovError -> Rama)
>

Estan devolviendo dos clases, deuda y error, eso signfica, si ocurre un error la clase que se va mostrar es MovError, pero si no ocurre un error -> MovDeuda, entonces, ahí es donde entra la instancia, verificando que rama se esta devolviendo.

Con esto obtengo un mejor control para poder crear los dict con información;<span style="color:rgb(255, 0, 0)"> Revise data/mov</span>, en ese articulo se asume que no se puede tener un metodo que devuelva estos dicts; dicho porque puede variar la información, al verificar las instancia de las funciones eso cambia, puede verlo reflejado aquí:

```
 if isinstance(sendInfo,MovDeuda):
                return {"compania": "Claro","docFactura":sendInfo.getDoc(),"monto":sendInfo.getMonto()}
            else:
                return {"errorNumero":sendInfo.getMensaje()}
```
>[!Get]
> Los campos get son los datos que se retornan```
>  def getMonto(self): return self.monto```

Con diferencía de los demas dict este solo cuenta con 2 campos get.