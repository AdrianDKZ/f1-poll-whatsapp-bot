from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import time

# Configurar el WebDriver de Firefox automáticamente usando webdriver_manager
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

# Abrir la página web
url = "https://f1calendar.com/es"
driver.get(url)

# Esperar unos segundos para que el contenido se cargue (ajustar según sea necesario)
time.sleep(5)  # Puedes aumentar el tiempo de espera si la página tarda más en cargar

# Obtener el HTML de la página después de que todo el contenido se haya cargado
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Encontrar la tabla que contiene los eventos de las carreras
table = soup.find('table', class_='events-table')

# Encontrar todos los tbody dentro de la tabla
tbody = table.find_all('tbody')

# Iterar sobre los tbody y extraer los horarios de todas las sesiones
for body in tbody:
    rows = body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')

        if len(cols) >= 3:
            # Extraer el nombre de la carrera
            race_name = row.find('th').find('span').get_text(strip=True)

            # Extraer la fecha
            date = cols[0].find('span').get_text(strip=True)

            # Extraer los horarios de las sesiones
            session_info = cols[2].find_all('span')

            for session in session_info:
                session_time = session.get_text(strip=True)
                print(f"Carrera: {race_name}")
                print(f"Fecha: {date}")
                print(f"Horario de la sesión: {session_time}")
                print('-' * 30)

# Cerrar el navegador
driver.quit()
