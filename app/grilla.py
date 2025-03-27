from bs4 import BeautifulSoup

GRILLA_URL = "https://ipssalta.gob.ar/SeguroEscolar/Seguro/GesPlanillaAdministrar.aspx"

def mostrar_grilla(session):
    print("[*] Accediendo a la tabla de planillas con deuda...")
    resp = session.get(GRILLA_URL, verify=False)
    soup = BeautifulSoup(resp.text, "html.parser")

    tabla = soup.find("table", id="tblPlanilla")

    if not tabla:
        print("[-] No se encontró la tabla de deuda con ID tblPlanilla")
        return

    encabezados = [th.get_text(strip=True) for th in tabla.find("thead").find_all("th")]
    filas = []

    for fila_html in tabla.find("tbody").find_all("tr"):
        columnas = [td.get_text(strip=True) for td in fila_html.find_all("td")]
        if columnas:
            filas.append(columnas)

    if not filas:
        print("[!] La tabla de deuda fue encontrada pero está vacía.")
        return

    print("\t".join(encabezados))
    print("-" * 100)
    for fila in filas:
        print("\t".join(fila))
