
import os
import re
from datetime import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from globo_scraper import get_noticias_globo_selenium
from pdf_utils import gerar_pdf
from email_utils import enviar_email

load_dotenv()


# Busca notícias sobre vagas de emprego no G1/Globo
SEARCH_URL_BASE = "https://g1.globo.com/busca/?q=vaga+de+emprego"
LIMITE = 20



# Aqui estou colocando a função main para organizar o fluxo do programa, com estados e áreas de interesse.
def main():
    print("Obtendo notícias sobre vagas de emprego com Selenium...")
    options = Options()
    options.headless = True
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    try:
        noticias = get_noticias_globo_selenium(driver, LIMITE, SEARCH_URL_BASE)
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
            if 'há' in data_pub_raw and ('hora' in data_pub_raw or 'minuto' in data_pub_raw):
                data_pub = datetime.now().strftime('%d/%m/%Y')
            else:
                data_pub = data_pub_raw
            pdf_path = gerar_pdf(noticia, estado, area, data_pub, idx)
            enviar_email(os.getenv("RECEIVER_EMAIL"), f"Nova vaga de emprego: {noticia['titulo']}", f"Uma nova vaga de emprego foi encontrada na sua área de interesse ({area}). Confira o PDF em anexo.", pdf_path)
    finally:
        driver.quit()
if __name__ == "__main__":
    main()
