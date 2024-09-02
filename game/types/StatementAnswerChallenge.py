from typing import Union, Callable

from elements.Attributes import FontSettings, SpriteAnimation
from elements.Elements import ChallengeInterface, TextDisplay, TextArea, Sprite, Button
from game import Challenge
from providers import ColorProvider, SpriteProvider


class StatementAnswerChallenge(Challenge):

	def __init__(self, chall_id: int, name: str, description: str, category: str, difficulty: int, container: ChallengeInterface, end_msg: Union[str, None], statement: str, answer: Union[str, Callable[[str], bool]], hint: Union[None, str], image: Union[None, SpriteAnimation] = None):
		super().__init__(chall_id, name, description, category, difficulty, container, end_msg)
		self.statement_display = TextDisplay(FontSettings("resources/fonts/Start.ttf", 75, ColorProvider.get('fg')), content=statement)
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
		if (self.has_static_answer() and self.text_input.get_content().upper() == self.answer.upper()) or (not self.has_static_answer() and self.answer(self.text_input.get_content())):
			self.text_input.disable().blink(ColorProvider.get("success"), lambda: self.end(1))
		else:
			self.text_input.disable().blink(ColorProvider.get("error"), lambda: (self.text_input.enable(), self.text_input.set_content("")))
		self.text_input.shake(15, 0.25, self.text_input.SHAKE_SMOOTH_IN_OUT)

	def start_challenge(self):
		if self.is_fully_completed():
			return self.end(1)
		super().start_challenge()
		self.get_container().add_element(self.statement_display, True)
		self.get_container().add_element(self.text_input, True)

		if not self.has_static_answer():
			self.get_container().add_element(self.submit_btn, True)
			self.submit_btn.set_anchor("center").set_relative_width(0.25).set_relative_pos((0.5, 0.95)).move((0, -Challenge.close_btn.height * 1.1))

		self.statement_display.set_max_width(int(0.98 * self.get_container().width)).set_relative_width(0.8).set_anchor("center").set_relative_pos((0.5, 0.15))
		if self.statement_display.height > 0.1 * self.get_container().height:
			self.statement_display.set_relative_height(0.1)
		# self.text_input.set_max_width(int(0.98 * self.get_container().width))
		if self.text_input.width > 0.98 * self.get_container().width:
			self.text_input.set_relative_width(0.98)
		self.text_input.set_anchor("center").set_relative_pos((0.5, 0.4))

		if self.image is not None:
			self.get_container().add_element(self.image, True)
			self.image.set_relative_height(0.40).set_anchor("center").set_relative_pos((0.5, 0.65))

	def get_result_str(self) -> str:
		return "PARFAIT !" if self.is_fully_completed() else "N/A"

