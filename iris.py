#%%
email = 'lorenreyes@gmail.com'
password = 'Lorena123'
Discord = 'ho.ttie'

mensaje_de_presentacion = '''💮 Hello, I make video calls, you can enter my profile and if you are interested in something about me, send me a message, I will be very attentive to you, I hope you are having a nice day💮
'''
mensajes_de_respuesta = ["Hello, love 😘", "If you are interested in me", f"Write to me on disc: {Discord}"]


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

#%%
iniciar_el_envio_del_mensaje_de_presentacion(
        mensaje_de_presentacion = mensaje_de_presentacion, 
        mensajes_de_respuesta = mensajes_de_respuesta,
        numero_de_enlaces_a_recorrer = 2, 
        numero_maximo_de_mensajes_de_presentacion_a_enviar = 100
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
