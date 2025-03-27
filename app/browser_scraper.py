from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from app.config import USERNAME, PASSWORD
import time

LOGIN_URL = "https://ipssalta.gob.ar/SeguroEscolar/login.aspx"
DEUDA_URL = "https://ipssalta.gob.ar/SeguroEscolar/Seguro/GesPlanillaAdministrar.aspx"

def extraer_tabla_deuda_con_selenium():
    print("[*] Iniciando navegador Selenium...")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--ignore-certificate-errors")

    driver = webdriver.Chrome(options=options)

    try:
        # Ir a login
        print(f"[*] Navegando a: {LOGIN_URL}")
        driver.get(LOGIN_URL)
        time.sleep(2)

        # Login automático
        print("[*] Autenticando usuario...")
        driver.find_element(By.ID, "txtUserName").send_keys(USERNAME)
        driver.find_element(By.ID, "txtPassword").send_keys(PASSWORD)
        driver.find_element(By.ID, "btnLogin").click()

        # Esperar redirección post-login
        time.sleep(3)

        # Ir a página con tabla
        print(f"[*] Navegando a: {DEUDA_URL}")
        driver.get(DEUDA_URL)
        time.sleep(5)

        # Extraer tabla deudas
        tabla = driver.find_element(By.ID, "tblPlanilla")
        filas = tabla.find_elements(By.TAG_NAME, "tr")

        print("\n🧾 TABLA DE DEUDA DETECTADA:\n")
        with open("output/tabla_deuda.txt", "w", encoding="utf-8") as out:
            for fila in filas:
                celdas = fila.find_elements(By.TAG_NAME, "th") or fila.find_elements(By.TAG_NAME, "td")
                texto = [col.text.strip() for col in celdas]
                linea = "\t".join(texto)
                if linea:
                    print(linea)
                    out.write(linea + "\n")

    except Exception as e:
        print(f"[-] Error al extraer tabla: {e}")

    finally:
        driver.quit()
