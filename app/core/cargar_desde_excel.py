from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import time
import os
import pandas as pd

PLANILLAS_URL = "https://ipssalta.gob.ar/SeguroEscolar/Seguro/GesPlanillaAdministrar.aspx"
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
LOG_PATH = os.path.join(DATA_DIR, "log_no_cargados.txt")

os.makedirs(DATA_DIR, exist_ok=True)

def cerrar_sweetalert_si_abierta(driver):
    try:
        alert = WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "sweet-alert"))
        )
        print("[!] SweetAlert detectada. Cerrando...")
        alert.find_element(By.CLASS_NAME, "confirm").click()
        time.sleep(1)
    except:
        pass

def abrir_planilla(driver, numero_planilla: str):
    print(f"[*] Accediendo a: {PLANILLAS_URL}")
    driver.get(PLANILLAS_URL)
    time.sleep(5)
    cerrar_sweetalert_si_abierta(driver)

    tabla = driver.find_element(By.ID, "tblPlanilla")
    filas = tabla.find_elements(By.TAG_NAME, "tr")

    for fila in filas:
        celdas = fila.find_elements(By.TAG_NAME, "td")
        if celdas and celdas[0].text.strip() == numero_planilla:
            print(f"[✔] Planilla Nº {numero_planilla} encontrada. Seleccionando...")
            try:
                fila.click()
            except ElementClickInterceptedException:
                print("[!] Clic interceptado. Ejecutando clic vía JavaScript...")
                driver.execute_script("arguments[0].click();", fila)
            break
    else:
        print(f"[✘] Planilla Nº {numero_planilla} no encontrada.")
        return False

    time.sleep(1)
    cerrar_sweetalert_si_abierta(driver)

    driver.find_element(By.ID, "btnPlanillaDetalle").click()
    time.sleep(5)
    print("[✔] Planilla abierta correctamente.")
    print("📄 URL actual:", driver.current_url)
    return True

def cargar_planilla_automatica(driver, numero_planilla: str):
    if not abrir_planilla(driver, numero_planilla):
        return

    archivos_excel = [f for f in os.listdir(DATA_DIR) if f.endswith(".xlsx")]
    if not archivos_excel:
        print("❌ No se encontraron archivos Excel en /data")
        return

    dni_fallidos = []

    for archivo in archivos_excel:
        path = os.path.join(DATA_DIR, archivo)
        curso_nombre = os.path.splitext(archivo)[0]
        print(f"\n[*] Procesando archivo: {archivo} | Curso: {curso_nombre}")

        try:
            df = pd.read_excel(path)
        except Exception as e:
            print(f"❌ Error al abrir {archivo}: {e}")
            continue

        df.columns = [col.strip().lower() for col in df.columns]

        for index, row in df.iterrows():
            try:
                nombre_excel = str(row.get("apellido y nombre") or row.iloc[1]).strip()
                dni = str(row.get("dni") or row.iloc[2]).split(".")[0].strip()
                importe_index = int(row.get("importe") or row.iloc[3])

                cerrar_sweetalert_si_abierta(driver)

                input_doc = driver.find_element(By.ID, "txtNroDoc")
                input_doc.clear()
                input_doc.send_keys(dni)
                input_doc.send_keys(Keys.TAB)

                WebDriverWait(driver, 8).until(
                    lambda d: d.find_element(By.ID, "txtNombre").get_attribute("value").strip() != ""
                )

                nombre_sistema = driver.find_element(By.ID, "txtNombre").get_attribute("value").strip()
                fecha_nac = driver.find_element(By.ID, "txtFechaNac").get_attribute("value").strip()

                print(f"👤 Excel: {nombre_excel} | DNI: {dni}")
                print(f"✅ Sistema: {nombre_sistema} | 🎂 {fecha_nac}")

                input_curso = driver.find_element(By.ID, "txtCurso")
                input_curso.clear()
                input_curso.send_keys(curso_nombre)

                select_importe = driver.find_element(By.ID, "ddlImporte")
                opciones = select_importe.find_elements(By.TAG_NAME, "option")
                if 0 <= importe_index < len(opciones):
                    opciones[importe_index].click()
                else:
                    print("⚠ Importe inválido, usando primera opción.")
                    opciones[0].click()

                driver.find_element(By.ID, "btnAgregarFila").click()
                time.sleep(5)
                cerrar_sweetalert_si_abierta(driver)

            except Exception as e:
                dni_fallidos.append({
                    "DNI": dni if 'dni' in locals() else '???',
                    "Curso": curso_nombre,
                    "Archivo": archivo,
                    "Error": str(e)
                })
                print(f"❌ Error al cargar {nombre_excel if 'nombre_excel' in locals() else '[Sin Nombre]'} (DNI: {dni if 'dni' in locals() else '???'}): {e}")

    if dni_fallidos:
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            for entry in dni_fallidos:
                f.write(f"{entry['DNI']} - {entry['Curso']} - {entry['Archivo']} - {entry['Error']}\n")
        print(f"\n[!] Log guardado en: {LOG_PATH}")

    print("\n✅ Carga automática finalizada.")
    input("Presiona ENTER para volver al menú...")
