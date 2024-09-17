import math
import re
from typing import Union

from elements.Attributes import FontSettings, SpriteAnimation
from elements.Elements import ChallengeInterface, TextDisplay, TextArea, Button
from game import Challenge
from providers import ColorProvider, SpriteProvider


class WordMatchingChallenge(Challenge):

	def __init__(self, chall_id: int, name: str, description: str, category: str, difficulty: int, container: ChallengeInterface, end_msg: Union[str, None], word_list: dict[str, str], guideline: str):
		super().__init__(chall_id, name, description, category, difficulty, container, end_msg)
		self.word_count = len(word_list)
		assert self.word_count > 0
		self.statements, self.answers = list(word_list.values()), list(word_list.keys())
		self.current_word = 0
		self.guideline = guideline

		display_font = FontSettings("resources/fonts/Code.ttf", 75, ColorProvider.get('fg'))

		self.statement_display, self.answer_display = TextDisplay(display_font), TextArea(display_font, blink_mode=TextArea.BLINK_BOTH, multiline=False).set_require_pattern(False)

		self.guideline_display = TextDisplay(FontSettings("resources/fonts/PurpleSmile-Regular.otf", 65, ColorProvider.get('fg')), content=guideline).set_anchor("midtop").set_relative_pos((0.5, 0.1)).set_relative_height(0.13)
		if self.guideline_display.width >= self.get_container().width * 0.95:
			self.guideline_display.set_relative_width(0.95)
		self.skip_word_button = Button(SpriteAnimation(SpriteProvider.get("Btn_Skip.png"), frame_count=[1], frame_time=[60], frame_size=None), on_click=lambda: self.skip_word())

		self.answer_display.on("type", lambda: self.submit_answer() if len(self.answer_display.get_content()) == len(self.get_current_tuple()[0]) else None)

	def update_word_guess(self):
		tup = self.get_current_tuple()
		if tup is None:
			self.display_result()
		else:
			self.statement_display.set_zoom((1, 1)).set_content(tup[0]).set_anchor("midbottom").set_relative_pos((0.5, 0.45), self.get_container())
			self.answer_display.set_zoom((1, 1)).set_anchor("center").set_pattern(re.sub(r'[^ ]', '_', tup[1])).set_relative_pos((0.5, 0.45)).move((0, self.answer_display.height))
			if self.answer_display.width >= self.get_container().width * 0.95:
				self.answer_display.set_relative_width(0.95)
			if self.statement_display.width >= self.get_container().width * 0.95:
				self.statement_display.set_relative_width(0.95)
			self.answer_display.set_content("")

	def is_complete(self) -> bool:
		return len(self.statements) == 0

	def skip_word(self):
		if self.is_complete():
			return
		self.current_word += 1
		if self.current_word >= len(self.statements):
			self.current_word = 0
		self.update_word_guess()

	def is_correct(self, guess: str) -> bool:
		return not self.is_complete() and self.answers[self.current_word].upper() == guess.upper()

	def get_current_tuple(self) -> Union[None, tuple[str, str]]:
		if self.is_complete():
			return None
		return self.statements[self.current_word], self.answers[self.current_word]

	def submit_answer(self):
		if self.is_correct(self.answer_display.get_content()):
			self.statements.pop(self.current_word)
			self.answers.pop(self.current_word)
			self.current_word %= (1 if len(self.statements) == 0 else len(self.statements))
			self.answer_display.disable().blink(ColorProvider.get("success"), lambda: (self.answer_display.enable(), self.update_word_guess()))
		else:
			self.answer_display.disable().blink(ColorProvider.get("error"), lambda: self.answer_display.enable().set_content(""))

	def start_challenge(self):
		super().start_challenge()

		self.get_container().add_element(self.statement_display, True)
		self.get_container().add_element(self.answer_display, True)
		self.get_container().add_element(self.skip_word_button, True)
		self.get_container().add_element(self.guideline_display, True)

		self.statement_display.set_anchor("midtop")# .set_max_width(int(self.get_container().width * 0.9))
		self.answer_display.set_anchor("topleft")# .set_max_width(int(self.get_container().width * 0.9))
		self.skip_word_button.set_anchor("center").set_relative_pos((0.5, 0.95)).set_click_callback(lambda: self.skip_word()).set_relative_width(0.25).move((0, -Challenge.close_btn.height * 1.2))
		self.update_word_guess()

	def reset_challenge(self):
		return
