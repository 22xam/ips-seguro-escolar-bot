import requests
from bs4 import BeautifulSoup
from app.config import LOGIN_URL, USERNAME, PASSWORD

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def login_to_portal():
    session = requests.Session()

    try:
        response = session.get(LOGIN_URL, verify=False)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[-] Error accediendo al login: {e}")
        return None

    with open("output/debug_login_page.html", "w", encoding="utf-8") as f:
        f.write(response.text)

    soup = BeautifulSoup(response.text, "html.parser")
    form = soup.find("form")

    if not form:
        print("[-] No se encontró el formulario principal.")
        return None

    # Extraer todos los campos del form
    payload = {}
    for input_tag in form.find_all("input"):
        name = input_tag.get("name")
        value = input_tag.get("value", "")
        if name:
            payload[name] = value

    # Actualizar campos críticos de login
    payload["txtUserName"] = USERNAME
    payload["txtPassword"] = PASSWORD
    payload["btnLogin"] = "Iniciar Sesión"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        login_response = session.post(LOGIN_URL, data=payload, headers=headers, verify=False)
        login_response.raise_for_status()
    except requests.RequestException as e:
        print(f"[-] Error durante el POST de login: {e}")
        return None

    with open("output/post_login.html", "w", encoding="utf-8") as f:
        f.write(login_response.text)

    if "cerrar sesión" in login_response.text.lower() or "cerrar sesion" in login_response.text.lower():
        print("[+] Login exitoso.")
        return session
    else:
        print("[-] Falló el login. Verifica tus credenciales.")
        return None

