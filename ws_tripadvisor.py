from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException


def get_section_classes(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # descomenta si no quieres ver el navegador

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(url)

    try:
        # Esperar hasta que el contenedor principal esté visible
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.XmUgu._T.Ft[data-part='ListSections']"))
        )

        container = driver.find_element(By.CSS_SELECTOR, "div.XmUgu._T.Ft[data-part='ListSections']")
        sections = container.find_elements(By.TAG_NAME, "section")

        print(f"🧱 Se encontraron {len(sections)} secciones dentro del contenedor")

        for idx, section in enumerate(sections, start=1):
            class_attr = section.get_attribute("class")
            data_automation = section.get_attribute("data-automation")
            print(f"\n🔹 Sección {idx}:")
            print(f"   → class = {class_attr}")
            print(f"   → data-automation = {data_automation}")

    except TimeoutException:
        print("⏰ No se encontró el contenedor principal en el tiempo esperado")

    finally:
        driver.quit()


if __name__ == "__main__":
    url = "https://www.tripadvisor.co/Attractions-g297478-Activities-oa60-Medellin_Antioquia_Department.html"
    get_section_classes(url)
