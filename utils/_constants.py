import pygame


class Constants:
	DISPLAY_SIZE = 0, 0
	DISPLAY_RECT = pygame.Rect((0, 0), (0, 0))
	FORCE_GLITCH_SHADER = False

	def glitch(self):
		self.FORCE_GLITCH_SHADER = True

	def unglitch(self):
		self.FORCE_GLITCH_SHADER = False
