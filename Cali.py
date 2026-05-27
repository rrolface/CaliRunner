#Santiago Osorio Granobles

#Mi idea Principal para este juego es basandome en la ciudad de cali para nadie es un secreto que una de las
#problematicas mas grandes de la ciudad es el estado de las calles, y es algo que vivo a diario en mi moto, por
# por lo tanto quise plasmar esa problematica en este juego mediante un juego de tipo runner donde el 
#jugador tiene que esquivar los huecos de las calles, ademas de eso quise agregar un toque de la cultura
#caleña como tal. :)

import pygame
import sys
import random

pygame.init()

Ancho_Pantalla = 800
Alto_Pantalla = 500

pantalla = pygame.display.set_mode((Ancho_Pantalla, Alto_Pantalla))
pygame.display.set_caption("Cali Runner")

fps = pygame.time.Clock()

#El juego va a tener 3 Carriles por los cuales nos vamos a poder mover con la moto para esquivar los huecos
Color1 = (100, 100, 100) #EL gris para la carretera
Color2 = (255, 255, 255)#El blanco para las lines de los Carriles

Carriles = [250,350, 450] 

#Tenia dudas de que agregar como personaje principal, pero me decidi por una Moto ya que es lo que vivo casi todos los dias :)
carril_actual = 1
moto_x = 100
moto_y = Carriles[carril_actual]

#Los obstaculos van a ser "Huecos" y "Conos" los cuales van a aparecer de forma random.
huecos = []
conos = []
llantas = []
velocidad = 5
timer_huecos = 0
timer_conos = 0
timer_llantas = 0
llantas_recogidas = 0

#Game Over
estado_juego = True
fuenteGameOver = pygame.font.SysFont("Times New Roman", 70)
fuenteReload = pygame.font.SysFont("Times New Roman", 30)

#Puntaje y Aumento de velocidad (El puntaje lo pense manejar como "Cuadras Recorridas").
cuadras_recorridas = 0
fuenteCuadras = pygame.font.SysFont("Times New Roman", 25)

#Assets Moto - Cono - Hueco - Bandera - Ciudad - Cristo Rey
moto_img = pygame.image.load("AssetsCali/bike.png")
moto_img = pygame.transform.scale(moto_img, (70,45))
cono_img = pygame.image.load("AssetsCali/cono.png")
cono_img = pygame.transform.scale(cono_img, (40,40))
hueco_img = pygame.image.load("AssetsCali/hueco.png")
hueco_img = pygame.transform.scale(hueco_img, (50,30))
ciudad_img = pygame.image.load("AssetsCali/ciudad.png")
ciudad_img = pygame.transform.scale(ciudad_img, (800, 220))
colombia_img = pygame.image.load("AssetsCali/colombia.png")
colombia_img = pygame.transform.scale(colombia_img, (150,100))
cristorey_img = pygame.image.load("AssetsCali/cristorey.png")
cristorey_img = pygame.transform.scale(cristorey_img, (300,400))
rueda_img = pygame.image.load("AssetsCali/rueda.png")
rueda_img = pygame.transform.scale(rueda_img, (60,60))


#Musica de Fondo (De cali Obviamente :) )
pygame.mixer.music.load("AssetsCali/OigaMireVea.mp3")
pygame.mixer.music.play(-1)  
sonido_choque = pygame.mixer.Sound("AssetsCali/choque.mp3")

