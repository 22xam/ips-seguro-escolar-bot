from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import time

PLANILLAS_URL = "https://ipssalta.gob.ar/SeguroEscolar/Seguro/GesPlanillaAdministrar.aspx"

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
        return

    time.sleep(1)
    cerrar_sweetalert_si_abierta(driver)

    driver.find_element(By.ID, "btnPlanillaDetalle").click()
    time.sleep(5)
    print("[✔] Planilla abierta correctamente.")
    print("📄 URL actual:", driver.current_url)

    while True:
        cerrar_sweetalert_si_abierta(driver)

        dni = input(">> Ingrese Nro. de Documento del alumno: ").strip()
        if not dni.isdigit():
            print("❌ DNI inválido.")
            continue

        input_doc = driver.find_element(By.ID, "txtNroDoc")
        input_doc.clear()
        input_doc.send_keys(dni)
        input_doc.send_keys(Keys.TAB)

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

        # 🏫 Solicitar curso
        curso = input(">> Ingrese curso del alumno: ").strip()
        input_curso = driver.find_element(By.ID, "txtCurso")
        input_curso.clear()
        input_curso.send_keys(curso)

        # 💰 Selección de importe
        select_importe = driver.find_element(By.ID, "ddlImporte")
        opciones = select_importe.find_elements(By.TAG_NAME, "option")
        print("\n💰 Opciones de Importe:")
        for idx, opcion in enumerate(opciones):
            print(f"[{idx}] {opcion.text.strip()}")

        while True:
            index = input(">> Seleccione el número de opción de Importe: ").strip()
            if index.isdigit() and 0 <= int(index) < len(opciones):
                opciones[int(index)].click()
                break
            print("❌ Selección inválida.")

        # ✅ Confirmar si desea agregar
        confirmar = input("\n¿Desea agregar este alumno a la planilla? (s/n): ").strip().lower()
        if confirmar == "s":
            try:
                driver.find_element(By.ID, "btnAgregarFila").click()
                print("✅ Alumno agregado.")
                time.sleep(2)
                cerrar_sweetalert_si_abierta(driver)
            except Exception as e:
                print(f"❌ Error al hacer clic en agregar: {e}")
        else:
            print("⏭ Alumno no agregado.")

        otra = input("\n¿Desea buscar otro alumno? (s/n): ").strip().lower()
        if otra != "s":
            break
