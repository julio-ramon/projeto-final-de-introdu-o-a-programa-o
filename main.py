import pygame

#tamanho da tela

LARGURA , ALTURA = 1000, 700

#cores 

AZUL = (100, 149, 237)
PRETO = (0 , 0 , 0)
VERDE = (0 ,100, 0)
VERMELHO = (100,0,0)

#constantes do jogo
FPS = 60
GRAVIDADE = 0.45
VELOCIDADE_MOVIMENTO = 5
TAMANHO_PERSONAGENS = (20 , 50)
ALTURA_DO_PULO = -10
ALTURA_DO_CHAO = 30
TOPO_CHAO = ALTURA - ALTURA_DO_CHAO
CHAO = ALTURA - TAMANHO_PERSONAGENS[1] - ALTURA_DO_CHAO
TETO = ALTURA

#funções
def criar_plataforma(x, y, largura, altura):
    return pygame.Rect(x, y, largura, altura)

def criar_parede(x, y, largura, altura):
    return pygame.Rect(x, y, largura, altura)



plataformas = [
    criar_plataforma(500, CHAO - 40, 50, 5),
    criar_plataforma(300,CHAO - 40, 100,5 )
]

plataformas_solidas = [
    criar_plataforma(600, CHAO - 80, 50, 5),

]

paredes = [
    criar_parede(-10, 0, 10, ALTURA),
    criar_parede(LARGURA, 0, 10, ALTURA),
    criar_parede(
        700,
        CHAO - ALTURA_DO_CHAO,
        5,
        TOPO_CHAO - (CHAO - ALTURA_DO_CHAO),
    )
    
]

#inicialização 
pygame.init() 
tela = pygame.display.set_mode((LARGURA , ALTURA))
pygame.display.set_caption("Jogo de Plataforma Multiplayer")
pygame.font.SysFont("Arial",36)
relogio = pygame.time.Clock()
rodando = True

#variaveis do jogo

personagem1_x , personagem1_y = 10 , CHAO
personagem2_x , personagem2_y = 100 , CHAO
velocidade1_y = 0
velocidade2_y = 0
no_chao1 = True
no_chao2 = True
na_plataforma1 = False
na_plataforma2 = False

#loop do jogo

