import undetected_chromedriver as uc
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import json
import re
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = uc.Chrome(options=chrome_options, use_subprocess=True)

COOKIES_PATH = "uber_cookies.json"


def load_cookies_if_available(driver, cookies_path):
    if not os.path.exists(cookies_path):
        return False
    try:
        with open(cookies_path, "r", encoding="utf-8") as f:
            cookies = json.load(f)
        # Abrir domínio base para permitir setar cookies
        driver.get("https://drivers.uber.com")
        for cookie in cookies:
            # Selenium aceita chaves padrão; remover inválidas se presentes
            cookie = {k: v for k, v in cookie.items() if k in {"name", "value", "domain", "path", "expiry", "secure", "httpOnly", "sameSite"}}
            try:
                driver.add_cookie(cookie)
            except Exception:
                # Ignora cookies problemáticos
                pass
        return True
    except Exception:
        return False


def save_cookies(driver, cookies_path):
    try:
        cookies = driver.get_cookies()
        with open(cookies_path, "w", encoding="utf-8") as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

print("Navegando para o dominio de autenticação...")

# Tenta reutilizar sessão via cookies
cookies_loaded = load_cookies_if_available(driver, COOKIES_PATH)

# Vai para a página de atividades
driver.get("https://drivers.uber.com/earnings/activities")

# Se cookies funcionaram, deve encontrar o elemento de ganhos sem login manual
logged_in = False
try:
    wait = WebDriverWait(driver, 20)
    wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Ganhos da Uber')]")))
    print("Sessão reutilizada! A página de ganhos foi encontrada.")
    logged_in = True
except Exception:
    pass

if not logged_in:
    print("Faça o login manual no navegador.")
    time.sleep(120)

    try:
        wait = WebDriverWait(driver, 30)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Ganhos da Uber')]")))
        print("Login bem-sucedido! A página de ganhos foi encontrada.")
        # Salva cookies para próximas execuções
        save_cookies(driver, COOKIES_PATH)
    except:
        print("Erro: O login não foi concluído dentro do tempo esperado.")

all_trips_data = []
main_window_handle = driver.current_window_handle
wait = WebDriverWait(driver, 10)

dias_para_puxar = ['8', '12', '18', '25']

for dia in dias_para_puxar:
    print(f"\n--- Iniciando a extração para o dia {dia} ---")
    
    print("Clicando no campo de seleção de data...")
    date_range_input = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='YYYY/MM/DD – YYYY/MM/DD']"))
    )
    date_range_input.click()

    print(f"Aguardando o calendário e clicando no dia {dia}...")
    wait.until(
        EC.visibility_of_element_located((By.XPATH, f"//div[text()='{dia}']"))
    )
    
    day_to_click = driver.find_element(By.XPATH, f"//div[text()='{dia}']")
    day_to_click.click()

    print("Aguardando a página recarregar com os dados da semana...")
    time.sleep(5)

    print("Pressionando ESC para fechar o calendário...")
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
    time.sleep(5)

    print("Rolando a página até o fim para carregar todos os dados...")
    while True:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            load_more_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Carregar mais')]")
            print("Botão 'Carregar mais' encontrado. Clicando...")
            load_more_button.click()
            time.sleep(2)
        except NoSuchElementException:
            print("Botão 'Carregar mais' não encontrado. Todos os resultados foram carregados.")
            break

    print("Todos os resultados foram carregados.")
    time.sleep(5)

    print("Subindo para o topo da página...")
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)

    view_details_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'View Details')]")

    for i in range(len(view_details_buttons)):
        print(f"Extraindo dados da corrida {i+1} de {len(view_details_buttons)}...")

        try:
            driver.execute_script("arguments[0].scrollIntoView();", view_details_buttons[i])
            time.sleep(1)
            view_details_buttons[i].click()

            wait.until(EC.number_of_windows_to_be(2))
            for window_handle in driver.window_handles:
                if window_handle != main_window_handle:
                    driver.switch_to.window(window_handle)
                    break

            dados_corrida = {}

            ganhos_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'R$')]")))
            ganhos_text = ganhos_element.text
            ganhos_valor = re.sub(r'R\$\s*', '', ganhos_text).replace(',', '.')
            dados_corrida["Ganhos"] = float(ganhos_valor)

            detalhes_element = driver.find_element(By.XPATH, "//p[contains(@class, 'gQdIWP') and contains(@class, 'chTMGz')]")
            detalhes_text = detalhes_element.text
            partes = detalhes_text.split(" • ")
            dados_corrida["Tipo de Corrida"] = partes[0]
            dados_corrida["Data"] = partes[1]
            dados_corrida["Hora"] = partes[2]

            mapa_element = driver.find_element(By.TAG_NAME, "img")
            mapa_url = mapa_element.get_attribute("src")
            dados_corrida["URL do Mapa"] = mapa_url

            infos = driver.find_elements(By.XPATH, "//div[contains(@class, 'cFyYHT')]")
            if len(infos) >= 2:
                dados_corrida["Duracao"] = infos[0].text
                dados_corrida["Distancia"] = infos[1].text
            else:
                dados_corrida["Duracao"] = None
                dados_corrida["Distancia"] = None

            enderecos = driver.find_elements(By.XPATH, "//p[contains(@class, 'eXlLWF')]")
            if len(enderecos) >= 2:
                dados_corrida["Endereco_Coleta"] = enderecos[0].text
                dados_corrida["Endereco_Destino"] = enderecos[1].text
            else:
                dados_corrida["Endereco_Coleta"] = None
                dados_corrida["Endereco_Destino"] = None

            pontos_element = driver.find_element(By.XPATH, "//p[contains(text(), 'Pontos ganhos:')]")
            dados_corrida["Pontos_Ganhos"] = pontos_element.text

            valores = driver.find_elements(By.XPATH, "//p[contains(@class, 'fMjedc') and contains(@class, 'dTqljZ')]")
            if len(valores) >= 3:
                dados_corrida["Valor_Total_Passageiro"] = valores[0].text
                dados_corrida["Descontos"] = valores[1].text
                dados_corrida["Meus_Ganhos"] = valores[2].text
            
            uber_ganhos = driver.find_element(By.XPATH, "//p[contains(@class, 'fMrAHl') and contains(@class, 'dTqljZ')]")
            dados_corrida["Ganhos_Uber"] = uber_ganhos.text

            all_trips_data.append(dados_corrida)
            print("Dados extraídos:", dados_corrida)

        except Exception as e:
            print(f"Erro ao extrair dados da corrida {i+1}: {e}")

        finally:
            driver.close()
            driver.switch_to.window(main_window_handle)
    
    # Linha removida: driver.get("https://drivers.uber.com/earnings/activities")
    
with open("uber_activities.json", "w", encoding="utf-8") as f:
    json.dump(all_trips_data, f, ensure_ascii=False, indent=4)

print("\nTodos os dados de todos os dias foram extraídos e salvos em 'uber_activities.json'.")
time.sleep(10)
driver.quit()