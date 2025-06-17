from main_epal import *
email = 'valsara0627@gmail.com'
password = 'Aidnaici12'
Discord = 'alaia_.'
mensaje_de_presentacion = '''Hello I make video calls if you are interested you could write me to know more, I hope you like it and you can order me. 💗
: ¨·.·¨ :                                         
 ` ·. 
`╱|、
("u"`7
|、˜〵
じしˍ,)ノ'''

mensajes_de_respuesta = [
    "Hey guy", "Write to me on disc. I have special services for you ❤️", f"DC: {Discord}"]

iniciar_navegador(
    tipo_navegador='chrome_u',
    idioma='Es',
)

iniciar_sesion(
    tipo_inicio='manual',
    email=email,
    password=password
)

while True:
    iniciar_envio_de_mensajes_de_respuesta(
        lista_de_mensajes_de_respuesta=mensajes_de_respuesta,
        numero_de_mensajes_de_respuesta_a_enviar=300
    )
    iniciar_el_envio_del_mensaje_de_presentacion(
        mensaje_de_presentacion=mensaje_de_presentacion,
        mensajes_de_respuesta=mensajes_de_respuesta,
        numero_de_enlaces_a_recorrer=6,
        numero_maximo_de_mensajes_de_presentacion_a_enviar=300
        )


'''
Inglés (Estados Unidos): en-US
Español (España): es-ES
Francés (Francia): fr-FR
Alemán (Alemania): de-DE
Italiano (Italia): it-IT
Portugués (Brasil): pt-BR
Ruso: ru
Japonés: ja
Coreano: ko
'''