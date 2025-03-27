from app.core.driver_factory import get_driver
from app.core.login import login
from app.core.tabla_planillas import mostrar_planillas
from app.core.navegar_planilla import abrir_planilla
from app.core.cargar_desde_excel import cargar_planilla_automatica

def menu():
    print("""
    ========== IPS Seguro Escolar ==========
    [1] Listar planillas
    [2] Entrar a una planilla por Nº
    [3] Carga automática desde Excel
    [0] Salir
    """)

def main():
    driver = get_driver()
    login(driver)

    while True:
        menu()
        opcion = input(">> Seleccione opción: ").strip()

        if opcion == "1":
            mostrar_planillas(driver)
        elif opcion == "2":
            numero = input(">> Ingrese N° de Planilla: ").strip()
            abrir_planilla(driver, numero)
        elif opcion == "3":
            numero = input(">> Ingrese N° de Planilla para carga automática: ").strip()
            cargar_planilla_automatica(driver, numero)
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida.")

    driver.quit()
    print("[*] Fin del proceso.")

if __name__ == "__main__":
    main()
