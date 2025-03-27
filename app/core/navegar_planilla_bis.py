from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PLANILLAS_URL = "https://ipssalta.gob.ar/SeguroEscolar/Seguro/GesPlanillaAdministrar.aspx"

def abrir_planilla(driver, numero_planilla: str):
    print(f"[*] Accediendo a: {PLANILLAS_URL}")
    driver.get(PLANILLAS_URL)
    time.sleep(5)

    # Buscar planilla por número
    tabla = driver.find_element(By.ID, "tblPlanilla")
    filas = tabla.find_elements(By.TAG_NAME, "tr")

    for fila in filas:
        celdas = fila.find_elements(By.TAG_NAME, "td")
        if celdas and celdas[0].text.strip() == numero_planilla:
            print(f"[✔] Planilla Nº {numero_planilla} encontrada. Seleccionando...")
            fila.click()
            break
    else:
        print(f"[✘] Planilla Nº {numero_planilla} no encontrada.")
        return

    # Click en botón "Completar"
    time.sleep(1)
    driver.find_element(By.ID, "btnPlanillaDetalle").click()
    time.sleep(5)

    print("[✔] Planilla abierta correctamente.")
    print("📄 URL actual:", driver.current_url)

    # Loop de búsqueda por DNI
    while True:
        dni = input(">> Ingrese Nro. de Documento del alumno: ").strip()
        if not dni.isdigit():
            print("❌ DNI inválido.")
            continue

        input_doc = driver.find_element(By.ID, "txtNroDoc")
        input_doc.clear()
        input_doc.send_keys(dni)
        input_doc.send_keys(Keys.TAB)

        # Esperar carga automática
        try:
            WebDriverWait(driver, 10).until(
                lambda d: d.find_element(By.ID, "txtNombre").get_attribute("value").strip() != ""
            )
        except:
            print("❌ No se cargaron los datos del alumno.")
            continue

        nombre = driver.find_element(By.ID, "txtNombre").get_attribute("value").strip()
        fecha_nac = driver.find_element(By.ID, "txtFechaNac").get_attribute("value").strip()

        print("\n📄 DATOS DEL ALUMNO:")
        print(f"🧑 Nombre: {nombre}")
        print(f"🎂 Fecha de Nacimiento: {fecha_nac}")

        otra = input("\n¿Buscar otro alumno? (s/n): ").strip().lower()
        if otra != "s":
            break
