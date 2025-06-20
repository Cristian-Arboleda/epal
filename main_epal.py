#%%
# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#
import time, random
from difflib import SequenceMatcher
import re

es = '\n' + '='*100 + '\n'
inicio = '\033[1m Inicio:\033[0m'
error = '\033[1m ❌ Error:\033[0m'
final = '\033[1m Final:\033[0m'

def iniciar_navegador(tipo_navegador, idioma):
    ruta = r'C:\Users\crist\OneDrive\Documentos\Programacion\Automatizacion\Drivers'
    
    if tipo_navegador in ['chrome', 'chrome_u']:
        opciones_google(ruta, tipo_navegador, idioma)
    elif tipo_navegador == 'edge':
        opciones_edge(ruta, idioma)
    elif tipo_navegador == 'firefox':
        opciones_firefox(ruta, idioma)

def opciones_google(ruta, tipo_navegador, idioma):
    from selenium.webdriver.chrome.options import Options as Options_chrome
    from selenium.webdriver.chrome.service import Service
    
    import undetected_chromedriver as uc
    
    options = Options_chrome()
    
    options = Options_chrome()
    options.add_argument(f'--lang={idioma}') # Establece el idioma principal
    options.add_argument("--incognito") # El navegador se inicia en incognito
    options.add_argument("--blink-settings=imagesEnabled=false") # Desactiva las imagenes
    options.add_argument("--disable-translate")
    options.add_argument('--mute-audio') # Desactiva el sonido
    options.add_argument("--disable-notifications") # Desactiva las notificaciones del navegador Chrome
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Opciones para que el navegador se ejecute en segundo plano
    options.add_argument("--disable-backgrounding-occluded-windows") # Evita que las pestañas inactivas sean pausadas
    options.add_argument("--disable-renderer-backgrounding") # Evita que los procesos de renderizado sean limitados en segundo plano
    options.add_argument("--disable-background-timer-throttling") # Evita la reducción del rendimiento del navegador en segundo plano
    options.add_argument("--disable-ipc-flooding-protection") # Mantiene la ejecución activa sin restricciones en background
    options.add_argument("--disable-background-task-scheduling") # Impide que las tareas de bajo uso de CPU sean postergadas
    options.add_argument("--force-device-scale-factor=1") # Mantiene activo el navegador aunque no esté en foco
    options.add_argument("--disable-features=CalculateNativeWinOcclusion") # Evita que el sistema operativo reduzca la prioridad del navegador
    options.add_argument("--disable-tab-discarding") # Previene la suspensión de pestañas por inactividad
    options.add_argument("--disable-low-res-tiling") # Evita que el navegador reduzca el rendimiento cuando la ventana no está visible
    
    global document
    service = Service(executable_path=fr"{ruta}\chromedriver.exe")
    
    if tipo_navegador == "chrome":
        document = webdriver.Chrome(service=service, options=options)
    elif tipo_navegador == "chrome_u":
        document = uc.Chrome(service=service, options=options)

def opciones_edge(ruta, idioma,):
    from selenium.webdriver.edge.service import Service as service_edge
    from selenium.webdriver.edge.options import Options as options_edge
    #
    options = options_edge()
    options.add_argument("--start-maximized")
    options.add_argument("--mute-audio")
    options.add_argument(f"--lang={idioma}")
    options.add_argument("--blink-settings=imagesEnabled=false") # Desactiva las imagenes
    options.add_argument("--disk-cache-size=0") # Desactivar almacenamiento en caché
    options.add_argument("--disable-backgrounding-occluded-windows") #Evita que Edge pause pestañas que no están visibles.
    options.add_argument("--disable-renderer-backgrounding") # Evita que los procesos de renderizado de páginas sean limitados en segundo plano.
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--incognito")
    
    #Eliminar mensaje de automatizacion
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    # Cambiar User-Agent
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36")
    # Usar perfil real de usuario
    options.add_argument(r"user-data-dir=C:\Users\crist\AppData\Local\Microsoft\Edge\User Data")
    options.add_argument("profile-directory=Profile 3")
    
    service = service_edge(ruta + r'\msedgedriver.exe')
    
    global document
    document = webdriver.Edge(service=service, options=options)

