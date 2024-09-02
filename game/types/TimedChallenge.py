from typing import Union

from elements.Attributes import FontSettings, PulseSettings, SpriteAnimation
from elements.Elements import Timer, TextDisplay, PulsingText, ChallengeInterface, Button
from game import Challenge
from providers import ColorProvider, SpriteProvider


class TimedChallenge(Challenge):

	def __init__(self, chall_id: int, name: str, description: str, category: str, difficulty: int, container: ChallengeInterface, end_msg: Union[str, None], **kwargs):
		super().__init__(chall_id, name, description, category, difficulty, container, end_msg)
		self.timer_display = Timer(FontSettings("resources/fonts/Code.ttf", 30, ColorProvider.get('fg')), clock=kwargs.get('clock', 60)).as_countdown()
		self.timer_display.on('timer_end', lambda: self.end(None))

	def get_timer(self) -> Timer:
		return self.timer_display

	def start_challenge(self):
		super().start_challenge()
		self.get_container().add_element(self.get_timer(), True)
		self.get_timer().set_anchor("topright").set_relative_pos((0.99, 0.01))

	def reset_challenge(self):
		super().reset_challenge()
		self.get_timer().reset().pause()

	def start_timer(self):
		self.get_timer().start()

	def display_result(self, completed: bool, improved: bool):
		super().display_result(completed, improved)
		font = FontSettings("resources/fonts/Code.ttf", 75, ColorProvider.get('fg'))
		field_text = TextDisplay(font, content="Temps Max\n\nTemps Restant\n\nScore").set_holder(self.get_container()).set_anchor("midleft")
		field_text.set_relative_pos((0, 0.1)).set_relative_height(0.4).move((self.RESULT_LEFT_MARGIN, 0.85 * field_text.height))
		str_result = f"{self.get_timer().get_passed_time():.2f} sec." if completed else "/"
		value_text = TextDisplay(font, content=f": {self.get_timer().get_initial_time():.2f} sec.\n\n: {self.get_timer().get_time():.2f} sec.\n\n: {str_result}").set_holder(self.get_container()).set_anchor("midright")
		value_text.set_relative_pos((1, 0.1)).set_relative_height(0.4).move((-self.RESULT_LEFT_MARGIN, 0.85 * field_text.height))

		if completed and improved:
			extra_text = PulsingText(font.copy().set_color(ColorProvider.get('success')), content="NEW BEST TIME !").set_holder(self.get_container()).set_anchor("midbottom")
			extra_text.set_pulse_settings(PulseSettings(0.65, 0.2, (0.9, 0.9)))
		else:
			extra_text = PulsingText(font.copy().set_color(ColorProvider.get('failure')), content=("TIME OUT..." if not completed else "TOO SLOW...")).set_holder(self.get_container()).set_anchor("midbottom")
			extra_text.set_pulse_settings(PulseSettings(0.75, 0.1, (0.95, 0.95)))
		extra_text.set_relative_pos((0.5, 0.85))

		self.get_container().add_element(field_text, True)
		self.get_container().add_element(value_text, True)
		self.get_container().add_element(extra_text, True)

