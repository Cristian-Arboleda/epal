#%%
email = 'Paovalen3000@gmail.com'
password = 'Andrea140627'
Discord = ''

mensaje_de_presentacion = '''
¡Hello! 🌟 I'm back and very excited to meet you. 💖 I hope we can share wonderful moments together. Tell me about yourself, I'm looking forward to learning more.✨'''

mensajes_de_respuesta = ''

from main_epal import *

iniciar_navegador(
    tipo_navegador = 'chrome_u',
    idioma = 'EN'
    )

iniciar_sesion(
    tipo_inicio = 'automatico',
    email = email,
    password = password
    )

#%%

while True:
    iniciar_el_envio_del_mensaje_de_presentacion(
        mensaje_de_presentacion = mensaje_de_presentacion, 
        mensajes_de_respuesta = mensajes_de_respuesta,
        numero_de_enlaces_a_recorrer = 100, 
        numero_maximo_de_mensajes_de_presentacion_a_enviar = 600
    )