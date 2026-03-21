import pygame

pygame.init()

print("Setup Started")
window = pygame.display.set_mode(size=(600, 480)) #criando janela do jogo
pygame.display.set_caption("Garden of Fruits") #definindo o título da janela
pygame.display.set_icon(pygame.image.load("assets/frutas/cherry.png"))

print("Setup Finished")

print("Game Started")
while True:
  # Check for all events
  for event in pygame.event.get():
    # If the event is of type QUIT then exit the game
    if event.type == pygame.QUIT:
      pygame.quit() # fecha a janela do jogo
      quit() #termina o processo do jogo
      