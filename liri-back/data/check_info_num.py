import requests

class NumberComp:
    def __init__(self):
        self.R3Q = requests.session()
        self.URIM = "https://movistar.com.sv/movaa/admin-ajax.php"

    def number_check_mov(self, numero)-> int:
        headersList = {
            "Host": "movistar.com.sv",
            "Cookie": "_gcl_au=1.1.887886952.1787459042.1016149077.1787549190.1787550730.1014869937.1787546087.1787550730; _ga_6C7XSM46F1=GS2.1.s1788641676$o6$g0$t1788641676$j60$l0$h0; _ga=GA1.3.1913887759.1787459042; _rlid=8d051d2a-54c3-4430-b8c0-9148e02ec13a; _fbp=fb.2.1787459044217.766371731463039731; _clck=kizzlr%5E2%5Eg97%5E0%5E2426; _gid=GA1.3.2035787189.1788641677; _clsk=1deglba%5E1788641678691%5E1%5E1%5Ek.clarity.ms%2Fcollect",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "multipart/form-data; boundary=----geckoformboundary3707365f967902ee46177dbb7ee8a102",
            "Content-Length": "304",
            "Origin": "https://movistar.com.sv",
            "Referer": "https://movistar.com.sv/pago-de-factura/" 
        }
        payload = f"------geckoformboundary3707365f967902ee46177dbb7ee8a102\nContent-Disposition: form-data; name=\"action\"\n\nvalidarNumeroMovistar\n------geckoformboundary3707365f967902ee46177dbb7ee8a102\nContent-Disposition: form-data; name=\"numero\"\n\n{numero}\n------geckoformboundary3707365f967902ee46177dbb7ee8a102--\n"
        req_ = self.R3Q.post(url=self.URIM,headers=headersList,data=payload)
    
        if req_.json()["status"] == "error":
            return 1
        return 0
#la función ya responde, solo es de implementarla


