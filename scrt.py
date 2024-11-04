import requests
import pandas as pd

# Base URL de la API
base_url = "https://api.transparencia.gob.do/api/nominas"

# Definimos los parámetros de consulta (ajusta según sea necesario)
params = {
    "periodo": "20240601",  # Cambia esto al periodo que deseas
    "nombres": "",
    "apellidos": "",
    "institucion": "",
    "cargo": "",
    "lugar": "",
    "genero": "",
    "estatus": "",
}

# Inicializa una lista para almacenar todos los datos
all_data = []

# Realiza la solicitud a la primera página para obtener el total de páginas
page = 1
while True:
    params["page"] = page  # Establece el número de página

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()  # Suponiendo que la respuesta es JSON
        all_data.extend(data.get('data', []))  # Agrega los datos de la página actual

        # Verifica si hay más páginas
        if page >= data.get('meta', {}).get('last_page', 0):
            break  # Sal del bucle si no hay más páginas

        page += 1  # Incrementa el número de página para la próxima solicitud
    else:
        print("Error al hacer la solicitud a la API:", response.status_code)
        break

# Procesa los datos y conviértelos en un DataFrame
nombres = []
apellidos = []
instituciones = []
funciones = []
areas = []
generos = []
estatuses = []
sueldos_brutos = []

for item in all_data:
    nombres.append(item['NOMBRES'])
    apellidos.append(item['APELLIDOS'])
    instituciones.append(item['INSTITUCION'])
    funciones.append(item['CARGO'])
    areas.append(item['LUGAR_FUNCIONES'])
    generos.append(item['GENERO'])
    estatuses.append(item['TIPO_EMPLEADO'])
    sueldos_brutos.append(item['SUELDO_BRUTO_FIJOS'])

# Crea un DataFrame y guarda los datos en un archivo CSV
df = pd.DataFrame({
    'Nombres': nombres,
    'Apellidos': apellidos,
    'Institución': instituciones,
    'Función': funciones,
    'Área': areas,
    'Género': generos,
    'Estatus': estatuses,
    'Sueldo bruto': sueldos_brutos
})
df.to_csv('nomina.csv', index=False, encoding='utf-8')

print("Datos extraídos y guardados en 'nomina.csv'.")
