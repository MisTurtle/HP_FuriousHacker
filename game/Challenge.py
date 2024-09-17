from elements.Attributes import FontSettings, SpriteAnimation, PulseSettings
from elements.Elements import ChallengeCard, TextDisplay, Button, PulsingText, ChallengeInterface
from providers import ColorProvider, SpriteProvider
from utils import C


class Challenge:

	RESULT_LEFT_MARGIN = 30  # px

	def __init__(self, chall_id: int, name: str, description: str, category: str, difficulty: int, container: ChallengeInterface, end_msg: str):
		self._id = chall_id
		self._name = name
		self._description = description
		self._difficulty = difficulty
		self._container = container
		self._category = category
		self.title_display = None
		self.card = None
		self.end_msg = end_msg
		self.complete = False
		
	def get_id(self) -> int:
		return self._id

	def get_name(self) -> str:
		return self._name

	def get_description(self) -> str:
		return self._description

	def get_category(self) -> str:
		return self._category

	def get_difficulty(self) -> int:
		return self._difficulty

	def get_container(self) -> ChallengeInterface:
		return self._container

	def get_end_msg(self) -> str:
		return self.end_msg

	def create_card(self) -> ChallengeCard:
		self.card = ChallengeCard(self)
		return self.card

	def create_title(self):
		if self.title_display is None:
			self.title_display = TextDisplay(FontSettings("resources/fonts/Code.ttf", 50, ColorProvider.get("fg")), content=">/" + self.get_name())
		self.get_container().add_element(self.title_display, True)
		self.title_display.set_anchor("midtop").set_relative_pos((0.5, 0.01), self.get_container())

	def start_challenge(self):
		self.get_container().clear_elements(True)
		self.reset_challenge()
		self.create_title()

		def close_handler():
			self.reset_challenge()
			self.get_container().close()

		self.get_container().add_element(Challenge.close_btn, True)
		Challenge.close_btn.set_anchor("midtop").set_relative_pos((0.5, 0.95)).set_click_callback(close_handler).set_relative_height(0.04)

	def hide_close_btn(self):
		self.get_container().rm_element(Challenge.close_btn, True)

	def reset_challenge(self):
		pass

	def is_complete(self) -> bool:
		return self.complete

	def display_result(self):
		# Result is only displayed when the challenge is completed now
		self.get_container().clear_elements(True)
		self.create_title()
		self.get_container().add_element(Challenge.close_btn, True)
		Challenge.close_btn.set_anchor("midbottom").set_relative_width(0.33)

		text = PulsingText(FontSettings("resources/fonts/Code.ttf", 65, ColorProvider.get("success")), content=self.end_msg).set_pulse_settings(PulseSettings(0.65, 0.1, (0.8, 0.8)))
		if text.width > 0.8 * C.DISPLAY_SIZE[0]:
			text.set_relative_width(0.8)
		text.set_anchor("center").set_relative_pos((0.5, 0.5))
		self.get_container().add_element(text, True)
		self.complete = True


Challenge.close_btn = Button(SpriteAnimation(SpriteProvider.get("Btn_Fermer.png"), [1], [64], (570, 60)), on_click=lambda: None)
