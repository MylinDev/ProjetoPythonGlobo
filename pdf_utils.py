from gpt_utils import resumir_texto_openai
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth

def gerar_pdf(noticia, estado, area, data_pub, idx):
    font_dir = os.getcwd()
    roboto_regular = os.path.join(font_dir, "Roboto-Regular.ttf")
    roboto_bold = os.path.join(font_dir, "Roboto-Bold.ttf")
    if os.path.exists(roboto_regular):
        pdfmetrics.registerFont(TTFont("Roboto", roboto_regular))
    if os.path.exists(roboto_bold):
        pdfmetrics.registerFont(TTFont("Roboto-Bold", roboto_bold))
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
    c.setFillColorRGB(0, 0, 1)
    c.drawString(20 * mm, y, link_text)
    link_width = c.stringWidth(link_text, "Helvetica-Oblique", 10)
    c.linkURL(link, (20 * mm, y, 20 * mm + link_width, y + 10 * mm), relative=0)
    c.setFillColorRGB(0, 0, 0)
    if "Roboto-Bold" in pdfmetrics.getRegisteredFontNames():
        c.setFont("Roboto-Bold", 12)
    else:
        c.setFont("Helvetica-Bold", 12)
    titulo_label = "Título: "
    titulo = noticia['titulo']
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
            # Redesenha fundo e faixa vermelha
            c.setFillColorRGB(1, 1, 1)
            c.rect(0, 0, width, height, fill=1, stroke=0)
            c.setFillColorRGB(196/255, 23/255, 12/255)
            faixa_altura = 25 * mm
            c.rect(0, height - faixa_altura, width, faixa_altura, fill=1, stroke=0)
            # Redesenha título do topo
            c.setFont(font_title, 16)
            c.setFillColorRGB(1, 1, 1)
            c.drawString(20 * mm, height - 18 * mm, "Vaga de Emprego")
            c.setFillColorRGB(0, 0, 0)
            c.setFont(font_title, 12)
            y = height - faixa_altura - 10 * mm
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
    noticia_completa = noticia.get("resumo", "")
    # Resumir o texto usando OpenAI antes de gerar o PDF
    resumo = resumir_texto_openai(noticia_completa)
    lines = simpleSplit(resumo, "Helvetica", 11, width - 40 * mm)
    for line in lines:
        if y < 30 * mm:
            c.showPage()
            # Redesenha fundo e faixa vermelha
            c.setFillColorRGB(1, 1, 1)
            c.rect(0, 0, width, height, fill=1, stroke=0)
            c.setFillColorRGB(196/255, 23/255, 12/255)
            faixa_altura = 25 * mm
            c.rect(0, height - faixa_altura, width, faixa_altura, fill=1, stroke=0)
            # Redesenha título do topo
            c.setFont(font_title, 16)
            c.setFillColorRGB(1, 1, 1)
            c.drawString(20 * mm, height - 18 * mm, "Vaga de Emprego")
            c.setFillColorRGB(0, 0, 0)
            c.setFont("Helvetica", 11)
            y = height - faixa_altura - 10 * mm
        c.drawString(20 * mm, y, line)
        y -= 6 * mm
    c.save()
    print(f"PDF salvo como {pdf_path}")
    return pdf_path
