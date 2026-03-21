import pygame
import random
import sys
import math

# --- INICIALIZAÇÃO ---
pygame.init()
pygame.mixer.init() # Inicializa o sistema de som

LARGURA, ALTURA = 600, 800
window = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pomar da Kado!")
pygame.display.set_icon(pygame.image.load("assets/frutas/ruby.png"))
clock = pygame.time.Clock()

# --- CAMADAS DE ESCURECIMENTO ---
overlay_menu = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
overlay_menu.fill((0, 0, 0, 160)) 

overlay_jogo = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
overlay_jogo.fill((0, 0, 0, 80)) 

# --- FONTES ---
fonte_titulo = pygame.font.SysFont("segoe ui", 50, bold=True) 
fonte_padrao = pygame.font.SysFont("Arial", 30, bold=True)
fonte_pequena = pygame.font.SysFont("Arial", 20, bold=True)

# --- ÁUDIO ---
# Música de fundo (carrega e toca em loop)
pygame.mixer.music.load("assets/sons/musica_fundo.mp3") 
pygame.mixer.music.set_volume(0.4) # Volume de 0.0 a 1.0
pygame.mixer.music.play(-1) # O -1 faz a música recomeçar sempre que acabar

# Efeitos sonoros
som_bomba = pygame.mixer.Sound("assets/sons/bomba.wav")
som_bomba.set_volume(0.6)

# Se você tiver um som para fruta, pode adicionar aqui também:
# som_fruta = pygame.mixer.Sound("assets/sons/fruta.wav")

# --- CARREGAMENTO DE ASSETS ---
def carregar_imagem(caminho, escala=None):
    try:
        img = pygame.image.load(caminho).convert_alpha()
        if escala:
            img = pygame.transform.scale(img, escala)
        return img
    except:
        img = pygame.Surface(escala if escala else (50, 50))
        img.fill((255, 0, 255)) 
        return img

# Assets de Imagem
reacao_normal = carregar_imagem("assets/personagem/neutro.png", (300, 300))
reacao_feliz  = carregar_imagem("assets/personagem/feliz.png", (300, 300))
reacao_triste = carregar_imagem("assets/personagem/triste.png", (300, 300))
personagem_menu_feliz = carregar_imagem("assets/personagem/feliz.png", (400, 400))
personagem_menu_neutro = carregar_imagem("assets/personagem/neutro.png", (400, 400))
personagem_perdeu = carregar_imagem("assets/personagem/triste.png", (450, 450))
img_fundo = carregar_imagem("assets/background.jpeg", (LARGURA, ALTURA))

# --- CLASSES ---

class Cesto(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img_v1 = carregar_imagem("assets/cesto/cestonaopegou.png", (100, 60))
        self.img_v2 = carregar_imagem("assets/cesto/cestopegouCerto.png", (100, 60))
        self.image = self.img_v1
        self.rect = self.image.get_rect()
        self.rect.centerx = LARGURA // 2
        self.rect.bottom = ALTURA - 30
        self.velocidade = 12
        self.timer_mudanca = 0

    def reagir(self):
        self.timer_mudanca = 15

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT] and self.rect.right < LARGURA:
            self.rect.x += self.velocidade
        
        if self.timer_mudanca > 0:
            self.image = self.img_v2
            self.timer_mudanca -= 1
        else:
            self.image = self.img_v1

class Item(pygame.sprite.Sprite):
    def __init__(self, tipo):
        super().__init__()
        self.tipo = tipo
        self.tamanho_base = 60
        if tipo == "bomba":
            self.image_original = carregar_imagem("assets/bomba/bomba.png", (self.tamanho_base, self.tamanho_base))
        else:
            frutas = ["assets/frutas/cherry.png", "assets/frutas/apple.png", "assets/frutas/pear.png"]
            self.image_original = carregar_imagem(random.choice(frutas), (self.tamanho_base, self.tamanho_base))
            
        self.image = self.image_original
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, LARGURA - 50)
        self.rect.y = -100
        self.velocidade = random.randint(6, 11)
        self.offset_animacao = random.uniform(0, 10)

    def update(self):
        self.rect.y += self.velocidade
        if self.tipo == "bomba":
            tempo = pygame.time.get_ticks() * 0.01 + self.offset_animacao
            escala = 1.0 + math.sin(tempo) * 0.15
            novo_tam = int(self.tamanho_base * escala)
            centro_atual = self.rect.center
            self.image = pygame.transform.smoothscale(self.image_original, (novo_tam, novo_tam))
            self.rect = self.image.get_rect(center=centro_atual)

        if self.rect.top > ALTURA:
            self.kill()
            return True
        return False

# --- FUNÇÕES DE TELA ---

