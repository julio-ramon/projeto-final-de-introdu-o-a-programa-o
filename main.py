import pygame

#tamanho da tela

LARGURA , ALTURA = 1000, 700

#cores 

AZUL = (100, 149, 237)
PRETO = (0 , 0 , 0)
VERDE = (0 ,100, 0)

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
velocidade1_y = 0
no_chao1 = True
na_plataforma = False

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
        if na_plataforma:
            personagem1_y += 2
            na_plataforma = False
            no_chao1 = False

    movimento_x = (
        int(teclas[pygame.K_RIGHT]) - int(teclas[pygame.K_LEFT])
    ) * VELOCIDADE_MOVIMENTO
    personagem1_x += movimento_x

   
    retangulo_personagem = pygame.Rect(
        personagem1_x, personagem1_y, *TAMANHO_PERSONAGENS
    )
    for obstaculo in plataformas_solidas + paredes:
        if retangulo_personagem.colliderect(obstaculo):
            if movimento_x > 0:
                personagem1_x = obstaculo.left - TAMANHO_PERSONAGENS[0]
            elif movimento_x < 0:
                personagem1_x = obstaculo.right
            retangulo_personagem.x = personagem1_x

    y_anterior1 = personagem1_y
    personagem1_y += velocidade1_y
    velocidade1_y += GRAVIDADE
    no_chao1 = False
    na_plataforma = False

    if personagem1_y >= CHAO:
        personagem1_y = CHAO
        velocidade1_y = 0
        no_chao1 = True

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
            na_plataforma = True

    for obstaculo in plataformas_solidas + paredes:
        sobrepoe_horizontalmente = (
            personagem1_x + TAMANHO_PERSONAGENS[0] > obstaculo.left
            and personagem1_x < obstaculo.right
        )
        if not sobrepoe_horizontalmente:
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
            
    
    

    pygame.draw.rect(tela,PRETO, (personagem1_x, personagem1_y, *TAMANHO_PERSONAGENS))
    pygame.draw.rect(tela, VERDE, (0, TOPO_CHAO, LARGURA, ALTURA_DO_CHAO))
    for plataforma in plataformas:
        pygame.draw.rect(tela, PRETO, plataforma)
    for plataforma in plataformas_solidas:
        pygame.draw.rect(tela, PRETO, plataforma)
    for parede in paredes:
        pygame.draw.rect(tela, PRETO, parede)
    pygame.display.update()
pygame.quit()
