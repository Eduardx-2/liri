import requests
import json
import regex
from data.mov import MovDeuda
from data.mov import MovError
from data.check_info_num import NumberComp
from data.claro import DataNumberClaro
from data.desk_web import WebiSession
from data.desk_web import SocialNetwork
from concurrent.futures import ThreadPoolExecutor
class ApisSession:
    def __init__(self):
        self.REQ = requests.session()
#data_json: {"numero":""}
    def data_response(self,recivedPostdata:str)->dict:
        with ThreadPoolExecutor(max_workers=2) as exec_h:

            hilos_redes = exec_h.submit(SocialNetwork(recivedPostdata["numero"]).consultar)
            hilos_data = exec_h.submit(self.create_session_numb,recivedPostdata)
            datosRedes = hilos_redes.result()
            data =hilos_data.result() 
        data["dataNumRedes"] = datosRedes
        return data

    def create_session_numb(self,data_json:str)-> dict:

        if NumberComp().number_check_mov(data_json["numero"]) == 0:
            return self.session_id_create_movistar(data_json["numero"])
        elif (data := self.getTokens_claro_session(data_json["numero"])).status == 200:
            sendInfo = self.getDataclaro_info_num(data.data)
            if isinstance(sendInfo,MovDeuda):
                return {"compania": "Claro","docFactura":sendInfo.getDoc(),"monto":sendInfo.getMonto()}
            else:
                return {"errorNumero":sendInfo.getMensaje(),"compania":"Claro"}
        elif (tig0_num := WebiSession(data_json["numero"]).session_tigo_num()).getCodResponse() == 200:
            if isinstance(tig0_num,MovDeuda):
                return {"compania":"Tigo","factura":tig0_num.getFactura(),"monto":tig0_num.getMonto(),"docFactura":tig0_num.getDoc(),"fecha":tig0_num.getFecha()}
            else:
                return {"errorNumero": tig0_num.getMensaje(),"compañia":"Tigo"}
        else:
            return {"errorNumero":"Numero no encontrado o posible prepago"}

    def session_id_create_movistar(self,numero):
        
        url = "https://movistar.com.sv/movaa/admin-ajax.php"

        payload = f"------geckoformboundary324c518d05eaf692b7e74aba9ffbe294\nContent-Disposition: form-data; name=\"action\"\n\nobtenerFacturas\n------geckoformboundary324c518d05eaf692b7e74aba9ffbe294\nContent-Disposition: form-data; name=\"numero\"\n\n{numero}\n------geckoformboundary324c518d05eaf692b7e74aba9ffbe294--"
        headers = {
            'Host': 'movistar.com.sv',
            'Cookie': '_gcl_au=1.1.887886952.1787459042; _ga_6C7XSM46F1=GS2.1.s1787459042$o1$g0$t1787459042$j60$l0$h0; _ga=GA1.3.1913887759.1787459042; _gid=GA1.3.820263790.1787459043; _rlid=8d051d2a-54c3-4430-b8c0-9148e02ec13a; _fbp=fb.2.1787459044217.766371731463039731; _clck=kizzlr%5E2%5Eg8u%5E0%5E2426; _clsk=na7f0g%5E1787459045100%5E1%5E1%5Ef.clarity.ms%2Fcollect',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'multipart/form-data; boundary=----geckoformboundary324c518d05eaf692b7e74aba9ffbe294',
            'Content-Length': '298',
            'Origin': 'https://movistar.com.sv',
            'Referer': 'https://movistar.com.sv/pago-de-factura/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        }

        response = self.REQ.post(url, headers=headers, data=payload)
        sessidStation = MovError(mensaje=response.json()["data"]["message"],estado=response.json()["data"]["status"])
        match sessidStation.getEstado():
            case 1:
                return {"mensaje": sessidStation.getMensaje()}
            case 0:
                dataMov = self.data_web_movistar(response.text)
                if isinstance(dataMov,MovDeuda):
                    return {"compania": "Tigo", "docFactura":dataMov.docId(),"factura":dataMov.getFactura(),"monto":dataMov.getMonto(),"fecha":dataMov.getFecha()}
                else:
                    return {"errorNumero":dataMov.getMensaje(),"compania": "Tigo"}
            case 2:
                return {"error":"Ocurrio un error Desconocido"}
        
# Este metodo es el que tiene que verificar lo que reciba, entonces success?
# success, ok, pero success, puede ser también, un estado de factura nulo
    def data_web_movistar(self, response:str)-> MovDeuda | MovError:
        jsons = json.loads(response)
        if jsons["data"]["cantidad"] == 0:
            doc = jsons["data"]["documento"]
            return MovError(mensaje=f"Sin deudas pendientes: {doc}")
        else:
            doc = jsons['data']['documento']
            fact =  jsons['data']['facturas']
            fecha = regex.search("<strong>(.*?)</strong>",fact)
            factura = regex.findall(r"""['"]([^'"]+)['"]""",fact)[5]
            mont = regex.findall("\\s*(\\$[0-9]+(?:\\.[0-9]+)?)",fact)
            return MovDeuda(factura=factura,docId=doc,monto=mont,fecha=fecha)
            
    
    def getTokens_claro_session(self,numero) -> DataNumberClaro:
        uri = f"https://api-sv.mipagoclaro.com/invoice/api/MpcProfile/MobileNumber/503{numero}?app=mpc"
        headersList = {
            "Host": "api-sv.mipagoclaro.com",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://sv.mipagoclaro.com/",
            "Content-Type": "application/json",
            "Authorization": "undefined",
            "Origin": "https://sv.mipagoclaro.com",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors" 
        }
        req_token = self.REQ.get(uri,headers=headersList)
        if req_token.status_code == 200:
            return DataNumberClaro(status=200,data=req_token.json())
        else:
            return DataNumberClaro(status=400)
      
    def getDataclaro_info_num(self,token:str) -> MovDeuda | MovError:
        url = "https://api-sv.mipagoclaro.com/invoice/api/MpcInvoice"
        
        headersList = {
            "Host": "api-sv.mipagoclaro.com",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:156.0) Gecko/20100101 Firefox/156.0",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://sv.mipagoclaro.com/",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "Origin": "https://sv.mipagoclaro.com"  
        }

            # 
        reqs_claro = self.REQ.get(url,headers=headersList)
        if len(reqs_claro.json()["pendingInvoices"]) > 0:
            if reqs_claro.json()["pendingInvoices"][0]["dueAmount"] > 0:
                return MovDeuda(docId=reqs_claro.json()["pendingInvoices"][0]["reference"],
                        monto=reqs_claro.json()["pendingInvoices"][0]["dueAmount"],
                        fecha=reqs_claro.json()["pendingInvoices"][0]["dueDate"])
                    
            else:
                return MovError(mensaje="No tiene deudas")
        else:
            return MovError(mensaje="Sin deudas pendientes")


    
#data = ApisSession().data_response({"numero":"75"})
#print(data)
#ApisSession().session_id_create_movistar("36874")
#ApisSession.getDataclaro_info_num(745) 
