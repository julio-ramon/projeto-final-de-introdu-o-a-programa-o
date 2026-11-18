import pygame

#tamanho da tela

LARGURA , ALTURA = 1000, 700

#cores 

AZUL = (100, 149, 237)
PRETO = (0 , 0 , 0)
VERDE = (0 ,100, 0)

#constantes do jogo

FPS = 60
GRAVIDADE = 0.5
TAMANHO_PERSONAGENS = (20 , 50)
ALTURA_DO_PULO = -10
ALTURA_DO_CHAO = 30
CHAO = ALTURA - TAMANHO_PERSONAGENS[1] - ALTURA_DO_CHAO
PAREDE_E = 0
PAREDE_D = LARGURA - TAMANHO_PERSONAGENS[0]
TETO = ALTURA

#funções
def criar_plataforma(x, y, largura, altura):
    return pygame.Rect(x, y, largura, altura)


# Adicione plataformas nesta lista: (x, y, largura, altura).
plataformas = [
    criar_plataforma(500, CHAO - 40, 50, 5),
    criar_plataforma(300,CHAO - 40, 100,5 )
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
            
    if teclas[pygame.K_RIGHT]:
        personagem1_x += 5

    if teclas[pygame.K_LEFT]:
        personagem1_x -= 5 

    y_anterior1 = personagem1_y
    personagem1_y += velocidade1_y
    velocidade1_y += GRAVIDADE
    no_chao1 = False

    if personagem1_y >= CHAO:
        personagem1_y = CHAO
        velocidade1_y = 0
        no_chao1 = True

    if personagem1_x <= PAREDE_E:
        personagem1_x = PAREDE_E

    if personagem1_x >= PAREDE_D:
        personagem1_x = PAREDE_D

    # Colisão com o topo de qualquer plataforma ao cair.
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
    
    

    pygame.draw.rect(tela,PRETO, (personagem1_x, personagem1_y, *TAMANHO_PERSONAGENS))
    pygame.draw.rect(tela, VERDE ,( 0 , ALTURA - ALTURA_DO_CHAO, *(LARGURA, ALTURA_DO_CHAO )))
    for plataforma in plataformas:
        pygame.draw.rect(tela, PRETO, plataforma)
    pygame.display.update()
pygame.quit()