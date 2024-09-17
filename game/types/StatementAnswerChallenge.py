from typing import Union, Callable

from elements.Attributes import FontSettings, SpriteAnimation
from elements.Elements import ChallengeInterface, TextDisplay, TextArea, Sprite, Button
from game import Challenge
from providers import ColorProvider, SpriteProvider
from utils import C


class StatementAnswerChallenge(Challenge):

	def __init__(self, chall_id: int, name: str, description: str, category: str, difficulty: int, container: ChallengeInterface, end_msg: Union[str, None], statement: str, answer: Union[str, Callable[[str], bool]], hint: Union[None, str], image: Union[None, SpriteAnimation] = None, case_sensitive: bool = False):
		super().__init__(chall_id, name, description, category, difficulty, container, end_msg)
		self.case_sensitive = case_sensitive
		self.statement_display = TextDisplay(FontSettings("resources/fonts/PurpleSmile-Regular.otf", 65, ColorProvider.get('fg')), content=statement)
		self.text_input = TextArea(
			FontSettings("resources/fonts/Code.ttf", 75, ColorProvider.get('fg')),
			pattern=hint,
			pattern_color=ColorProvider.get('placeholder'),
			require_pattern=False,
			multiline=False,
			blink_mode=TextArea.BLINK_BOTH
		)
		self.answer = answer
		if self.has_static_answer():
			self.text_input.on("type", lambda: self.submit_answer() if len(self.text_input.get_content()) == len(answer) else None)
		else:
			self.submit_btn = Button(SpriteAnimation(SpriteProvider.get("Btn_Submit.png"), [1], [64], (570, 60)), on_click=self.submit_answer)
		self.text_input.on("type", lambda: self.text_input.shake(5, 0.15, self.text_input.SHAKE_INSTANT))

		if image is not None:
			self.image = Sprite(image)
		else:
			self.image = None

	def has_static_answer(self) -> bool:
		return isinstance(self.answer, str)

	def submit_answer(self):
		if self.has_static_answer():
			answer_check = self.text_input.get_content() == self.answer or (not self.case_sensitive and self.text_input.get_content().upper() == self.answer.upper())
		else:
			answer_check = self.answer(self.text_input.get_content())

		if answer_check:
			self.text_input.disable().blink(ColorProvider.get("success"), lambda: self.display_result())
		else:
			self.text_input.disable().blink(ColorProvider.get("error"), lambda: (self.text_input.enable(), self.text_input.set_content("")))
		self.text_input.shake(15, 0.25, self.text_input.SHAKE_SMOOTH_IN_OUT)

	def start_challenge(self):
		super().start_challenge()
		self.get_container().add_element(self.statement_display, True)
		self.get_container().add_element(self.text_input, True)

		if not self.has_static_answer():
			self.get_container().add_element(self.submit_btn, True)
			self.submit_btn.set_anchor("midtop").set_relative_pos((0.5, 0.90)).set_click_callback(self.submit_answer).set_relative_height(0.04)

		# Statement display space occupation in height : Max from 0.1 to 0.23
		self.statement_display.set_relative_height(0.13).set_anchor("midtop").set_relative_pos((0.5, 0.1))
		if self.statement_display.width > 0.9 * C.DISPLAY_SIZE[0]:
			self.statement_display.set_relative_width(0.9)

		# Input display space occupation in height : Max from 0.35 to 0.43
		self.text_input.set_relative_height(0.08).set_anchor("midtop").set_relative_pos((0.5, 0.35))
		if self.text_input.width > 0.9 * C.DISPLAY_SIZE[0]:
			self.text_input.set_relative_width(0.9)

		# Image display space occupation in height : Max from 0.50 to 0.88
		if self.image is not None:
			self.get_container().add_element(self.image, True)
			self.image.set_relative_height(0.38).set_anchor("midtop").set_relative_pos((0.5, 0.5))
			if self.image.width > 0.85 * C.DISPLAY_SIZE[0]:
				self.image.set_relative_width(0.85)
