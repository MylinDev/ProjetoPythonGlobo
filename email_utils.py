import os
from email.message import EmailMessage
import smtplib
from rich import print

# Função para enviar e-mail com PDF em anexo, usando variáveis de ambiente para credenciais, crie um arquivo .env na raiz do projeto e coloque suas credenciais lá. 
def enviar_email(destinatario, assunto, corpo, caminho_pdf):
    try:
        message = EmailMessage()
        message['Subject'] = assunto
        message['From'] = os.getenv("SENDER_EMAIL")
        message['To'] = destinatario
        message.set_content(corpo)
        with open(caminho_pdf, 'rb') as f:
            pdf_data = f.read()
            message.add_attachment(pdf_data, maintype='application', subtype='pdf', filename=os.path.basename(caminho_pdf))
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_PASSWORD"))
        server.send_message(message)
        server.quit()
        print("[green]E-mail enviado com sucesso![/green]")
    except Exception as e:
        print(f"[red]Erro ao enviar e-mail: {e}[/red]")
