import imaplib
import email
from email.header import decode_header
import requests


def login(user, pwd):
    #especificamos el imap a usar
    imap = imaplib.IMAP4_SSL("imap.gmail.com")

    #iniciamos sesion y seleccionamos el buzon
    imap.login(user, pwd)
    status, messages = imap.select("INBOX")
    messages = int(messages[0])

    #retornamos la cantidad de mensajes en el buzon y la conexion del imap
    return messages, imap


def extraer(messages, imap):
    n = 50
    #ajustamos para que lea desde los emails mas recientes
    for i in range(messages, messages-n, -1):
        # extraemos los emails por ID
        res, msg = imap.fetch(str(i), "(RFC822)")
    
        for response in msg:
            if isinstance(response, tuple):
                # pasamos los emails en bites a un objeto
                msg = email.message_from_bytes(response[1])
            
                # decodificamos el asunto del email
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # Si son bites, convertimos a string
                    subject = subject.decode(encoding)
                #si existe el email con este asunto
                if "falta stock" in subject.lower():
                    print("Subject:", subject)

                    # iteramos en las partes del email
                    for part in msg.walk():
                        # extraemos el tipo de contenido del email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            # obtenemos el valor buscado del cuerpo del email
                            body = part.get_payload(decode=True).decode()
                            id = ''
                            for c in body:
                                if c.isdigit():
                                    id += c
                        except:
                            pass
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            print(id)
                    break
                #retornamos la id en el cuerpo
                try:
                    return id
                except:
                    print('No se encontro el email requerido')
                    quit()
                    
def get(id):
    #enviamos la id a la ruta y le damos formato JSON a la respuesta
    api_url = f"https://webhook.site/51ec7249-ec8c-4426-9f26-a210ddf39d8c/?id={id}"
    response = requests.get(api_url)
    print(response.json())

messages, imap = login("maestreanthonyac@gmail.com", "scwgzigrfwnoocya")
id = extraer(messages, imap)
get(id)

# Cerramos la conexion y la sesion
imap.close()
imap.logout()