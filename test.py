import pygame

# Initialize Pygame
pygame.init()

# Get the list of available fonts
fonts = pygame.font.get_fonts()

# Display the fonts
print("Available fonts:")
for font in fonts:
    print(font)

# Quit Pygame
pygame.quit()
