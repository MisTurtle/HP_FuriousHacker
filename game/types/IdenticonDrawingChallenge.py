from typing import Union

import pygame

from elements.Attributes import SpriteAnimation, FontSettings, PulseSettings
from elements.Elements import ChallengeInterface, DrawingGrid, Button, TextDisplay, PulsingText
from game import Challenge
from providers import ColorProvider, SpriteProvider


class IdenticonDrawingChallenge(Challenge):

	def __init__(self, chall_id: int, name: str, description: str, difficulty: int, container: ChallengeInterface, end_msg: Union[str, None], statement: str, answer: list[list[bool]]):
		super().__init__(chall_id, name, description, difficulty, container, end_msg)
		self.answer = answer
		self.statement = TextDisplay(FontSettings("resources/fonts/Start.otf", 35, ColorProvider.get("fg")), content=statement)
		self.grid = DrawingGrid((5, 5), hover_color=ColorProvider.get('placeholder'), filled_color=pygame.Color(255, 255, 255), empty_color=ColorProvider.get("bg"), border_color=ColorProvider.get("fg2"))
		self.submit_btn = Button(SpriteAnimation(SpriteProvider.get("Btn_Submit.png"), [1], [64], (570, 60)), on_click=self.submit)

	def submit(self):
		if self.grid.compare(self.answer):
			self.grid.blink(ColorProvider.get("success"), lambda: self.end(1))
		else:
			self.grid.blink(ColorProvider.get("error"), None)

	def get_result_str(self) -> str:
		return "PARFAIT !" if self.is_fully_completed() else "N/A"

	def start_challenge(self):
		if self.is_fully_completed():
			return self.end(1)
		super().start_challenge()
		self.get_container().add_element(self.statement, True)
		self.get_container().add_element(self.grid, True)
		self.get_container().add_element(self.submit_btn, True)
		self.grid.set_anchor("center").set_relative_pos((0.5, 0.5)).set_relative_height(0.5)
		self.statement.set_max_width(int(self.get_container().width * 0.95)).set_anchor("midbottom").set_relative_pos((0.5, 0.5)).move((0, -self.grid.height / 2 - 20))
		self.submit_btn.set_anchor("center").set_relative_width(0.25).set_relative_pos((0.5, 0.95)).move((0, -Challenge.close_btn.height * 1.1))

	def display_result(self, completed: bool, improved: bool):
		super().display_result(completed, improved)
		text = PulsingText(FontSettings("resources/fonts/Code.ttf", 35, ColorProvider.get("success")), content="Openly Intelligent ^_^").set_pulse_settings(PulseSettings(0.65, 0.2, (0.9, 0.9)))
		self.get_container().add_element(text, True)
		text.set_relative_height(0.05).set_anchor("center").set_relative_pos((0.5, 0.5))