def opciones_firefox(ruta, idioma):
    from selenium.webdriver.firefox.service import Service as service_firefox
    from selenium.webdriver.firefox.options import Options as options_firefox
    
    ruta = ruta + r'\geckodriver.exe'
    
    options = options_firefox()
    options.add_argument("--private")  # Modo privado
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference("useAutomationExtension", False)
    options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0")
    options.set_preference("dom.webnotifications.enabled", False)
    options.set_preference("media.navigator.enabled", False)
    options.set_preference("permissions.default.image", 2)
    
    service = service_firefox(ruta)
    
    global document
    document = webdriver.Firefox(service=service, options=options)
    document.execute_script("""
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    })
    """)

def iniciar_sesion(tipo_inicio, email, password):
    if tipo_inicio == 'manual':
        document.get('https://www.epal.gg/login')
        input('Esperando al inicio de sesion Manual: ')
    elif tipo_inicio == 'automatico':
        iniciar_sesion_automatica(email, password)
    
    x()#NO eleiminar esta funcion


def iniciar_sesion_automatica(email, password):
    document.get('https://www.epal.gg/login')
    
    # cerrar "HI, THERE"
    try:
        hi_there = WebDriverWait(document, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='ant-modal epal-modal epal-modal-L epal-modal-full']")))
        hi_there_button = hi_there.find_element(By.CSS_SELECTOR, "button[class='ant-modal-close']")
        hi_there_button.click()
        time.sleep(1)
    except:
        pass
    # cerrar "Cookie"
    try:
        contenedor = WebDriverWait(document, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='container___2iIsx']")))
        button = WebDriverWait(contenedor, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='epal-button epal-button-default-primary']")))
        button.click()
        time.sleep(1)
    except:
        pass
    
    print(es + f"{inicio} iniciando sesion automatica")
    
    title = document.title
    while title == document.title:
        print("Ingresando el e-mail")
        intento = 1
        while intento <= 10:
            try:
                contenedor = WebDriverWait(document, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='epal-input epal-input-large ant-select-selection-search-input']")))
                campo_email = contenedor.find_element(By.CSS_SELECTOR, "input")
                campo_email.send_keys(Keys.CONTROL + 'a')
                time.sleep(0.5)
                campo_email.send_keys(Keys.DELETE)
                time.sleep(0.5)
                campo_email.send_keys(email)
                time.sleep(2)
                campo_email.send_keys(Keys.ENTER)
                time.sleep(0.5)
                campo_email.send_keys(Keys.ENTER)
                time.sleep(2.5)
            except:
                print(f"{error} Al ingresar el e-mail")
                intento += 1
            
            # verificacion de que ya se paso a ingresar contrasena
            try:
                campo_password = WebDriverWait(document, 2.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='password']")))
                print('✅')
                break
            except:
                pass
            
            # Email Verificaiton
            try:
                WebDriverWait(document, 2.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='epal-verify-code']")))
                input('Ingresa el codigo de verificacion: ')
                return
            except:
                pass
            
            print(f"Numero de intentos al ingresar el correo: {intento}")
            if intento % 4 == 0:
                document.get('https://www.epal.gg/login')
                time.sleep(5)
            intento += 1
        
        
        print('Ingresando la contrasena')
        intento = 1
        while intento <= 5:
            try:
                campo_password = WebDriverWait(document, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
                campo_password.send_keys(Keys.CONTROL + 'a'); campo_password.send_keys(Keys.DELETE)
                time.sleep(0.5)
                campo_password.send_keys(password)
                time.sleep(0.5)
                campo_password.send_keys(Keys.ENTER)
                time.sleep(3)
                break
            except:
                print(f'{error} Al ingresas la contrasena')
            
            # Verificar
            try:
                contenedor = WebDriverWait(document, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='epal-input epal-input-large ant-select-selection-search-input']")))
                campo_email = contenedor.find_element(By.CSS_SELECTOR, "input")
                break
            except:
                pass
            
            # Email Verificaiton iniciar sesion con codigo
            try:
                
                WebDriverWait(document, 4).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='epal-verify-code']")))
                input('Ingresa el codigo para poder iniciar sesion: ')
                return
            except:
                pass
            
            print(f"Intento: {intento}")
            if intento % 4:
                document.refresh()
            intento += 1
    
    
    print('Se ha inicido sesion ✅' + es)


def x():
    global my_name
    my_name = obtener_my_name()
    
    # ------------> Obteniendo la lista de los enlaces a recorrer
    global list_enlaces
    list_enlaces = obtener_enlaces_epal()


