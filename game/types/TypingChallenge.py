from typing import Union

from elements.Attributes import FontSettings
from elements.Elements import TextArea, ChallengeInterface
from game import Challenge
from game.types.TimedChallenge import TimedChallenge
from providers import ColorProvider


class TypingChallenge(TimedChallenge):

	PERFECT_WPM = 65
	WORD_LENGTH = 5

	def __init__(self, chall_id: int, name: str, description: str, difficulty: int, container: ChallengeInterface, end_msg: Union[str, None], **kwargs):
		super().__init__(chall_id, name, description, difficulty, container, end_msg, **kwargs)
		self.text_area = TextArea(FontSettings("resources/fonts/JetBrainsMono-Medium.ttf", 22, ColorProvider.get('fg')), pattern=kwargs.get('text'), pattern_color=ColorProvider.get('placeholder'))

		# Time to get below or equal to get a perfect score
		self.perfect_min_time = (len(self.text_area.get_pattern()) / self.WORD_LENGTH) * 60 / self.PERFECT_WPM

		self.text_area.on("type", lambda _: (self.start_timer(), self.show_restart_btn()) if self.text_area.get_content().__len__() == 1 else None)
		self.text_area.on("type", lambda _: self.text_area.shake(6, 0.1))
		self.text_area.on("text_complete", lambda _: self.end(min(1., self.perfect_min_time / self.get_timer().get_passed_time())))

	def get_result_str(self) -> str:
		if self.result is None:
			return "0/" + str(self.PERFECT_WPM) + " wpm"
		return f"{self.result * self.PERFECT_WPM:.0f}/{self.PERFECT_WPM} wpm"

	def reset_challenge(self):
		super().reset_challenge()
		self.text_area.reset()

	def show_restart_btn(self):
		self.get_container().add_element(Challenge.restart_btn, True)
		Challenge.close_btn.set_anchor("midbottom").set_relative_width(0.25).set_relative_pos((0.7, 0.95))
		Challenge.restart_btn.set_anchor("midbottom").set_relative_width(0.25).set_relative_pos((0.3, 0.95))

	def start_challenge(self):
		super().start_challenge()
		self.get_container().add_element(self.text_area, True)
		self.text_area.set_max_width(int(0.8 * self.get_container().width)).set_anchor("midleft").set_relative_pos((0.1, 0.5))
