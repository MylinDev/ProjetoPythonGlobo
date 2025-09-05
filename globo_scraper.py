import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Função para buscar notícias no G1/Globo usando Selenium , mas pode usar outra fonte se quiser, qualquer dúvida entre em contato pelo meu github.
def get_noticias_globo_selenium(driver, limite, SEARCH_URL_BASE):
    noticias = []
    url = SEARCH_URL_BASE
    pagina = 1
    data_hoje = datetime.now().strftime('%d/%m/%Y')
    def contem_data_hoje(texto):
        texto = texto.lower()
        if data_hoje in texto:
            return True
        if 'há ' in texto and ('hora' in texto or 'minuto' in texto):
            return True
        return False
    while len(noticias) < limite and url:
        print(f"[DEBUG] Acessando página de busca {pagina}...")
        driver.get(url)
        time.sleep(3)
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".widget--info"))
            )
        except Exception as e:
            print(f"[DEBUG] Nenhuma notícia encontrada nesta página. Erro: {e}")
            break
        cards = driver.find_elements(By.CSS_SELECTOR, ".widget--info")
        encontrou_noticia_do_dia_pagina = False
        # Verifica se há notícias do dia na página atual.
        for card in cards:
            try:
                titulo_elem = card.find_element(By.CSS_SELECTOR, ".widget--info__title")
                resumo_elem = card.find_element(By.CSS_SELECTOR, ".widget--info__description")
                link_elem = card.find_element(By.CSS_SELECTOR, "a")
                data_elem = card.find_element(By.CSS_SELECTOR, ".widget--info__meta") if card.find_elements(By.CSS_SELECTOR, ".widget--info__meta") else None
                titulo = titulo_elem.text.strip()
                resumo = resumo_elem.text.strip() if resumo_elem else ""
                link = link_elem.get_attribute("href")
                data_pub = data_elem.text.strip() if data_elem else ""
                print(f"[DEBUG] Data encontrada: '{data_pub}' para notícia: {titulo}")
                if titulo and link and contem_data_hoje(data_pub):
                    noticias.append({
                        "titulo": titulo,
                        "resumo": resumo,
                        "link": link,
                        "data_pub": data_pub
                    })
                    encontrou_noticia_do_dia_pagina = True
            except Exception as e:
                continue
            if len(noticias) >= limite:
                break
        if not encontrou_noticia_do_dia_pagina:
            print("[DEBUG] Nenhuma notícia do dia encontrada nesta página. Encerrando busca.")
            break
        print(f"[DEBUG] {len(noticias)} notícias extraídas até agora.")
        if len(noticias) >= limite:
            break
        next_page_found = False
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, ".load-more__button")
            if next_button.is_enabled() and "disabled" not in next_button.get_attribute("class"):
                print("[DEBUG] Clicando no botão 'Ver mais'...")
                driver.execute_script("arguments[0].click();", next_button)
                pagina += 1
                time.sleep(5)
                next_page_found = True
        except Exception as e:
            print(f"[DEBUG] Botão 'Ver mais' não encontrado ou erro: {str(e).splitlines()[0]}")
        if not next_page_found:
            pagina += 1
            url = f"{SEARCH_URL_BASE}&page={pagina}"
            print(f"[DEBUG] Tentando acessar manualmente a página {pagina} via URL: {url}")
            time.sleep(2)
            driver.get(url)
            time.sleep(2)
            cards_test = driver.find_elements(By.CSS_SELECTOR, ".widget--info")
            if not cards_test:
                print("[DEBUG] Não há mais notícias nas próximas páginas.")
                break
        else:
            url = driver.current_url
    print(f"[DEBUG] {len(noticias)} notícias extraídas no total.")
    return noticias[:limite]
