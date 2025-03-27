import time
from selenium.webdriver.common.by import By

def mostrar_planillas(driver):
    print("[*] Cargando tabla de planillas...")
    driver.get("https://ipssalta.gob.ar/SeguroEscolar/Seguro/GesPlanillaAdministrar.aspx")
    time.sleep(5)  # Importante: darle tiempo al JS

    tabla = driver.find_element(By.ID, "tblPlanilla")
    filas = tabla.find_elements(By.TAG_NAME, "tr")

    for fila in filas:
        celdas = fila.find_elements(By.TAG_NAME, "td")
        if not celdas:
            continue
        texto = [col.text.strip() for col in celdas]
        print("\t".join(texto))
