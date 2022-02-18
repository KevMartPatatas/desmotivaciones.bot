from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import facebook as fb
import urllib.request
import requests

#<--- autenticación de la API facebook --->
token_de_acceso = 'EAAJA8yQmGTIBANC7DSB9GjYE4hjDtjotsRg4MyLphvY4R8KZCgeBsDYAClhOxB6tpUNOo77uvUApRVUI08l8Dcxej8Y6dpvve7s9iw7VhPRga8oVYuqEGoZCmiSFHY166KRLjfzGgHYKWN3RCNoJWfDTQ1r55keP54VZBCyq6S2q8DqGVQf'
graph = fb.GraphAPI(access_token = token_de_acceso)


def leer_numero_foto():
    file = open('recursos/numero_imagen.txt', 'r')
    nombre_foto = int(file.read().strip())
    file.close()
    return nombre_foto


def reestablecer_numero_foto(nombre_foto):
    nombre_foto = nombre_foto + 1
    file = open('recursos/numero_imagen.txt', 'w')
    file.write(str(nombre_foto))
    file.close()


def descargar_imagen(src):
    ubicacion = 'imagenes/img_' + str(leer_numero_foto())+'.jpg'
    urllib.request.urlretrieve(src, ubicacion)
    print('Paso 3: Descargando la imagen')
    print('\tImagen descargada\n')


def leer_post_id():
    file = open('recursos/post_id.txt', 'r')
    post_id = file.read().strip()
    file.close()
    return post_id


def reestablecer_post_id(post_id):
    file = open('recursos/post_id.txt', 'w')
    file.write(str(post_id))
    file.close()


