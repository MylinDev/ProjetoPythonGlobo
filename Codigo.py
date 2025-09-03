import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime


# Busca notícias sobre vagas de emprego no G1/Globo
SEARCH_URL_BASE = "https://g1.globo.com/busca/?q=vaga+de+emprego"
LIMITE = 20


def get_noticias_globo_selenium(driver, limite):
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    from datetime import datetime
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
                # Só adiciona se a data for igual a de hoje ou for 'há X horas/minutos'
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
        # Tenta ir para a próxima página pelo botão, senão tenta por URL
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
            print(f"[DEBUG] Botão 'Ver mais' não encontrado ou erro: {e}")

        if not next_page_found:
            # Tenta acessar próxima página manualmente pelo parâmetro page=
            pagina += 1
            url = f"{SEARCH_URL_BASE}&page={pagina}"
            print(f"[DEBUG] Tentando acessar manualmente a página {pagina} via URL: {url}")
            time.sleep(2)
            # Se não houver mais notícias, a próxima página não terá cards
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




def main():
    print("Obtendo notícias sobre vagas de emprego com Selenium...")
    options = Options()
    options.headless = True
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    try:
        from reportlab.lib.utils import simpleSplit
        import os
        import re
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        import os
        # Registra fontes Roboto se disponíveis
        font_dir = os.getcwd()
        roboto_regular = os.path.join(font_dir, "Roboto-Regular.ttf")
        roboto_bold = os.path.join(font_dir, "Roboto-Bold.ttf")
        if os.path.exists(roboto_regular):
            pdfmetrics.registerFont(TTFont("Roboto", roboto_regular))
        if os.path.exists(roboto_bold):
            pdfmetrics.registerFont(TTFont("Roboto-Bold", roboto_bold))

        noticias = get_noticias_globo_selenium(driver, LIMITE)
        # Listas de estados e áreas para busca
        estados = [
            'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO',
            'Acre', 'Alagoas', 'Amapá', 'Amazonas', 'Bahia', 'Ceará', 'Distrito Federal', 'Espírito Santo', 'Goiás', 'Maranhão', 'Mato Grosso', 'Mato Grosso do Sul', 
            'Minas Gerais', 'Pará', 'Paraíba', 'Paraná', 'Pernambuco', 'Piauí', 'Rio de Janeiro', 'Rio Grande do Norte', 'Rio Grande do Sul', 'Rondônia', 'Roraima',
            'Santa Catarina', 'São Paulo', 'Sergipe', 'Tocantins'
        ]
        areas = [
            ('tecnologia', ['tecnologia', 'TI', 'informática', 'desenvolvedor', 'programador', 'software', 'dados', 'analista']),
            ('saúde', ['saúde', 'enfermeiro', 'médico', 'hospital', 'clínica', 'enfermagem', 'farmácia', 'biomédico']),
            ('educação', ['professor', 'educação', 'escola', 'universidade', 'docente', 'pedagogo']),
            ('administração', ['administração', 'administrativo', 'secretária', 'gestão', 'assistente administrativo']),
            ('comercial', ['vendas', 'comercial', 'representante', 'vendedor', 'atendimento']),
            ('engenharia', ['engenheiro', 'engenharia', 'civil', 'mecânico', 'elétrico', 'produção']),
            ('outras', [])
        ]
        from datetime import datetime
        def extrair_estado(texto):
            for estado in estados:
                if re.search(rf'\b{re.escape(estado)}\b', texto, re.IGNORECASE):
                    return estado
            return 'Desconhecido'
        def extrair_area(texto):
            for area, palavras in areas:
                for palavra in palavras:
                    if re.search(rf'\b{re.escape(palavra)}\b', texto, re.IGNORECASE):
                        return area.capitalize()
            return 'Outras'

        for idx, noticia in enumerate(noticias, start=1):
            print(f"Processando notícia {idx}/{len(noticias)}: {noticia['titulo']}")
            texto_busca = f"{noticia['titulo']} {noticia['resumo']}"
            estado = extrair_estado(texto_busca)
            area = extrair_area(texto_busca)
            data_pub_raw = noticia.get('data_pub', datetime.now().strftime('%d/%m/%Y'))
            # Se vier 'há X horas' ou 'há X minutos', usa a data de hoje
            if 'há' in data_pub_raw and ('hora' in data_pub_raw or 'minuto' in data_pub_raw):
                data_pub = datetime.now().strftime('%d/%m/%Y')
            else:
                data_pub = data_pub_raw
            # Acessa o link da notícia e extrair o texto principal
            noticia_completa = noticia["resumo"]
            try:
                driver.get(noticia["link"])
                time.sleep(2)
                # Tenta pegar todos os parágrafos principais
                paragrafos = driver.find_elements(By.CSS_SELECTOR, "p.content-text__container")
                if paragrafos:
                    noticia_completa = "\n\n".join([p.text for p in paragrafos if p.text.strip()])
            except Exception as e:
                print(f"[DEBUG] Erro ao extrair texto completo da notícia: {e}")
            pdf_filename = f"vaga_{estado}_{area}_{data_pub.replace('/', '-')}_{idx}.pdf".replace(' ', '_')
            pdf_path = os.path.join(os.getcwd(), pdf_filename)
            c = canvas.Canvas(pdf_path, pagesize=A4)
            width, height = A4
            c.setFillColorRGB(1, 1, 1)
            c.rect(0, 0, width, height, fill=1, stroke=0)
            c.setFillColorRGB(196/255, 23/255, 12/255)
            faixa_altura = 25 * mm
            c.rect(0, height - faixa_altura, width, faixa_altura, fill=1, stroke=0)
            if "Roboto-Bold" in pdfmetrics.getRegisteredFontNames():
                c.setFont("Roboto-Bold", 16)
            else:
                c.setFont("Helvetica-Bold", 16)
            c.setFillColorRGB(1, 1, 1)
            c.drawString(20 * mm, height - 18 * mm, "Vaga de Emprego")
            if "Roboto" in pdfmetrics.getRegisteredFontNames():
                c.setFont("Roboto", 11)
            else:
                c.setFont("Helvetica", 11)
            c.setFillColorRGB(0, 0, 0)
            y = height - faixa_altura - 10 * mm
            c.drawString(20 * mm, y, f"Data de publicação: {data_pub}")
            if "Roboto" in pdfmetrics.getRegisteredFontNames():
                c.setFont("Roboto", 10)
            else:
                c.setFont("Helvetica-Oblique", 10)
            link = noticia["link"]
            y -= 8 * mm
            link_text = "Clique aqui para acessar a notícia"
            c.setFillColorRGB(0, 0, 1)  # azul
            c.drawString(20 * mm, y, link_text)
            link_width = c.stringWidth(link_text, "Helvetica-Oblique", 10)
            c.linkURL(link, (20 * mm, y, 20 * mm + link_width, y + 10 * mm), relative=0)
            c.setFillColorRGB(0, 0, 0)  # volta ao preto
            # Título com quebra de linha e negrito, sem corte
            from reportlab.pdfbase.pdfmetrics import stringWidth
            if "Roboto-Bold" in pdfmetrics.getRegisteredFontNames():
                c.setFont("Roboto-Bold", 12)
            else:
                c.setFont("Helvetica-Bold", 12)
            titulo_label = "Título: "
            # Título completo: tenta pegar do <h1> da notícia
            titulo = noticia['titulo']
            try:
                driver.get(noticia["link"])
                time.sleep(2)
                h1s = driver.find_elements(By.TAG_NAME, "h1")
                if h1s and h1s[0].text.strip():
                    titulo = h1s[0].text.strip()
                # Tenta pegar todos os parágrafos principais
                paragrafos = driver.find_elements(By.CSS_SELECTOR, "p.content-text__container")
                if paragrafos:
                    noticia_completa = "\n\n".join([p.text for p in paragrafos if p.text.strip()])
            except Exception as e:
                print(f"[DEBUG] Erro ao extrair texto completo da notícia: {e}")
            y -= 12 * mm
            max_width = width - 40 * mm
            def split_lines(text, font, font_size, max_width):
                words = text.split()
                lines = []
                current = ''
                for word in words:
                    test = (current + ' ' + word).strip()
                    if stringWidth(test, font, font_size) <= max_width:
                        current = test
                    else:
                        if current:
                            lines.append(current)
                        current = word
                if current:
                    lines.append(current)
                return lines
            font_title = "Roboto-Bold" if "Roboto-Bold" in pdfmetrics.getRegisteredFontNames() else "Helvetica-Bold"
            font_text = "Roboto" if "Roboto" in pdfmetrics.getRegisteredFontNames() else "Helvetica"
            titulo_full = titulo_label + titulo
            titulo_lines = split_lines(titulo_full, font_title, 12, max_width)
            for line in titulo_lines:
                if y < 30 * mm:
                    c.showPage()
                    c.setFont(font_title, 12)
                    y = height - 20 * mm
                c.drawString(20 * mm, y, line)
                y -= 7 * mm
            c.setFont(font_text, 11)
            c.drawString(20 * mm, y, f"Estado: {estado}")
            y -= 10 * mm
            c.drawString(20 * mm, y, f"Área: {area}")
            y -= 15 * mm
            c.setFont("Helvetica", 11)
            c.drawString(20 * mm, y, "Notícia:")
            y -= 8 * mm
            lines = simpleSplit(noticia_completa, "Helvetica", 11, width - 40 * mm)
            for line in lines:
                if y < 30 * mm:
                    c.showPage()
                    c.setFont("Helvetica", 11)
                    y = height - 20 * mm
                c.drawString(20 * mm, y, line)
                y -= 6 * mm
            c.save()
            print(f"PDF salvo como {pdf_path}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
