import pygame

pygame.init()
LARGURA_TELA = 800
ALTURA_TELA = 600

tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Jogo de Labirinto")
# Cores
BRANCO = (255, 255, 255)    
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
# Configurações do jogador
LARGURA_JOGADOR = 40
ALTURA_JOGADOR = 40
VELOCIDADE_JOGADOR = 5
# Configurações do labirinto
LARGURA_PAREDE = 40 
ALTURA_PAREDE = 40
# Configurações do inimigo
LARGURA_INIMIGO = 40
ALTURA_INIMIGO = 40
VELOCIDADE_INIMIGO = 3
# Configurações do objetivo
LARGURA_OBJETIVO = 40
ALTURA_OBJETIVO = 40
# Configurações do jogo
FPS = 60
clock = pygame.time.Clock()
# Labirinto (1 = parede, 0 = caminho)
labirinto = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],]
labirinto += [[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],]
labirinto += [[1, 0, 1, 1, 1, 1, 1, 1, 0, 1],]
labirinto += [[1, 0, 1, 0, 0, 0, 0, 1, 0, 1],]
labirinto += [[1, 0, 1, 0, 1, 1, 0, 1, 0, 1],]
labirinto += [[1, 0, 1, 0, 1, 1, 0, 1, 0, 1],]
labirinto += [[1, 0, 1, 0, 0, 0, 0, 1, 0, 1],]
labirinto += [[1, 0, 1, 1, 1, 1, 1, 1, 0, 1],]
labirinto += [[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],]
labirinto += [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],]
# Posições iniciais
posicao_jogador = [LARGURA_PAREDE + (LARGURA_PAREDE - LARGURA_JOGADOR) // 2, ALTURA_PAREDE + (ALTURA_PAREDE - ALTURA_JOGADOR) // 2]
posicao_inimigo = [LARGURA_PAREDE * 8 + (LARGURA_PAREDE - LARGURA_INIMIGO) // 2, ALTURA_PAREDE * 8 + (ALTURA_PAREDE - ALTURA_INIMIGO) // 2]
posicao_objetivo = [LARGURA_PAREDE * 8 + (LARGURA_PAREDE - LARGURA_OBJETIVO) // 2, ALTURA_PAREDE + (ALTURA_PAREDE - ALTURA_OBJETIVO) // 2]
# Função para desenhar o labirinto
def desenhar_labirinto():
    for linha in range(len(labirinto)):
        for coluna in range(len(labirinto[linha])):
            if labirinto[linha][coluna] == 1:
                pygame.draw.rect(tela, PRETO, (coluna * LARGURA_PAREDE, linha * ALTURA_PAREDE, LARGURA_PAREDE, ALTURA_PAREDE))
# Função para desenhar o jogador
def desenhar_jogador():
    pygame.draw.rect(tela, AZUL, (posicao_jogador[0], posicao_jogador[1], LARGURA_JOGADOR, ALTURA_JOGADOR))
# Função para desenhar o inimigo
def desenhar_inimigo():    
    pygame.draw.rect(tela, VERMELHO, (posicao_inimigo[0], posicao_inimigo[1], LARGURA_INIMIGO, ALTURA_INIMIGO))
# Função para desenhar o objetivo
def desenhar_objetivo():
    pygame.draw.rect(tela, VERDE, (posicao_objetivo[0], posicao_objetivo[1], LARGURA_OBJETIVO, ALTURA_OBJETIVO))
# Função para verificar colisões
def verificar_colisoes():
    # Colisão com paredes
    for linha in range(len(labirinto)):
        for coluna in range(len(labirinto[linha])):
            if labirinto[linha][coluna] == 1:
                parede_rect = pygame.Rect(coluna * LARGURA_PAREDE, linha * ALTURA_PAREDE, LARGURA_PAREDE, ALTURA_PAREDE)
                jogador_rect = pygame.Rect(posicao_jogador[0], posicao_jogador[1], LARGURA_JOGADOR, ALTURA_JOGADOR)
                if jogador_rect.colliderect(parede_rect):
                    return True
    # Colisão com inimigo
    inimigo_rect = pygame.Rect(posicao_inimigo[0], posicao_inimigo[1], LARGURA_INIMIGO, ALTURA_INIMIGO)
    jogador_rect = pygame.Rect(posicao_jogador[0], posicao_jogador[1], LARGURA_JOGADOR, ALTURA_JOGADOR)
    if jogador_rect.colliderect(inimigo_rect):
        return True
    # Colisão com objetivo
    objetivo_rect = pygame.Rect(posicao_objetivo[0], posicao_objetivo[1], LARGURA_OBJETIVO, ALTURA_OBJETIVO)
    if jogador_rect.colliderect(objetivo_rect):
        return "vitoria"
    return False
  
# Função para mover o inimigo
def mover_inimigo():
    if posicao_inimigo[0] < posicao_jogador[0]:
        posicao_inimigo[0] += VELOCIDADE_INIMIGO
    elif posicao_inimigo[0] > posicao_jogador[0]:
        posicao_inimigo[0] -= VELOCIDADE_INIMIGO
    if posicao_inimigo[1] < posicao_jogador[1]:
        posicao_inimigo[1] += VELOCIDADE_INIMIGO
    elif posicao_inimigo[1] > posicao_jogador[1]:
        posicao_inimigo[1] -= VELOCIDADE_INIMIGO
# Loop principal do jogo
jogo_rodando = True
while jogo_rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogo_rodando = False
    # Movimentação do jogador
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        posicao_jogador[0] -= VELOCIDADE_JOGADOR
    if teclas[pygame.K_RIGHT]:
        posicao_jogador[0] += VELOCIDADE_JOGADOR
    if teclas[pygame.K_UP]:
        posicao_jogador[1] -= VELOCIDADE_JOGADOR
    if teclas[pygame.K_DOWN]:
        posicao_jogador[1] += VELOCIDADE_JOGADOR
    # Verificar colisões
    resultado_colisao = verificar_colisoes()
    if resultado_colisao == True:
        print("Game Over!")
        jogo_rodando = False
    elif resultado_colisao == "vitoria":
        print("Você venceu!")
        jogo_rodando = False
    # Mover inimigo
    mover_inimigo()
    # Desenhar tudo
    tela.fill(BRANCO)
    desenhar_labirinto()
    desenhar_jogador()
    desenhar_inimigo()
    desenhar_objetivo()
    pygame.display.flip()
    clock.tick(FPS)
    
pygame.quit()