def crear_imagen(texto_principal_final, texto_secundario_final, numero_mayor_votos):  
    print('Paso 4: Creando la imagen final\n')

    imagen = Image.open('imagenes/img_' + str(leer_numero_foto()) + '.jpg') #<--- Esta es la imagen que ira en el medio. Esta sentencia carga la imagen
    img_baner = Image.open('recursos/baner/baner.png') #<--- Aca estoy cargando la imegn del baner

    #<--- Importacion de las fuentes. Ajustar el texto de fuente despues --->
    fuente_principal = ImageFont.truetype('recursos/fuentes/FreeSerif.ttf', 34)
    fuente_secundaria = ImageFont.truetype('recursos/fuentes/EkMukta-Medium.ttf', 17)

    #<--- Asignacion de los textos --->
    texto_principal = texto_principal_final
    texto_secundario = texto_secundario_final

    texto_principal_recortado = texto_principal[0:39] #<---- Recoge como maximo 40 caracteres
    texto_secundario_recortado = texto_secundario[0:84] #<---- Recoge como maximo 85 caracteres

    #<--- Aca voy a redimensionar la imagen a 650 pixeles
    ancho_imagen_nuevo = 650 - 66
    alto_imagen_nuevo = (imagen.size[1] * ancho_imagen_nuevo) / imagen.size[0] #<--- Formula para encontrar la altura en proporcion a la anchura de la imagen
    imagen = imagen.resize((ancho_imagen_nuevo, int(alto_imagen_nuevo))) #<--- Aca redimenziono la imagen

    #imagen.size ma da en alto y el ancho de la imagen cargada. Lo que hago aqui es asignar el tamaño del marco en el que iran las imagenes
    ancho_imagen_marco = ancho_imagen_nuevo + 66
    alto_imagen_marco = alto_imagen_nuevo + 135
    ancho_img_baner = img_baner.size[0] #<--- Obtengo el ancho de la imagen del baner
    marco = Image.new('RGB', (ancho_imagen_marco, int(alto_imagen_marco))) #<--- Esto crea la imagen que sera el fondo negro. La imagen es asignada en la variable marco

    #Estas coordenadas son los puntos finales para dibujar el ractangulo
    coordenada_final_rectangulo_x = ancho_imagen_marco - 31
    coordenada_final_rectangulo_y = alto_imagen_nuevo + 35
    coordenada_img_baner_x = ((ancho_imagen_marco - ancho_img_baner)/2) #<--- Esta coordenada es para posicionar al baner en el centro del marco

    #Aca se dibuja el rectangulo
    print('Paso 5: Dibujando marco\n')
    a = ImageDraw.ImageDraw(marco) #<--- La variable a es solo para representar, no se me pudo ocurrir otro nombre XD
    a.rectangle(((30, 30), (coordenada_final_rectangulo_x, coordenada_final_rectangulo_y)), fill = None, outline = 'white', width = 1)

    print('Paso 6: Dibujando texto\n')
    #<--- Comienzo. Dibujar el texto en el marco --->
        #<--- Texto principal --->
    dibujo_texto_principal = ImageDraw.Draw(marco)

    ancho_texto_principal, alto_texto_principal = dibujo_texto_principal.textsize(texto_principal_recortado, fuente_principal)
    #<--- Coordenadas para la insercion del dibujo dle texto principal --->
    coordenada_x_texto_principal = (ancho_imagen_marco - ancho_texto_principal)/2 #<--- Esto centra el texto
    coordenada_y_texto_principal = alto_imagen_nuevo + 56

    dibujo_texto_principal.text((int(coordenada_x_texto_principal), coordenada_y_texto_principal), texto_principal_recortado, (255, 255, 255), font = fuente_principal) #<--- Aca se dibuja el texto --->

        #<--- Texto secundario --->
    dibujo_texto_secundario = ImageDraw.Draw(marco)

    ancho_texto_secundario, alto_texto_secundario = dibujo_texto_secundario.textsize(texto_secundario_recortado, fuente_secundaria)
    #<--- Coordenadas para la insercion del dibujo dle texto secundario --->
    coordenada_x_texto_secundario = (ancho_imagen_marco - ancho_texto_secundario)/2 #<--- Esto centra el texto
    coordenada_y_texto_secundario = coordenada_y_texto_principal + alto_texto_principal + 7

    dibujo_texto_secundario.text((int(coordenada_x_texto_secundario), coordenada_y_texto_secundario), texto_secundario_recortado, (255, 255, 255), font = fuente_secundaria) #<--- Aca se dibuja el texto --->

    #<--- Se guarda el marco con los textos --->
    marco.save('marcos/marco_img_' + str(leer_numero_foto())+'.jpg') #<--- Esto guarda la imagen ya con el marco en blanco creado

    print('Paso 7: Fusionando las imagenes')
    #<--- Parte final, fusuion del marco e imagen. Tambien el baner --->
    marco.paste(imagen, (33, 33)) #<--- Esta sentencia fusiona las dos imagenes, el marco y la imagen, los numeros son las coordenadas de inicio

    marco.paste(img_baner, ((int(coordenada_img_baner_x)), (int(coordenada_final_rectangulo_y) - 7))) #<--- Aca estoy fusionando el marco con el baner
    marco.save('export/imagen_final_' + str(leer_numero_foto()) + '.jpg') #<--- Esta sentencia me guarda la imagen fusuionada

    print('\tImagen final Lista\n')

    print('Paso 8: Publicando la imagen')
    publicar_imagen = graph.put_photo(image = open("export/imagen_final_" + str(leer_numero_foto()) + ".jpg", "rb"), message = 'Su pedido.' + '\nNúmero de imagen: ' + str(leer_numero_foto())) #<--- Esto tambien me da datos de la publicacion
    post_id = publicar_imagen['id']
    print('\tImagen publicada')
    print('\tID:', post_id)
    print('\tPOST ID:', publicar_imagen['post_id'] + '\n')

    reestablecer_post_id(post_id)

    print('Paso 9: Poniendo un comentario en la publicacion reciente\n')
    id_publicacion = publicar_imagen['post_id'] #<--- Obtengo su ID
    graph.put_comment(object_id=id_publicacion, message='Número de votos: ' + str(numero_mayor_votos)) #<--- Pongo un comentario

    print('Paso 10: Reestableciendo el numero de imagen\n')
    reestablecer_numero_foto(leer_numero_foto())

    print('Realizado todo con exito')