while rodando:
    relogio.tick(FPS)
    tela.fill(AZUL)

    for evento in pygame.event.get():
        #evento para fechar o jogo
        if evento.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()

    
    if teclas[pygame.K_UP]:
        if no_chao1:
            velocidade1_y = ALTURA_DO_PULO
            no_chao1 = False
    if teclas[pygame.K_DOWN]:
        if na_plataforma1:
            personagem1_y += 2
            na_plataforma1 = False
            no_chao1 = False
    # personagem 2 (w , s)
    if teclas[pygame.K_w] :
        if no_chao2 :
            velocidade2_y = ALTURA_DO_PULO
            no_chao2 = False

    if teclas[pygame.K_s] :
        if na_plataforma2 :
            personagem2_y += 2
            na_plataforma2 = False
            no_chao2 = False
    
    movimento1_x = (
        int(teclas[pygame.K_RIGHT]) - int(teclas[pygame.K_LEFT])
    ) * VELOCIDADE_MOVIMENTO
    personagem1_x += movimento1_x

   
    retangulo_personagem1 = pygame.Rect(
        personagem1_x, personagem1_y, *TAMANHO_PERSONAGENS
    )
    for obstaculo in plataformas_solidas + paredes:
        if retangulo_personagem1.colliderect(obstaculo):
            if movimento1_x > 0:
                personagem1_x = obstaculo.left - TAMANHO_PERSONAGENS[0]
            elif movimento1_x < 0:
                personagem1_x = obstaculo.right
            retangulo_personagem1.x = personagem1_x
    # personagem 2
    movimento2_x = (
        int(teclas[pygame.K_d]) - int(teclas[pygame.K_a])
    ) * VELOCIDADE_MOVIMENTO
    personagem2_x += movimento2_x

    retangulo_personagem2 = pygame.Rect(
         personagem2_x, personagem2_y, *TAMANHO_PERSONAGENS
    )
    for obstaculo in plataformas_solidas + paredes:
            if retangulo_personagem2.colliderect(obstaculo):
                if movimento2_x > 0:
                    personagem2_x = obstaculo.left - TAMANHO_PERSONAGENS[0]
                elif movimento2_x < 0:
                    personagem2_x = obstaculo.right
                retangulo_personagem2.x = personagem2_x

    
    y_anterior1 = personagem1_y
    personagem1_y += velocidade1_y
    velocidade1_y += GRAVIDADE
    no_chao1 = False
    na_plataforma1 = False

    # personagem 2 
    y_anterior2 = personagem2_y
    personagem2_y += velocidade2_y
    velocidade2_y += GRAVIDADE
    no_chao2 = False
    na_plataforma2 = False

    if personagem1_y >= CHAO:
        personagem1_y = CHAO
        velocidade1_y = 0
        no_chao1 = True

    # personagem 2
    if personagem2_y >= CHAO:
            personagem2_y = CHAO
            velocidade2_y = 0
            no_chao2 = True

    for plataforma in plataformas:
        if (
            velocidade1_y >= 0
            and y_anterior1 + TAMANHO_PERSONAGENS[1] <= plataforma.top
            and personagem1_y + TAMANHO_PERSONAGENS[1] >= plataforma.top
            and personagem1_x + TAMANHO_PERSONAGENS[0] > plataforma.left
            and personagem1_x < plataforma.right
        ):
        
            personagem1_y = plataforma.top - TAMANHO_PERSONAGENS[1]
            velocidade1_y = 0
            no_chao1 = True
            na_plataforma1 = True
    # personagem 2
    for plataforma in plataformas :
        if(
            velocidade2_y >=0
            and y_anterior2 + TAMANHO_PERSONAGENS[1] <= plataforma.top
            and personagem2_y + TAMANHO_PERSONAGENS[1] > plataforma.top
            and personagem2_x + TAMANHO_PERSONAGENS[0] > plataforma.left
            and personagem2_x < plataforma.right
        ) :
            personagem2_y = plataforma.top - TAMANHO_PERSONAGENS[1]
            velocidade2_y = 0
            no_chao2 = True
            na_plataforma2 = True

    for obstaculo in plataformas_solidas + paredes:
        sobrepoe_horizontalmente1 = (
            personagem1_x + TAMANHO_PERSONAGENS[0] > obstaculo.left
            and personagem1_x < obstaculo.right
        )
        if not sobrepoe_horizontalmente1:
            continue

        if (
            velocidade1_y >= 0
            and y_anterior1 + TAMANHO_PERSONAGENS[1] <= obstaculo.top
            and personagem1_y + TAMANHO_PERSONAGENS[1] >= obstaculo.top
        ):
            personagem1_y = obstaculo.top - TAMANHO_PERSONAGENS[1]
            velocidade1_y = 0
            no_chao1 = True
        elif (
            velocidade1_y < 0
            and y_anterior1 >= obstaculo.bottom
            and personagem1_y <= obstaculo.bottom
        ):
            personagem1_y = obstaculo.bottom
            velocidade1_y = 0

        # personagem 2
    for obstaculo in plataformas_solidas + paredes :
        sobrepoe_horizontalmente2 = (
            personagem2_x  + TAMANHO_PERSONAGENS[0] > obstaculo.left
            and personagem2_x < obstaculo.right
        )   
        if not sobrepoe_horizontalmente2 :
            continue
        if (
            velocidade2_y >= 0
            and y_anterior2 + TAMANHO_PERSONAGENS[1] <= obstaculo.top
            and personagem2_y + TAMANHO_PERSONAGENS[1] >= obstaculo.top
        ):
            personagem2_y = obstaculo.top - TAMANHO_PERSONAGENS[1]
            velocidade2_y = 0
            no_chao2 = True
        elif (
            velocidade2_y < 0
            and y_anterior2 >= obstaculo.bottom
            and personagem2_y <= obstaculo.bottom
        ):
            personagem2_y = obstaculo.bottom
            velocidade2_y =0

    pygame.draw.rect(tela,PRETO, (personagem1_x, personagem1_y, *TAMANHO_PERSONAGENS))
    pygame.draw.rect(tela,VERMELHO, (personagem2_x, personagem2_y, *TAMANHO_PERSONAGENS))
    pygame.draw.rect(tela, VERDE, (0, TOPO_CHAO, LARGURA, ALTURA_DO_CHAO))
    for plataforma in plataformas:
        pygame.draw.rect(tela, PRETO, plataforma)
    for plataforma in plataformas_solidas:
        pygame.draw.rect(tela, PRETO, plataforma)
    for parede in paredes:
        pygame.draw.rect(tela, PRETO, parede)
    pygame.display.update()
pygame.quit()
