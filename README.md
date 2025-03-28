🤖 IPS Seguro Escolar Bot
Automatización de carga y gestión de planillas para el sistema IPS Seguro Escolar del Instituto Provincial de Salud de Salta. Este bot permite listar planillas, abrir una específica, cargar alumnos manualmente por DNI o de forma masiva desde archivos Excel.

📦 Características
✅ Login automático

✅ Listado de planillas disponibles

✅ Apertura de planilla por número

✅ Búsqueda de alumno por DNI

✅ Carga automática de alumnos desde archivo Excel

✅ Registro de errores con alumnos que no pudieron ser cargados

✅ Manejo de ventanas emergentes tipo SweetAlert

⚙️ Requisitos
Python 3.10+

Google Chrome instalado

chromedriver compatible (instalado automáticamente)

Paquetes instalados con pip (ver sección instalación)

🚀 Instalación
git clone https://github.com/22xam/ips-seguro-escolar-bot.git
cd ips-seguro-escolar-bot
python -m venv venv
venv\Scripts\activate # en Windows
pip install -r requirements.txt
🔐 Configuración
Crear un archivo .env en la raíz del proyecto con tus credenciales:

IPS_USERNAME= usuario
IPS_PASSWORD= 123456

⚠️ No uses comillas ni espacios. El archivo .env ya está en .gitignore para evitar que se suba a GitHub.

🧠 Modo de uso
📜 Menú interactivo
Ejecutá el bot con:

css
Copiar
Editar
python main.py
Menú:

css
Copiar
Editar
[1] Listar planillas
[2] Entrar a una planilla por Nº
[3] Cargar planilla automáticamente desde Excel
[0] Salir
📚 Estructura del archivo Excel para carga automática
Colocá el archivo Excel en la carpeta /data

El nombre del archivo (sin extensión) será usado como nombre del curso

El archivo debe tener al menos 4 columnas:

Columna Contenido Obligatorio
A (ignorada por el script) ❌ No
B Apellido y Nombre del alumno ✅ Sí
C DNI del alumno (solo números) ✅ Sí
D Índice del Importe (0 o 1) ✅ Sí
📌 Ejemplo:

A B C D
1 (vacío) Juan Pérez 30111222 0
2 (vacío) María López 29100888 1
3 (vacío) Ricardo González 27333444 0
🪵 Logs de errores
Los alumnos que no puedan ser cargados correctamente se registran automáticamente en:

bash
Copiar
Editar
/data/log_no_cargados.txt
📁 Estructura del proyecto
bash
Copiar
Editar
.
├── app/
│ ├── core/
│ │ ├── login.py
│ │ ├── driver_factory.py
│ │ ├── tabla_planillas.py
│ │ ├── navegar_planilla.py
│ │ └── cargar_desde_excel.py
├── data/
│ └── (archivos Excel)
├── .env
├── main.py
└── README.md
✨ Contribuciones
Este proyecto fue creado para facilitar la carga de planillas en entornos escolares. Pull requests y sugerencias son bienvenidas.

🧠 Autor
@22xam
Desarrollado con ❤ para automatizar tareas del IPS Seguro Escolar.
