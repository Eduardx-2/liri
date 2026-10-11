import time
import re
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
from data.mov import MovError
from data.mov import MovDeuda
#from mov import MovError,MovDeuda

from data.socialnet import SocialOkData, SocialError

class SocialNetwork:
    def __init__(self,numero):
        self.URIFB = "https://www.facebook.com/"
        self.INSTA = "https://www.instagram.com/"
        self.numero = numero
        self.driver = None
        self._tab_instagram = None
        self._tab_facebook = None

    def _navegador(self):
        if self.driver is None:
            opt = Options()
            opt.add_argument("-headless")
            self.driver = webdriver.Firefox(options=opt)
            self._tab_instagram = self.driver.current_window_handle
            self.driver.switch_to.new_window("tab")
            self._tab_facebook = self.driver.current_window_handle
        return self.driver

    def cerrar(self):
        if self.driver is not None:
            self.driver.quit()
            self.driver = None
            self._tab_instagram = None
            self._tab_facebook = None

    def instagrams_session(self) -> dict:
        LABEL = (
           "//label[contains(., 'Mobile number') or contains(., 'username') "
           "or contains(., 'email') or contains(., 'celular') or contains(., 'correo')]"
        )
        ERRORS = (
           "//span[contains(., 'No account found') "
           "or contains(., 'No se encontró ninguna cuenta')]"
         )
        webingInstagram = self._navegador()
        webingInstagram.switch_to.window(self._tab_instagram)
        webingInstagram.get(self.INSTA)
        btnPass = WebDriverWait(driver=webingInstagram,timeout=10).until(
            EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div/div[1]/div/div/div/div/div[3]/div/div/div/div/div/div/div/div/div[2]/form/div/div[1]/div/div[4]/div/a"))
        )
        webingInstagram.execute_script("arguments[0].click()",btnPass)
        time.sleep(3)
        btnReset = WebDriverWait(driver=webingInstagram,timeout=20).until(
            EC.element_to_be_clickable((By.XPATH, LABEL + "/preceding-sibling::input[@type='text']"))
        )
        btnReset.click()
        btnReset.clear()
        btnReset.send_keys(self.numero)
        btnOk = WebDriverWait(driver=webingInstagram,timeout=30).until(
            EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div/div[1]/div[1]/div/div/div/div/div/div[1]/div[3]/div/div/div/div/div/div/div"))
        )
        webingInstagram.execute_script("arguments[0].click()",btnOk)
        try:
            data = WebDriverWait(driver=webingInstagram,timeout=20).until(
                lambda d: next((e for e in d.find_elements(By.XPATH, ERRORS) if e.is_displayed()), False)
            )
            confirm = data.text.strip()
        except TimeoutException:
            confirm = None

        if confirm == None:
            return SocialOkData(estado=True, mensaje="Instagram").dataString()
        else:
            return SocialError(estado=False,mensaje=confirm).errorSocial()
        

    def facebook_inicie_session(self, number) -> dict:
        ERROR = (
            "//span[contains(., 'No se encontró ninguna cuenta') "
            "or contains(., 'No account found')]"
        )
        webingDriverSocial = self._navegador()
        webingDriverSocial.switch_to.window(self._tab_facebook)
        webingDriverSocial.get(self.URIFB)
        btnOlvd = WebDriverWait(driver=webingDriverSocial,timeout=30).until(
            EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div/div/div/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div/div[3]/div/div/div/div/div/div/div/div/div[2]/form/div/div[1]/div/div[4]/div/a"))
        )
        webingDriverSocial.execute_script("arguments[0].click()", btnOlvd)
        time.sleep(1)
        dataInput = WebDriverWait(webingDriverSocial, 45).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//label[contains(., 'Mobile number') or contains(., 'email') "
                "or contains(., 'móvil') or contains(., 'correo')]"
                "/preceding-sibling::input[@type='text']"
            ))
        )
        time.sleep(3)
        dataInput.click()
        dataInput.clear()
        dataInput.send_keys(self.numero)
        btnSend = WebDriverWait(driver=webingDriverSocial,timeout=30).until(
            EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div[1]/div/div/div/div[1]/div[1]/div/div/div/div/div/div[1]/div[3]/div/div/div/div/div/div/div/div"))
        )
        time.sleep(2)
        webingDriverSocial.execute_script("arguments[0].click()",btnSend)
        try:
            msg = WebDriverWait(driver=webingDriverSocial, timeout=7).until(
                EC.presence_of_element_located((By.XPATH, ERROR))
            )
            errorDetected = msg.text.strip()
        except TimeoutException:
            errorDetected = None
        if errorDetected == None:
            
            okData = SocialOkData(estado=True,mensaje="Facebook")
            return okData.dataString()
        else:
            error = SocialError(estado=False,mensaje=errorDetected)
            return error.errorSocial()

    def consultar(self) -> dict:
        resultado = {}
        try:
            try:
                resultado["instagram"] = self.instagrams_session()
            except Exception as exc:
                resultado["instagram"] = SocialError(estado=False, mensaje=str(exc)).errorSocial()
            try:
                resultado["facebook"] = self.facebook_inicie_session(self.numero)
            except Exception as exc:
                resultado["facebook"] = SocialError(estado=False, mensaje=str(exc)).errorSocial()
            return resultado
        finally:
            self.cerrar()


