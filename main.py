import pygame

#tamanho da tela
LARGURA , ALTURA = 600, 300

#cores 
AZUL = (100, 149, 237)
PRETO = (0 , 0 , 0)


#constantes do jogo
FPS = 60
GRAVIDADE = 0.5
TAMANHO_PERSONAGENS = (20 , 50)
ALTURA_DO_PULO = -10
chao = ALTURA - TAMANHO_PERSONAGENS[1]

#inicialização 
pygame.init() 
tela = pygame.display.set_mode((LARGURA , ALTURA))
pygame.display.set_caption("Jogo de Plataforma Multiplayer")
pygame.font.SysFont("Arial",36)
relogio = pygame.time.Clock()

#variaveis do jogo
personagem1_x = 0
personagem1_y = chao
velocidade1_y = 0
no_chao1 = True

rodando = True

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

    personagem1_y += velocidade1_y
    velocidade1_y += GRAVIDADE
    
    if personagem1_y >= chao:
        personagem1_y = chao
        velocidade1_y = 0
        no_chao1 = True

    pygame.draw.rect(tela,PRETO, (personagem1_x, personagem1_y, *TAMANHO_PERSONAGENS))
    pygame.display.update()
pygame.quit()