def tela_inicial():
    esperando = True
    while esperando:
        window.blit(img_fundo, (0, 0)) 
        window.blit(overlay_menu, (0, 0)) 
        tempo = pygame.time.get_ticks()

        texto_titulo = fonte_titulo.render("POMAR DA KADO", True, (255, 50, 50))
        window.blit(texto_titulo, texto_titulo.get_rect(center=(LARGURA//2, 100)))
        
        img_atual = personagem_menu_feliz if (tempo // 500) % 2 == 0 else personagem_menu_neutro
        window.blit(img_atual, img_atual.get_rect(center=(LARGURA//2, ALTURA//2)))
        
        escala_pulso = 1.0 + math.sin(tempo * 0.005) * 0.1 
        texto_base = fonte_padrao.render("Pressione ESPAÇO para iniciar", True, (0, 255, 0))
        w, h = texto_base.get_size()
        texto_pulso = pygame.transform.smoothscale(texto_base, (int(w * escala_pulso), int(h * escala_pulso)))
        window.blit(texto_pulso, texto_pulso.get_rect(center=(LARGURA//2, ALTURA//2 + 200)))
        
        texto_setas = fonte_pequena.render("Use as SETAS [←] [→] para mover", True, (200, 200, 200))
        window.blit(texto_setas, texto_setas.get_rect(center=(LARGURA//2, ALTURA - 60)))
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: esperando = False
        clock.tick(60)

def tela_game_over(pontos_finais):
    esperando = True
    while esperando:
        window.blit(img_fundo, (0, 0))
        window.blit(overlay_menu, (0, 0))
        
        texto_perdeu = fonte_titulo.render("VOCÊ PERDEU!", True, (255, 50, 50))
        window.blit(texto_perdeu, texto_perdeu.get_rect(center=(LARGURA//2, 100)))
        
        window.blit(personagem_perdeu, personagem_perdeu.get_rect(center=(LARGURA//2, ALTURA//2)))
        
        texto_pts = fonte_padrao.render(f"Pontos totais: {pontos_finais}", True, (255, 255, 255))
        window.blit(texto_pts, texto_pts.get_rect(center=(LARGURA//2, ALTURA//2 + 200)))
        
        texto_voltar = fonte_pequena.render("Pressione ESPAÇO para tentar de novo", True, (200, 200, 200))
        window.blit(texto_voltar, texto_voltar.get_rect(center=(LARGURA//2, ALTURA - 60)))
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: esperando = False
        clock.tick(60)

def jogar():
    pontos = 0
    bombas_pegas = 0
    perdidas = 0
    reacao_atual = reacao_normal
    timer_reacao_p = 0
    todos_sprites = pygame.sprite.Group()
    frutas, bombas = pygame.sprite.Group(), pygame.sprite.Group()
    jogador = Cesto()
    todos_sprites.add(jogador)
    
    rodando = True
    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()

        if random.random() < 0.03: 
            tipo = "bomba" if random.random() < 0.25 else "fruta"
            novo = Item(tipo); todos_sprites.add(novo)
            if tipo == "fruta": frutas.add(novo)
            else: bombas.add(novo)

        for sprite in todos_sprites:
            passou = sprite.update()
            if passou and hasattr(sprite, 'tipo') and sprite.tipo == "fruta": perdidas += 1

        if timer_reacao_p > 0: timer_reacao_p -= 1
        else: reacao_atual = reacao_normal

        # Colisão com frutas
        if pygame.sprite.spritecollide(jogador, frutas, True):
            pontos += 1; reacao_atual = reacao_feliz; timer_reacao_p = 45; jogador.reagir()
            # som_fruta.play() # Caso tenha som de fruta, descomente aqui
            
        # Colisão com bombas
        if pygame.sprite.spritecollide(jogador, bombas, True):
            bombas_pegas += 1; reacao_atual = reacao_triste; timer_reacao_p = 45; jogador.reagir()
            som_bomba.play() # Toca o som da bomba
            if bombas_pegas >= 3: rodando = False

        window.blit(img_fundo, (0, 0))
        window.blit(overlay_jogo, (0, 0))
        todos_sprites.draw(window)
        window.blit(reacao_atual, (20, 20))
        
        window.blit(fonte_padrao.render(f"Frutas: {pontos}", True, (0, 255, 0)), (LARGURA - 280, 40))
        window.blit(fonte_padrao.render(f"Bombas: {bombas_pegas}/3", True, (255, 80, 80)), (LARGURA - 280, 100))
        window.blit(fonte_padrao.render(f"Perdidas: {perdidas}", True, (200, 200, 200)), (LARGURA - 280, 160))

        pygame.display.flip()
        clock.tick(60)
    
    tela_game_over(pontos)
    tela_inicial()
    jogar()

# --- EXECUÇÃO ---
tela_inicial()
jogar()