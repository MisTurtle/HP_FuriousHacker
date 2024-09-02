from typing import Union

from elements.Attributes import FontSettings, SpriteAnimation, PulseSettings
from elements.Elements import ChallengeCard, TextDisplay, Button, ChallengeInterface, PulsingText
from providers import ColorProvider, SpriteProvider


class Challenge:

	DIFFICULTY_MULTIPLIER = 0.2
	RESULT_LEFT_MARGIN = 30  # px

	def __init__(self, chall_id: int, name: str, description: str, category: str, difficulty: int, container: ChallengeInterface, end_msg: Union[str, None]):
		self._id = chall_id
		self._name = name
		self._description = description
		self._difficulty = difficulty
		self._container = container
		self._category = category
		self.title_display = None
		self.result = None
		self.card = None
		self.fully_completed = False
		self.end_msg = end_msg
		
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

	def get_result(self) -> Union[float, None]:
		return self.result

	def get_result_str(self) -> str:
		if self.get_result() is None:
			return "N/A"
		return f"{self.get_result():.2f}"

	def get_container(self) -> ChallengeInterface:
		return self._container

	def get_end_msg(self) -> str:
		return self.end_msg

	def is_fully_completed(self) -> bool:
		return self.fully_completed

	def set_fully_completed(self):
		self.fully_completed = True

	def compute_score(self, result: Union[None, float]) -> float:
		if result is None:
			return 0
		if not 0 <= result <= 1:
			print("[Alert] Result isn't in the [0;1] range")

		def f(x):
			return (1.588 * x - 0.5 ** (1/3)) ** 3 + 0.5
		# print(result, f(result), 1000 * f(result))
		return round(min(1, f(result)) * 1000 * (1 + self.DIFFICULTY_MULTIPLIER * (self.get_difficulty() - 1)))

	def improves(self, result: float) -> bool:
		return self.result is None or self.compute_score(result) >= self.compute_score(self.result)

	def set_result(self, result: float):
		"""
		Only call this once "improves" has been checked
		"""
		self.result = result

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
		Challenge.restart_btn.set_click_callback(lambda: self.start_challenge())

		def close_handler():
			self.reset_challenge()
			self.get_container().close()

		self.get_container().add_element(Challenge.close_btn, True)
		Challenge.close_btn.set_anchor("center").set_relative_pos((0.5, 0.95)).set_click_callback(close_handler).set_relative_width(0.25)

	def hide_close_btn(self):
		self.get_container().rm_element(Challenge.close_btn, True)

	def reset_challenge(self):
		pass

	def end(self, result: Union[None, float]):
		improved = False
		# print("New Result : ", result, ":", self.compute_score(result), "\nPrev. Result : ", self.result, self.compute_score(self.result) if self.result is not None else 0)
		if result is not None and self.improves(result):
			self.set_result(result)
			improved = True
			if result >= 1:
				self.set_fully_completed()

		self.display_result(result is not None, improved)

	def display_result(self, completed: bool, improved: bool):
		self.get_container().clear_elements(True)
		self.create_title()
		self.get_container().add_element(Challenge.close_btn, True)
		Challenge.close_btn.set_anchor("midbottom").set_relative_width(0.33)

		if not self.is_fully_completed():
			self.get_container().add_element(Challenge.restart_btn, True)
			Challenge.close_btn.set_relative_pos((0.75, 0.95))
			Challenge.restart_btn.set_anchor("midbottom").set_relative_width(0.33).set_relative_pos((0.25, 0.95))
		else:
			Challenge.close_btn.set_relative_pos((0.5, 0.95))

		if self.end_msg is not None:
			text = PulsingText(FontSettings("resources/fonts/Code.ttf", 35, ColorProvider.get("success")), content=self.end_msg).set_pulse_settings(PulseSettings(0.65, 0.2, (0.9, 0.9)))
			self.get_container().add_element(text, True)
			text.set_max_width(int(0.95 * self.get_container().width)).set_relative_height(0.05).set_anchor("center").set_relative_pos((0.5, 0.5))


Challenge.close_btn = Button(SpriteAnimation(SpriteProvider.get("Btn_Fermer.png"), [1], [64], (570, 60)), on_click=lambda: None)
Challenge.restart_btn = Button(SpriteAnimation(SpriteProvider.get("Btn_Restart.png"), [1], [64], (570, 60)), on_click=lambda: None)
