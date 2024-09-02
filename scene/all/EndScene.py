import pygame

from elements.Attributes import FontSettings, PulseSettings, SpriteAnimation
from elements.Elements import PulsingText, TextDisplay, Sprite
from elements.Types import ElementGroup
from game import challenge_manager
from providers import ColorProvider, SpriteProvider
from scene import Scene


class EndScene(Scene):

	def __init__(self):
		super().__init__()

		logo = Sprite(
			SpriteAnimation(SpriteProvider.get("HoneyPot_Logo_NOBG_Centered.png"), [1], [60], (1051, 1138))
		).set_relative_height(0.33).set_anchor("center").set_relative_pos((0.5, 0.3))
		self.add_element(logo)

		qr_code = Sprite(
			SpriteAnimation(SpriteProvider.get("HoneyPot_QR_Discord.png"), [1], [60], (485, 485))
		).set_relative_height(0.33).set_anchor("midright").set_relative_pos((0.9, 0.3))
		self.add_element(qr_code)
		# Logo goes till 0.3 + 0.33/2 = 0.3 + 0.165 = 0.435

		self.time_out_text = TextDisplay(FontSettings("resources/fonts/Start.otf", 95, ColorProvider.get("fg"))).set_content("Time Out !")
		self.points_display = PulsingText(FontSettings("resources/fonts/Start.otf", 95, ColorProvider.get("fg"))).set_content("Résultat : 0 points")
		self.points_prompt = ElementGroup([self.time_out_text, self.points_display]).set_relative_height(0.18).set_relative_width(1)

		self.time_out_text.set_anchor("midtop").set_relative_height(0.45).set_relative_pos((0.5, 0))
		self.points_display.set_anchor("midbottom").set_pulse_settings(PulseSettings(0.75, 0.2, (0.95, 0.95))).set_relative_height(0.45).set_relative_pos((0.5, 1))

		self.add_element(self.points_prompt.set_anchor("midtop").set_relative_pos((0.5, 0.75)))

	def on_set_active(self):
		self.points_display.set_content(f"Résultat : {challenge_manager.recompute_points():.0f} points")
