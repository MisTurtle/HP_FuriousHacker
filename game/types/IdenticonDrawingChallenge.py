from typing import Union

import pygame

from elements.Attributes import SpriteAnimation, FontSettings, PulseSettings
from elements.Elements import ChallengeInterface, DrawingGrid, Button, TextDisplay, PulsingText
from game import Challenge
from providers import ColorProvider, SpriteProvider
from utils import C


class IdenticonDrawingChallenge(Challenge):

	def __init__(self, chall_id: int, name: str, description: str, category: str, difficulty: int, container: ChallengeInterface, end_msg: Union[str, None], statement: str, answer: list[list[bool]]):
		super().__init__(chall_id, name, description, category, difficulty, container, end_msg)
		self.answer = answer
		self.statement = TextDisplay(FontSettings("resources/fonts/PurpleSmile-Regular.otf", 35, ColorProvider.get("fg")), content=statement)
		self.grid = DrawingGrid((5, 5), hover_color=ColorProvider.get('placeholder'), filled_color=pygame.Color(255, 255, 255), empty_color=ColorProvider.get("bg"), border_color=ColorProvider.get("fg2"))
		self.submit_btn = Button(SpriteAnimation(SpriteProvider.get("Btn_Submit.png"), [1], [64], (570, 60)), on_click=self.submit)

	def submit(self):
		if self.grid.compare(self.answer):
			self.grid.blink(ColorProvider.get("success"), lambda: self.display_result())
		else:
			self.grid.blink(ColorProvider.get("error"), None)

	def start_challenge(self):
		super().start_challenge()
		self.get_container().add_element(self.statement, True)
		self.get_container().add_element(self.grid, True)
		self.get_container().add_element(self.submit_btn, True)
		self.grid.set_anchor("center").set_relative_pos((0.5, 0.5)).set_relative_height(0.5)

		self.statement.set_relative_height(0.13).set_anchor("midtop").set_relative_pos((0.5, 0.1))
		if self.statement.width > 0.9 * C.DISPLAY_SIZE[0]:
			self.statement.set_relative_width(0.9)

		self.submit_btn.set_anchor("midtop").set_relative_height(0.04).set_relative_pos((0.5, 0.90))