class WebiSession:
    def __init__(self,number):
       self.number = number
       
   
#verdaderamente estoy retomando esta mierda despues de 3 semanas, no me acuerdo un carajo
    def session_tigo_num(self)-> MovDeuda |  MovError:
        opts = Options()
        opts.add_argument("-headless")
        webingT = webdriver.Firefox(options=opts)
        windowsSessid = webingT.current_window_handle
        webingT.get("https://www.tigo.com.sv/pago-de-facturas")
        
        btnAcces = WebDriverWait(driver=webingT,timeout=30).until(
            EC.element_to_be_clickable((By.XPATH,"/html/body/app-root/div/main/app-page/or-themed-column-container[1]/section/div/div/div[1]/ml-media-vertical/a/div/div[2]/at-button/a"))
        )
        webingT.execute_script("arguments[0].click()",btnAcces)
        #//*[@id="messageNoLink"]
        # si encuentra el message, no se tiene ejcutar lo demas
        WebDriverWait(driver=webingT,timeout=8).until(EC.number_of_windows_to_be(2))
        newWind = (set(webingT.window_handles) - {windowsSessid}).pop()
        webingT.switch_to.window(newWind)
        #No necesito agregar un sleep, lo hago directamente con js
        # Por que js? si usara click() el diseño de ion haria que fallara, la transiccion de ion es la que haría que fallaba 
        btnIndexNum = WebDriverWait(driver=webingT,timeout=30).until(
            EC.element_to_be_clickable((By.XPATH,"/html/body/mitigo-root/ion-app/ion-router-outlet/mitigo-express/ion-content/ion-card/ion-grid/ion-row[3]/ion-col[2]/div"))
        )

        webingT.execute_script("arguments[0].click();", btnIndexNum)
        inputInfoNum =  WebDriverWait(driver=webingT,timeout=30).until(
            EC.element_to_be_clickable((By.XPATH,"/html/body/mitigo-root/ion-app/ion-router-outlet/mitigo-express/ion-content/ion-card/ion-grid/div/ion-row/ion-col/ion-item/ion-input/input"))
        )
        
        webingT.execute_script("arguments[0].click()",inputInfoNum)
        inserData = WebDriverWait(driver=webingT, timeout=30).until(
            EC.element_to_be_clickable((By.XPATH,"/html/body/mitigo-root/ion-app/ion-router-outlet/mitigo-express/ion-content/ion-card/ion-grid/div/ion-row/ion-col/ion-item/ion-input/input"))
        )
        #time.sleep(2.3)#un sleep ciego, si no, el programa colapsa
        inserData.send_keys(self.number)

        insertKeySend =  WebDriverWait(driver=webingT,timeout=30).until(
            EC.element_to_be_clickable((By.XPATH,'//*[@id="onSubmitChangeNameForm"]'))
        )
        time.sleep(3)
        webingT.execute_script("arguments[0].click()",insertKeySend)
        time.sleep(2)
        try:
            WebDriverWait(driver=webingT,timeout=25).until(
                EC.presence_of_element_located((By.XPATH,"/html/body/mitigo-root/ion-app/ion-router-outlet/mitigo-express/mitigo-alert"))
            )
            dataError = webingT.execute_script("return document.getElementById('messageNoLink')?.textContent")
        #web alert: /html/body/mitigo-root/ion-app/ion-router-outlet/mitigo-express/mitigo-alert
        except TimeoutException:
            dataError = None
        if dataError == None:
            WebDriverWait(driver=webingT, timeout=25).until(
                lambda script:script.execute_script('var d=document.querySelector("wc-billing-dashboard"); return d && d.shadowRoot && d.shadowRoot.querySelectorAll(".billing-info-block").length >= arguments[0];',4)
            )
            time.sleep(5)
            data = webingT.execute_script("""return [...document.querySelector("wc-billing-dashboard").shadowRoot.querySelectorAll(".billing-info-block")].map(el => el.innerText);""")
            factura = re.search(r'\d{1}',data[0])
            ref_pag = re.search(r'\d{8}',data[1])
            findFecha = re.search(r'\d{2}/\d{2}/\d{4}',data[3])
            return MovDeuda(codResponse=200,factura=factura.group(),docId=ref_pag.group(),fecha=findFecha.group(),monto=data[2])
            
        else:
            
            return MovError(mensaje=dataError,codResponse=404)
            webingT.close()


