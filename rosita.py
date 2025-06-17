email = 'Janihsalas404@gmail.com'
password = 'Adnioenxri14'
Discord = 'rosita_.fresita'

mensaje_de_presentacion = '''Hi, if you're interested and want to meet me, leave your message and I'll read you with much love.💗
─────▄█░░▀▀▀▀▀░░█▄
─▄▄──█░░░░░░░░░░░█──▄▄
█▄▄█─█░░▀░░┬░░▀░░█─█▄▄█'''

mensajes_de_respuesta = ["Hi, baby ❤️", "If you want you can write to me on disc", f"My disc: {Discord}"]

from main_epal import *

iniciar_navegador(
    tipo_navegador = 'chrome_u',
    idioma = 'EN'
)    

iniciar_sesion(
    tipo_inicio = 'manual',
    email = email,
    password = password
)

while True:
    iniciar_envio_de_mensajes_de_respuesta(
        lista_de_mensajes_de_respuesta = mensajes_de_respuesta,
        numero_de_mensajes_de_respuesta_a_enviar = 600
    )
    
    iniciar_el_envio_del_mensaje_de_presentacion(
        mensaje_de_presentacion = mensaje_de_presentacion, 
        mensajes_de_respuesta = mensajes_de_respuesta,
        numero_de_enlaces_a_recorrer = 6, 
        numero_maximo_de_mensajes_de_presentacion_a_enviar = 300
    )