def obtener_comentarios():
    comentarios = graph.get_connections(id = leer_post_id(), connection_name='comments') #<--- Me devuelve los comentarios en un post

    print('Paso 1: Obteniendo los comentarios e iterandolos\n')

    numero_mayor_votos = -100

    #<--- Itera sobre los comentarios --->
    for comentarios['data'] in comentarios['data']:
        comentario_id = comentarios['data']['id'] #<--- Me da la ID de los comentarios

        #<--- Solicitud de informacion de los comentarios --->
        url_solicitar_informacion_comentario = "https://graph.facebook.com/" + comentario_id + "?fields=attachment&access_token=" + token_de_acceso #<--- Manda una solicitud HTTP a la api de facebook
        solicitud_informacion_comentario = requests.get(url_solicitar_informacion_comentario).json()

        if (len(solicitud_informacion_comentario) == 2): #<--- Esto comprueba que los comentarios tengan algun archivo
            tipo_archivo_adjunto = solicitud_informacion_comentario['attachment']['type'] #<--- Me da el tipo de archivo que contiene el comentario

            if (tipo_archivo_adjunto == 'photo'): #<--- Esto comprueba que el archivo adjunto sea una imagen
                mensaje = comentarios['data']['message'] #<--- Me da el texto de los comentarios

                separar_texto_comentario = mensaje.split(sep = '\n') #<--- Esto me separa el texto por cada salto de linea

                if len(separar_texto_comentario) == 3: #<--- Esto me comprueba que las lineas solo sean

                    if separar_texto_comentario[0] == '!req': #<--- Esto me comprueba que el comentario tenga como primera linea !req
                        url_solicitar_like = 'https://graph.facebook.com/' + comentario_id + '?fields=reactions.type(LIKE).limit(0).summary(total_count)&access_token=' + token_de_acceso
                        solicitar_like = requests.get(url_solicitar_like).json()

                        url_solicitar_love = 'https://graph.facebook.com/' + comentario_id + '?fields=reactions.type(LOVE).limit(0).summary(total_count)&access_token=' + token_de_acceso
                        solicitar_love = requests.get(url_solicitar_love).json()

                        url_solicitar_wow = 'https://graph.facebook.com/' + comentario_id + '?fields=reactions.type(WOW).limit(0).summary(total_count)&access_token=' + token_de_acceso
                        solicitar_wow = requests.get(url_solicitar_wow).json()

                        url_solicitar_haha = 'https://graph.facebook.com/' + comentario_id + '?fields=reactions.type(HAHA).limit(0).summary(total_count)&access_token=' + token_de_acceso
                        solicitar_haha = requests.get(url_solicitar_haha).json()

                        url_solicitar_sad = 'https://graph.facebook.com/' + comentario_id + '?fields=reactions.type(SAD).limit(0).summary(total_count)&access_token=' + token_de_acceso
                        solicitar_sad = requests.get(url_solicitar_sad).json()

                        url_solicitar_angry = 'https://graph.facebook.com/' + comentario_id + '?fields=reactions.type(ANGRY).limit(0).summary(total_count)&access_token=' + token_de_acceso
                        solicitar_angry = requests.get(url_solicitar_angry).json()

                        numero_likes = solicitar_like['reactions']['summary']['total_count']
                        numero_love = solicitar_love['reactions']['summary']['total_count']
                        numero_wow = solicitar_wow['reactions']['summary']['total_count']
                        numero_haha = solicitar_haha['reactions']['summary']['total_count']
                        numero_sad = solicitar_sad['reactions']['summary']['total_count']
                        numero_angry = solicitar_angry['reactions']['summary']['total_count']

                        voto_total = numero_likes + numero_love + numero_wow + numero_haha - numero_sad - numero_angry #<--- Sistema de votos

                        if voto_total > numero_mayor_votos:
                            numero_mayor_votos = voto_total

                            src = solicitud_informacion_comentario['attachment']['media']['image']['src'] #<--- Este es el link de la imagen

                            comentario_id_final = comentario_id
                            mensaje_final = mensaje

                            texto_principal_final = separar_texto_comentario[1]
                            texto_secundario_final = separar_texto_comentario[2]  


    if numero_mayor_votos != -100:
        #<--- DATOS DEL COMENTARIO CON MAS VOTOS --->
        print('Paso 2: Obteniendo el pedido con mayor numero de votos\n\n\n')

        print('\tNumero de votos: ' + str(numero_mayor_votos) + '\n')
        print('\tURL de la imagen: ' + src + '\n')
        print('\tID del comentario: ' + comentario_id_final + '\n')
        print('\tMensaje: ' + mensaje_final + '\n')

        print('\tTexto principal: ' + texto_principal_final)
        print('\tTexto secundario: ' + texto_secundario_final + '\n\n\n')

        descargar_imagen(src)
        crear_imagen(texto_principal_final, texto_secundario_final, numero_mayor_votos)

    else:
        print('No hay nada que hacer aqui')
        print('ID del post: ' + leer_post_id())


obtener_comentarios()