def controlador_de_interrupciones():
    time.sleep(1)
    # Can you play with me for a while? (cerrar)
    try:
        contenedor = document.find_element(By.CSS_SELECTOR, "div[class='ant-modal-content']")
        button = contenedor.find_element(By.CSS_SELECTOR,"button[class='ant-modal-close']")
        button.click()
        print(es + 'Can you play with me for a while? (cerrar)')
    except:
        pass
    
    # Tips e-pal
    try:
        document.find_element(By.CSS_SELECTOR, 'button[aria-label="Close"]').click()
        print('Se cerro tips epal')
    except:
        pass


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def obtener_enlaces_epal():
    """
    Obtener los enlaces de los usuarios epal a las que se van a iterar
    """
    
    print(es + f"{inicio} Obteniendo los enlaces de las E-pal's (Obligatorio)")
    enlaces_list = []
    intento = 1
    while intento <= 12:
        try:
            document.get('https://www.epal.gg/leaderboard/epal')
            time.sleep(2)
            
            #       Obtener los enlaces de la lista top
            top_epals_list = WebDriverWait(document, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='h-[180px] relative z-10']")))
            top_epals_list = top_epals_list.find_elements(By.TAG_NAME, 'a')
            for epal in top_epals_list:
                enlace = epal.get_attribute('href')
                if enlace not in enlaces_list:
                    enlaces_list.append(enlace)
            
            #       Obtener los demas elementos de la lista epal
            for i in range(2):
                epal_items = WebDriverWait(document, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='py-8 px-6 space-y-6']")))
                epal_items = epal_items.find_elements(By.TAG_NAME, 'a')
                document.execute_script("arguments[0].scrollIntoView(true);",epal_items[-1])
                for epal in epal_items:
                    enlace = epal.get_attribute('href')
                    if enlace not in enlaces_list:
                        enlaces_list.append(enlace)
            # organizar la lista de enlaces de forma aleatoria
            random.shuffle(enlaces_list)
            print(f'Numero de enlaces obtenidos: {len(enlaces_list)}')
            return enlaces_list
        except:
            print(f'{error} Al intentar obtener los enlaces e-pals' + es)
            print(f'Intento: {intento}' + es)
            intento += 1
    if intento >= 12:
        print(f"{final} No se pudo obtener los enlaces de las e-pal's")




def obtener_my_name():
    '''Obtener el nombre de usuario de la cuenta en uso'''
    print(es + f'{inicio} Obteniendo el nombre de usuario de esta cuenta' )
    intento = 0
    while intento <= 7:
        try:
            # Abrir el perfil
            WebDriverWait(document, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class='avatarWarp___h1Tby']"))).click()
            time.sleep(5)
        except:
            controlador_de_interrupciones()
            pass
        
        # Obteniendo el elemento donde se encuentra el nombre de esta cuenta
        try:
            my_name = WebDriverWait(document, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='truncate epal-name cursor-pointer']"))).text
            print(f'Nombre de usuario: {my_name}')
            # cerrando el perfill
            try:
                WebDriverWait(document, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class='ant-drawer ant-drawer-right epal-drawer drawerWrapper___26ipK ant-drawer-open']"))).click()
            except:
                controlador_de_interrupciones()
            return my_name
        except:
            intento += 1
            print('Error: Al obtener el nombre de este usuario' + es)
            print(f'Intento: {intento}')
            if intento % 3 == 0:
                document.get('https://www.epal.gg/')
    print(f"{final} ")


# -------------> Creando la lista para guardar los enlaces ya recorridos y no repetirlos

