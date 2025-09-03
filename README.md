# Projeto Globo Vagas de Emprego - PDF Automático

Este projeto automatiza a busca de notícias sobre vagas de emprego no portal G1/Globo usando Selenium, e gera um PDF profissional para cada notícia encontrada.

## O que o script faz?
- Busca notícias do dia sobre vagas de emprego no G1/Globo (limite de 20), mas basta colocar mais ou tirar o limite, qualquer coisa entre
 em contato que respondo dúvidas sobre o código.
- Extrai título completo, resumo, data, estado, área e link da notícia.
- Acessa a notícia para pegar o texto completo e o título real (não cortado).
- Gera um PDF para cada notícia, com layout profissional (faixa vermelha, fontes Roboto, link clicável, etc).
- O nome do PDF inclui estado, área, data e índice.

## Pré-requisitos
- Python 3.8+
- Google Chrome instalado
- Chromedriver compatível (instalado automaticamente pelo script)
- As fontes Roboto-Regular.ttf e Roboto-Bold.ttf na mesma pasta do script (baixe em https://fonts.google.com/specimen/Roboto)

## Instalação
1. Clone ou baixe este repositório.
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
3. Baixe as fontes Roboto (Regular e Bold) e coloque na pasta do projeto.

## Como executar
1. Abra o terminal na pasta do projeto.
2. Execute o script:
   ```
   python Codigo.py
   ```
3. Os PDFs serão gerados na mesma pasta, um para cada notícia encontrada.

## Observações
- O script usa Selenium em modo headless (não abre janela do navegador).
- O layout do PDF é inspirado nas cores do G1.
- O script só pega notícias do dia (data de hoje ou "há X horas/minutos").

---
Dúvidas? Abra uma issue ou entre em contato.