#funcion de la pantalla principal
def pantalla_inicio():
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    esperando = False

        pantalla.fill((135, 206, 235))
        pantalla.blit(ciudad_img, (10, 12))
        pantalla.blit(cristorey_img, (250, -85))
        pantalla.blit(colombia_img, (650, 10))
        pygame.draw.rect(pantalla, Color1, (0, 200, 800, 300))

        # Titulo
        titulo = fuenteGameOver.render("CALI RUNNER", True, (255, 220, 0))
        rect_titulo = titulo.get_rect(center=(Ancho_Pantalla // 2, 270))
        sombra_titulo = fuenteGameOver.render("CALI RUNNER", True, (0, 0, 0))
        pantalla.blit(sombra_titulo, (rect_titulo.x + 3, rect_titulo.y + 3))
        pantalla.blit(titulo, rect_titulo)

        # Instrucciones
        inst = fuenteReload.render("Presiona ESPACIO para comenzar", True, (255, 255, 255))
        rect_inst = inst.get_rect(center=(Ancho_Pantalla // 2, 350))
        pantalla.blit(inst, rect_inst)

        # Controles
        ctrl = fuenteCuadras.render("Flechas arriba/abajo para cambiar de carril", True, (255, 255, 255))
        rect_ctrl = ctrl.get_rect(center=(Ancho_Pantalla // 2, 400))
        pantalla.blit(ctrl, rect_ctrl)

        pygame.display.flip()
        fps.tick(60)

# funcion Game Over
def game_over():
        global huecos, conos, llantas, timer_llantas, llantas_recogidas, timer_huecos, timer_conos, carril_actual, moto_y, velocidad, cuadras_recorridas
        sonido_choque.play()
        pygame.mixer.music.pause()
        pantalla.fill((0, 0, 0))
        texto_game_over = fuenteGameOver.render("Se le Poncho la llanta pana!", True, (255, 0, 0))
        rect_go = texto_game_over.get_rect(center=(Ancho_Pantalla//2, Alto_Pantalla//2 - 60))
        pantalla.blit(texto_game_over, rect_go)
        texto_reload = fuenteReload.render("Presiona R para volver a la Ciudad", True, (255, 255, 255))
        rect_reload = texto_reload.get_rect(center=(Ancho_Pantalla//2, Alto_Pantalla//2 + 60))
        pantalla.blit(texto_reload, rect_reload)
        pygame.display.flip()
        espera = True
        while espera:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                     pygame.quit()
                     sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        sonido_choque.stop()
                        pygame.mixer.music.play(-1)
                        huecos = []
                        conos = []
                        llantas = []
                        timer_huecos = 0
                        timer_conos = 0
                        timer_llantas = 0
                        carril_actual = 1
                        moto_y = Carriles[carril_actual]
                        velocidad = 5
                        cuadras_recorridas = 0
                        llantas_recogidas = 0
                        espera = False
            
        return False


#juego activo   
pantalla_inicio()
while estado_juego:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #aqui estaria la logica de movimiento entre carriles de la moto
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and carril_actual > 0:
                carril_actual  = carril_actual - 1
                moto_y = Carriles[carril_actual]
            if event.key == pygame.K_DOWN and carril_actual < 2:
                carril_actual = carril_actual + 1
                moto_y = Carriles[carril_actual]


#Vamos a generar un hueco cada 60 frames, van a aparecer de manera random en los carriles y posteriormente se eliminaran.
    timer_huecos += 1
    if timer_huecos > 60:
        carril_random = random.randint(0,2)
        huecos.append([800, Carriles[carril_random]])
        timer_huecos = 0
    for hueco in huecos:
        hueco[0] = hueco[0] - velocidad
    huecos = [hueco for hueco in huecos if hueco[0] > -50]

#Vamos a generar un cono cada 90 frames, van a aparecer de manera random en los carriles y posteriormente se eliminaran.
    timer_conos = timer_conos + 1
    if timer_conos > 90: 
        carril_random = random.randint(0,2)
        conos.append([800, Carriles[carril_random]])
        timer_conos = 0
    for cono in conos:
        cono[0] = cono[0] - velocidad
    conos = [cono for cono in conos if cono[0] > -50]

#logica de Cuadras (cada 5 segundos nos deberia sumar una cuadra recorrida)
    cuadras_recorridas = cuadras_recorridas + 1
    velocidad = 5 + (cuadras_recorridas // 500)
    
#Colisiones con los Huecos y Conos
    rect_moto = pygame.Rect(moto_x, moto_y - 20, 50, 35)
    for hueco in huecos:
        rect_hueco = pygame.Rect(hueco[0], hueco[1] - 15, 40, 25)
        if rect_moto.colliderect(rect_hueco):
            if llantas_recogidas > 0:
                llantas_recogidas -= 1
                huecos.remove(hueco)
                break
            else:
                game_over()

    for cono in conos:
        rect_cono = pygame.Rect(cono[0], cono[1] - 20, 30, 35)
        if rect_moto.colliderect(rect_cono):
            if llantas_recogidas > 0:
                llantas_recogidas = llantas_recogidas - 1
                conos.remove(cono)
                break
            else:
                game_over()

#Logica de la aparicion de las llantas
    timer_llantas = timer_llantas + 1
    if timer_llantas > 120:
        carril_random = random.randint(0,2)
        llantas.append([800, Carriles[carril_random]])
        timer_llantas = 0
    for llanta in llantas:
        llanta[0] = llanta[0] - velocidad
    llantas = [llanta for llanta in llantas if llanta[0] > -50]

#Recoger las llantas
    for llanta in llantas:
        rect_llanta = pygame.Rect(llanta[0], llanta[1] - 15, 30, 30)
        if rect_moto.colliderect(rect_llanta):
            llantas_recogidas = llantas_recogidas + 1
            llantas.remove(llanta)
            break


    pantalla.fill((135, 206, 235))

    #Fondo de la ciudad - Bandera - Cristo Rey
    pantalla.blit(ciudad_img, (10, 12))
    pantalla.blit(colombia_img, (650, 10))
    pantalla.blit(cristorey_img, (250, -85))
        
    #La carretera en general va a ser de Color Gris.
    pygame.draw.rect(pantalla, Color1, (0,200, 800, 300))
    #esa carretera va a estar dividida en 3 carriles de color Blanco.
    pygame.draw.line(pantalla, Color2, (0,300), (800,300), 3)
    pygame.draw.line(pantalla, Color2, (0,400), (800,400), 3)

    #Aparicion de los huecos
    for hueco in huecos:
        pantalla.blit(hueco_img, (hueco[0], hueco[1] - 15))
    
    #Aparicion de la Moto
    pantalla.blit(moto_img, (moto_x, moto_y - 20))

    #Aparicion de los Conos
    for cono in conos:
        pantalla.blit(cono_img, (cono[0], cono[1] - 20))

    #Aparicion de las llantas
    for llanta in llantas:
        pantalla.blit(rueda_img, (llanta[0] - 15, llanta[1] - 15))

# Texto
    # Cuadras
    sombra_cuadras = fuenteCuadras.render(f"Cuadras Recorridas: {cuadras_recorridas // 300}", True, (0, 0, 0))
    pantalla.blit(sombra_cuadras, (12, 12))
    texto_cuadras = fuenteCuadras.render(f"Cuadras Recorridas: {cuadras_recorridas // 300}", True, (255, 220, 0))
    pantalla.blit(texto_cuadras, (10, 10))

# Llantas
    sombra_llantas = fuenteCuadras.render(f"Llantas: {llantas_recogidas}", True, (0, 0, 0))
    pantalla.blit(sombra_llantas, (12, 37))
    texto_llantas = fuenteCuadras.render(f"Llantas: {llantas_recogidas}", True, (255, 220, 0))
    pantalla.blit(texto_llantas, (10, 35))

    pygame.display.flip()
    fps.tick(60)


    



