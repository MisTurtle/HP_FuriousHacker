import pygame

from elements.Attributes import FontSettings, PulseSettings, SpriteAnimation
from elements.Elements import PulsingText, TextDisplay, Sprite
from elements.Types import ElementGroup
from game import challenge_manager
from providers import ColorProvider, SpriteProvider
from scene import Scene
from utils import C


class EndScene(Scene):

	def __init__(self):
		super().__init__()

		logo = Sprite(
			SpriteAnimation(SpriteProvider.get("HoneyPot_Logo_NOBG_Centered.png"), [1], [60], (1051, 1138))
		).set_relative_width(0.20).set_anchor("center").set_relative_pos((0.5, 0.3))
		self.add_element(logo)

		qr_code = Sprite(
			SpriteAnimation(SpriteProvider.get("DISCORD_QR_CODE.png"), [1], [60], None)
		).set_relative_width(0.20).set_anchor("center").set_relative_pos((0.85, 0.3))
		self.add_element(qr_code)

		self.time_out_text = TextDisplay(FontSettings("resources/fonts/PurpleSmile-Regular.otf", 75, ColorProvider.get("fg"))).set_content("C'est fini !")
		self.points_display = PulsingText(FontSettings("resources/fonts/PurpleSmile-Regular.otf", 75, ColorProvider.get("fg"))).set_content("0/0 preuves trouvées !")
		self.points_prompt = ElementGroup([self.time_out_text, self.points_display]).set_relative_height(0.18).set_relative_width(1)

		self.time_out_text.set_anchor("midtop").set_relative_height(0.45).set_relative_pos((0.5, 0))
		self.points_display.set_anchor("midbottom").set_pulse_settings(PulseSettings(0.75, 0.2, (0.95, 0.95))).set_relative_height(0.45).set_relative_pos((0.5, 1))

		self.add_element(self.points_prompt.set_anchor("midtop").set_relative_pos((0.5, 0.75)))

	def on_set_active(self):
		self.points_display.set_content(f"{challenge_manager.get_completed_challs()}/{challenge_manager.get_challenge_count()} preuves trouvées ({challenge_manager.get_points()} points) !")
		C.unglitch()