list_enlaces_recorridos_totales = []
def iniciar_el_envio_del_mensaje_de_presentacion(
    mensaje_de_presentacion, 
    mensajes_de_respuesta, 
    numero_de_enlaces_a_recorrer = 2, 
    numero_maximo_de_mensajes_de_presentacion_a_enviar = 50
    ):
    """
    Enviar mensajes de presentacion

    Args:
        mensaje_de_presentacion (String): El mensaje de presentacion a enviar
        cantidad_de_mensajes_de_presentacion (int, optional): _description_. Defaults to 8.
    """
    
    print(es + f"{inicio} Enviando mensaje de presentacion")
    
    # ----------> Entrando a los enlaces para enviar mensajes a los visitantes
    
    for enlace in list_enlaces:
        
        if enlace in list_enlaces_recorridos_totales:
            print(f'Ya se habia recorrido el enlace {enlace}, continuar con el siguiente.')
            continue
        
        # Verificar que solo se recorran una cantidad de enlaces predefinidos
        if len(list_enlaces_recorridos_totales) >= numero_de_enlaces_a_recorrer:
            print(f"{final} Ya se han recorrido {len(list_enlaces_recorridos_totales)} enlaces" + es)
            break
        
        list_enlaces_recorridos_totales.append(enlace)
        
        # 1. Entrando al enlace de la e-girl(Obligatorio)
        print(es + f'{inicio} Entrando al enlace')
        print(f' {len(list_enlaces_recorridos_totales)}: {enlace}')
        
        # Entrando a la lista de visitantes del enlace
        if not entrar_a_la_lista_de_visitantes(enlace):
            continue
        
        # Empezando a enviar el mensaje de presentacion
        
        numero_de_mensajes_de_presentacion_enviados = 0
        lista_de_nombres_de_visitantes_temporales = []
        contador_de_ciclos = 0; comparador_de_visitantes = 0
        while len(lista_de_nombres_de_visitantes_temporales) <= numero_maximo_de_mensajes_de_presentacion_a_enviar:
            
            # Cancelar el envio de mensajes de presentacion si durante 3 ciclos no se obtienen nuevos visitantes en este enlace, esto significa que en este en enlace ahi menos visitantes de los mensajes que se quieren enviar
            
            if comparador_de_visitantes == len(lista_de_nombres_de_visitantes_temporales):
                contador_de_ciclos += 1
                print('No se han obtenido nuevos visitantes en este enlace')
                print(f"Contador: {comparador_de_visitantes}")
            else:
                contador_de_ciclos = 0
            if contador_de_ciclos >= 3:
                (print(f'Este enlace solo tiene {len(lista_de_nombres_de_visitantes_temporales)} visitantes, continuar con el siguiente enlace'))
                break
            
            comparador_de_visitantes = len(lista_de_nombres_de_visitantes_temporales)
            
            # Obteniendo la lista de los visitantes (obligatorio)
            intento = 0
            while intento <= 9:
                try:
                    contenedor_visitantes = WebDriverWait(document, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"div[class='ant-tabs-tabpane ant-tabs-tabpane-active'")))
                    lista_de_visitantes = contenedor_visitantes.find_elements(By.CSS_SELECTOR, "div[class='px-6 py-4 relative cursor-pointer bg-surface-district-normal']")
                    document.execute_script("arguments[0].scrollIntoView(true);", lista_de_visitantes[-1])
                    print(f'{final} Se obtuvo la lista de los visitantes' + es)
                    break
                except:
                    intento += 1
                    if intento % 4 == 0:
                        document.refresh()
                        time.sleep(8)
                    print(f'{error} Al intentar obtener la lista de los visitantes')
                    print(f'Intento: {intento}')
            if intento >= 9:
                print(f'{final} No se pudo obtener la lista de los visitanes. Continuar con el siguiente enlace' + es)
                time.sleep(10)
                break
            
            # -----------> Entrando al chat del visitante
            
            for visitante in lista_de_visitantes:
                
                # Obteniendo el nombre_del_visitante
                try:
                    nombre_del_visitante = WebDriverWait(visitante, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='text___He8CB epal-single-paragraph epal-name']"))).text
                except:
                    print(f'{error} Al obtener el nombre del visitante')
                    break
                
                # NO se pueden enviar mensajes a tu propio perfil (Opcional)
                
                if nombre_del_visitante == my_name:
                    continue
                
                # Verificar que no se repita el visitante durante el enlace
                if nombre_del_visitante in lista_de_nombres_de_visitantes_temporales:
                    continue
                else:
                    lista_de_nombres_de_visitantes_temporales.append(nombre_del_visitante)
                
                print(f"{len(lista_de_nombres_de_visitantes_temporales)}: {nombre_del_visitante}")
                
                
                # -------------->
                
                print(es + f'{inicio} Dar click en el visitante (Obligatorio)')
                try:
                    document.execute_script("arguments[0].scrollIntoView(true);", visitante)
                    visitante.click()
                    time.sleep(5)
                except:
                    controlador_de_interrupciones()
                    print(f'{error} al dar click en el visitante {nombre_del_visitante}')
                    time.sleep(5)
                    cerrar_visitante(nombre = nombre_del_visitante)
                    break
                
                # ----------->
                print(es + f"{inicio} Obteniendo el genero del visitante {nombre_del_visitante} (Obligatorio)")
                link_del_genero_femenino = 'data:image/png;base64,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'
                intento = 0
                while intento <= 3:
                    # Obteniendo el link del simbolo del genero del visitante
                    try:
                        contenedor_del_genero = WebDriverWait(document, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='identityBox']")))
                        contenedor_del_genero = contenedor_del_genero.find_elements(By.CSS_SELECTOR, "div[class='ant-space-item']")
                        link_del_genero_del_visitante = contenedor_del_genero[0].find_element(By.CSS_SELECTOR, "img[class='w-full h-full object-cover']").get_attribute('src')
                        print(f'{final} Se obtuvo el link del genero del visitante {nombre_del_visitante}' + es)
                        break
                    except:
                        intento += 1
                        print(f"{error} Al obtener el genero del visitante {nombre_del_visitante}")
                        print(f'Intento: {intento}')
                if intento >= 3:
                    print(f"{final} No se obtuvo el genero del visitante {nombre_del_visitante}. Salir y continuar con el siguiente visitante")
                    cerrar_visitante(nombre_del_visitante)
                    time.sleep(5)
                    continue
                
                if  link_del_genero_del_visitante == link_del_genero_femenino:
                    genero_del_visitante = 'femenino'
                    print(f'El genero del visitante {nombre_del_visitante} es {genero_del_visitante}')
                    print(f"Salir y continuar con el siguiente visitante" + es)
                    cerrar_visitante(nombre=nombre_del_visitante)
                    continue
                
                genero_del_visitante = 'masculino'
                print(f'El genero del visitante {nombre_del_visitante} es {genero_del_visitante}')
                
                
                # Dar click en "Chatear"
                
                print(f"{inicio} Dar click en 'Chatear'")
                intento = 0
                while intento <= 9:
                    try:
                        chatear = WebDriverWait(document, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.epal-button:nth-child(2) > span:nth-child(1)')))
                        chatear.click()
                        # Verificando que se dio click en "Chatear"
                        contenedor_de_mensajes_del_chat = WebDriverWait(document, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='msgContainer___G1P7E']")))
                        print(f"{final} Se entro al chat del visitante {nombre_del_visitante}")
                        time.sleep(5)
                        break
                    except:
                        controlador_de_interrupciones()
                        intento += 1
                        print(f"{error} al entrar al chat del del visitante {nombre_del_visitante}")
                        print(f"Intento: {intento}")
                if intento >= 9:
                    print(f"{final} No se pudo entrar al chat del visitante {nombre_del_visitante}. Salir y continuar con el siguiente visitante")
                    cerrar_visitante(nombre_del_visitante)
                    continue
                
                # Estoy dentro del chat
                numero_de_mensajes_de_este_chat = obtener_numero_de_mensajes_de_este_chat(nombre_del_visitante)
                
                if numero_de_mensajes_de_este_chat == None:
                    print('Salir y continuar con el siguiente visitante')
                    cerrar_lista_de_chats()
                    continue
                
                elif numero_de_mensajes_de_este_chat == 0:
                    enviar_mensaje_de_presentacion(mensaje_de_presentacion = mensaje_de_presentacion, nombre = nombre_del_visitante)
                    numero_de_mensajes_de_presentacion_enviados += 1
                    print(f"Numero de mensajes de presentacion enviados en este enlace {numero_de_mensajes_de_presentacion_enviados}")
                
                
                elif numero_de_mensajes_de_este_chat > 0:
                    numero_de_mensajes_recibidos = obtener_numero_de_mensajes_recibidos()
                    if numero_de_mensajes_recibidos > 0:
                        print(f"El visitante {nombre_del_visitante} ya nos respondio")
                        enviar_mensaje_de_respuesta(lista_de_mensajes_de_respuesta = mensajes_de_respuesta)
                        cerrar_lista_de_chats()
                    else:
                        print(f"El visitante {nombre_del_visitante} no nos ha respondido.")
                        cerrar_lista_de_chats()

def enviar_mensaje_de_respuesta(lista_de_mensajes_de_respuesta):
    #print(es + f'{inicio} Obteniendo los mensajes enviados')
    intento = 1
    while intento <= 10:
        try:
            time.sleep(2)
            contenedor_de_mensajes_del_chat = WebDriverWait(document, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='msgContainer___G1P7E']")))
            contenedor_de_mensajes_enviados = contenedor_de_mensajes_del_chat.find_elements(By.CSS_SELECTOR, "div[class='rightMsg___2-A5A']")
            print(f"Numero de mensajes enviados en este chat: {len(contenedor_de_mensajes_enviados)}")
            break
        except:
            print(f"{error} Al obtener los mensajes enviados en este chat")
            print(f"Intento: {intento}")
            intento += 1
    if intento >= 10:
        print(f"{final} No se pudo obtener los mensajes enviados en este chat")
        return
    
    # Guardar en una lista los mensajes en viados para ser comparados con la lista de mensajes de respuesta
    lista_de_mensajes_enviados = []
    for mensaje_enviado in contenedor_de_mensajes_enviados:
        mensaje_enviado = mensaje_enviado.find_element(By.CSS_SELECTOR, "div[class='messgageText___3JveQ']").text
        lista_de_mensajes_enviados.append(mensaje_enviado)
    
    if len(contenedor_de_mensajes_enviados) == 0:
        lista_de_mensajes_enviados = ['']
    # Comparar la lista de mensajes de respuesta con la lista de mensajes enviados
    
    for mensaje_de_respuesta in lista_de_mensajes_de_respuesta:
        for mensaje_enviado in lista_de_mensajes_enviados:
            similitud = similar(mensaje_enviado, mensaje_de_respuesta)
            if  similitud >= 0.6:
                print(f'Mensaje: "{mensaje_de_respuesta}" ✅')
                time.sleep(1)
                break
        
        # enviar el mensaje de respuesta por letra
        if similitud < 0.6:
            for letra in mensaje_de_respuesta:
                try:
                    campo_de_texto = WebDriverWait(document, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class*='ql-editor']")))
                    campo_de_texto.send_keys(letra)
                    time.sleep(0.01)
                except:
                    print(f"{error} Al enviar mensaje de respuesta por letra")
            try:
                campo_de_texto.send_keys(Keys.ENTER)
                time.sleep(0.5)
            except:
                print(f"{final} No se puedo enviar el mensaje de respuesta")
                time.sleep(5)
    print(es)
    time.sleep(2)


def enviar_mensaje_de_presentacion(mensaje_de_presentacion, nombre = None):
    print(es + f"{inicio} Enviando el mensaje de presentacion")
    intento = 0
    while intento <= 9:
        try:
            # Obteniendo campo de texto
            campo_de_texto = WebDriverWait(document, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class*='ql-editor']")))
            document.execute_script("arguments[0].textContent = arguments[1];", campo_de_texto, mensaje_de_presentacion)
            time.sleep(1)
            campo_de_texto.send_keys(Keys.ENTER)
            print(f"{final} Se envio el mensaje de presentacion a {nombre}" + es)
            time.sleep(1)
            cerrar_lista_de_chats()
            return True
        except:
            intento += 1
            print(f"{error} Envian el mensaje de presentacion")
            print(f"Intento {intento}")
    if intento >= 9:
        print(f"{final} No se pudo enviar el mensaje de presentacion a {nombre}" + es)
        cerrar_lista_de_chats()
        return False

def obtener_numero_de_mensajes_recibidos():
    time.sleep(1)
    intento = 1
    while intento <= 5:
        try:
            contenedor_de_mensajes = WebDriverWait(document, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='msgContainer___G1P7E']")))
            contenedor_de_mensajes_recibidos = contenedor_de_mensajes.find_elements(By.CSS_SELECTOR, "div[class='leftMsg___2NDOC']")
            numero_de_mensajes_recibidos = len(contenedor_de_mensajes_recibidos)
            print(f"Numero de mensajes recibidos: {numero_de_mensajes_recibidos}")
            return numero_de_mensajes_recibidos
        except:
            print(f"{error} Al obtener el numero de mensajes recibidos")
            print(f"Intento: {intento}")
            intento += 1


def cerrar_visitante(nombre = None):
    '''
    Salir del visitante
    
    Args:
        nombre(str, optional): nombre del visitante
    '''
    intento = 0
    while intento <= 1:
        try:
            contenedor_salir = WebDriverWait(document, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='px-6 pt-6 pb-5 flex justify-between items-center']")))
            salir = WebDriverWait(contenedor_salir, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='epal-iconButton epal-iconButton-default-tertiary epal-iconButton-circle']")))
            salir.click()
            time.sleep(2)
            return
        except:
            controlador_de_interrupciones()
            intento += 1
            print(f'{error} Al salir del chat del visitante {nombre}')
            print(f'Intento: {intento}')
    document.refresh()
    time.sleep(5)


def obtener_numero_de_mensajes_de_este_chat(nombre = None):
    print(es + f"{inicio} Obteniendo el numero de mensajes del chat de {nombre}")
    intento = 0
    while intento <= 9:
        try:
            contenedor_de_mensajes_del_chat = WebDriverWait(document, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='msgContainer___G1P7E']")))
            lista_de_mensajes_totales = contenedor_de_mensajes_del_chat.find_elements(By.CSS_SELECTOR, "div[_nk='iArf4+W15']")
            print(f"{final} Numero de mensajes en este chat {len(lista_de_mensajes_totales)}" + es)
            return len(lista_de_mensajes_totales)
        except:
            intento += 1
            print(f"{error} Al obtener los mensajes del chat de {nombre}")
            print(f'Intento: {intento}')
    if intento >= 9:
        print(f"{final} No se pudo obtener los mensajes del chat de {nombre}" + es)


def entrar_a_la_lista_de_visitantes(enlace):
    print(es + f"{inicio} Entrando a la lista de visitantes de este enlace (Obligatorio)")
    document.get(enlace + '?tab=about' )
    time.sleep(1)
    intento = 0
    while intento <= 9:
        try:
            # contenedor de followers, following, visitors
            contendor = WebDriverWait(document, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='p-2 rounded-m bg-surface-nest-normal grid grid-cols-3 gap-2']")))
            visitantes = contendor.find_elements(By.CSS_SELECTOR, 'div[class="cursor-pointer p-2"]')[2]
            visitantes.click()
            time.sleep(1)
            print('✅')
        except:
            pass
        
        try:
            # Obtener el nombre de usuario de este enlace dentro de la lista de visitanes para saber si se pudo entrar a la lista de visitantes
            nombre_del_enlace = WebDriverWait(document, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[class="txt-headline-m text-txt-primary-normal break-words"]'))).text
            print(f"{final} Se entro a la lista de visitantes de la e-gilr {nombre_del_enlace}" + es)
            return nombre_del_enlace
        except:
            controlador_de_interrupciones()
            intento += 1
            print(f"{error} Al entrar a la lista de visitantes")
            print(f"Intento: {intento}")
            if intento % 3 == 0:
                document.get(enlace + '?tab=about')
    print(f"{final} No se pudo entrar a la lista de visitantes")


def cerrar_lista_de_chats():
    print(es + f"{inicio} Cerrando la lista de chats ➡️")
    intento = 1
    while intento <=9:
        try:
            contenedor = WebDriverWait(document, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='w-[360px] border-r border-solid border-outline-normal h-screen flex flex-col']")))
            time.sleep(1)
            cerrar = contenedor.find_element(By.CSS_SELECTOR, "button[class='epal-iconButton epal-iconButton-default-tertiary epal-iconButton-circle']")
            cerrar.click()
            print('✅')
            time.sleep(3)
            return
        except:
            controlador_de_interrupciones()
            print(f"{error} Al cerrar lista de chats ➡️")
            print(f"Intento: {intento}")
            intento += 1
    document.refresh()
    time.sleep(5)


def iniciar_envio_de_mensajes_de_respuesta(lista_de_mensajes_de_respuesta, numero_de_mensajes_de_respuesta_a_enviar):
    abrir_lista_de_chats()
    lista_de_nombres_chat = []
    error_contenedor_chats = 0
    while len(lista_de_nombres_chat) <= numero_de_mensajes_de_respuesta_a_enviar:
        
        if len(lista_de_nombres_chat) > 0:
            print(f'Numero de chats recorridos: {len(lista_de_nombres_chat)}')
            time.sleep(2)
        
        intento = 1
        while intento <= 10:
            try:
                id_contenedor_de_chats = WebDriverWait(document, 10).until(EC.visibility_of_element_located((By.ID, 'imListContainer')))
                contenedor_de_chats = WebDriverWait(id_contenedor_de_chats, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='ReactVirtualized__Grid__innerScrollContainer']")))
                contenedor_de_chats = contenedor_de_chats.find_elements(By.CSS_SELECTOR, "li[class='ant-list-item']")
                time.sleep(1)
                break
            except:
                print(f"{error} Al obtener el contenedor de los chats")
                print(f"Intento: {intento}")
                time.sleep(5)
            if intento % 4 == 0:
                abrir_lista_de_chats()
            if intento % 6 ==0:
                document.refresh()
                time.sleep(10)
                abrir_lista_de_chats()
            intento += 1
        
        if error_contenedor_chats >= numero_de_mensajes_de_respuesta_a_enviar:
            print(es + f"{final} Se ha superado el numero de errores al obtener el nombre del chat: {error_contenedor_chats}")
            print("Cancelar el envio de mensajes de respuesta" + es)
            time.sleep(5)
            break
        
        # Recorrer chats
        
        for chat in contenedor_de_chats:
            
            #Obtener el nombre del chat
            try:
                #ActionChains(document).move_to_element(chat).perform()
                nombre_chat = chat.find_element(By.CSS_SELECTOR, 'div[class="text___He8CB epal-single-paragraph epal-name nick___3CpP_"]').text
            except:
                time.sleep(0.5)
                error_contenedor_chats += 1
                print(f"{error} Al obtener el nombre del chat")
                print(f"Error numero: {error_contenedor_chats}")
                print('Continuar con el siguiente chat')
                
                try:
                    ActionChains(document).move_to_element(contenedor_de_chats[-1]).perform()
                except:
                    pass
                break
            
            if nombre_chat in lista_de_nombres_chat:
                continue
            
            try:
                ActionChains(document).move_to_element(chat).perform()
                chat.click()
                time.sleep(2)
            except:
                controlador_de_interrupciones()
                print(f"{error} Al entrar en el chat del usuario {nombre_chat}")
                time.sleep(0.5)
                break
            
            lista_de_nombres_chat.append(nombre_chat)
            
            print(es + f"{lista_de_nombres_chat.index(nombre_chat) + 1}: {nombre_chat}")
            
            # verificar que tenga menos de 3 servicios
            numero_servicios = obtener_numero_de_servicios_del_chat()
            if numero_servicios > 3:
                print('Este usuario tiene mas de 3 servicios')
                print('Continuar con el siguiente chat')
                continue
            
            # verificar que la persona nos haya respondido el mensaje de presentacion
            
            numero_de_mensajes_recibidos = obtener_numero_de_mensajes_recibidos()
            if  numero_de_mensajes_recibidos  in [0, None]:
                print('Este usuario NO ha respondido')
                continue
            
            enviar_mensaje_de_respuesta(lista_de_mensajes_de_respuesta = lista_de_mensajes_de_respuesta)
        # Ir al ultimo elemento si no hay nuevos chats
        try:
            ActionChains(document).move_to_element(contenedor_de_chats[-1]).perform()
        except:
            pass
    print(f"Numero de chats recorridos: {len(lista_de_nombres_chat)}")


def obtener_numero_de_servicios_del_chat():
    time.sleep(1)
    try:
        numero_servicios_contenedor = WebDriverWait(document, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='border-b border-solid border-outline-normal py-6']")))
        numero_servicios = numero_servicios_contenedor.find_element(By.CSS_SELECTOR, "div[class='epal-chip epal-chip-active']").text
        numero_servicios = int(re.search(r'\d+', numero_servicios).group())
        print(f"Numero de servicios: {numero_servicios}")
        return numero_servicios
    except:
        print(f'Numero de servicios: 0')
        return 0


def abrir_lista_de_chats():
    print(es + f"{inicio} Abriendo la lista de chats ⬅️")
    time.sleep(2.5)
    intento = 1
    while intento <= 10:
        
        try:
            button = WebDriverWait(document, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='epal-iconButton epal-iconButton-default-tertiary cursor-pointer epal-iconButton-circle']")))
            button.click()
            print('✅')
            return
        except:
            controlador_de_interrupciones()
        
        # Verificar que la lista de chats ya haya estado abierta
        try:
            WebDriverWait(document, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[id="imListContainer"]')))
            print('La lista de chats ya estaba abierta')
            return
        except:
            pass
        
        print(f"{error} Al intentar abrir la lista de chats ⬅️")
        print(f"Intento: {intento}")
        
        if intento % 4 == 0:
            document.get('https://www.epal.gg/')
            time.sleep(5)
        if intento >= 10:
            print('No se pudo abrir la lista de chats')
            return
        intento += 1

# %%


