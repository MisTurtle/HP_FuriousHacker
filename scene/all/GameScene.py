from typing import Union

from elements.Attributes import FontSettings, Animation
from elements.Elements import ChallengeCard, Timer, TextDisplay, ChallengeInterface
from elements.Types import ElementGroup
from game import Challenge, challenge_manager
from providers import ColorProvider
from scene import Scene, scene_manager
from utils import C


class GameScene(Scene):

	challenge_interface: ChallengeInterface = None
	global_countdown: Timer = None
	active_challenge: Union[Challenge, None] = None

	def __init__(self):
		super().__init__()

		# Create Timer
		self.points_display = TextDisplay(FontSettings("resources/fonts/Start.otf", 95, ColorProvider.get("fg"))).set_content("Points : 0.00")
		self.global_countdown = Timer(FontSettings("resources/fonts/Code.ttf", 65, ColorProvider.get("fg")), clock=600).as_countdown().start()
		group = ElementGroup([self.points_display, self.global_countdown])
		group.set_anchor("center").set_relative_pos((0.5, 0.5))
		self.points_display.set_relative_pos((0.5, 0.5)).move((0, - int(self.points_display.height / 2)))
		self.global_countdown.set_relative_pos((0.5, 0.5)).move((0, int(self.points_display.height / 2)))
		self.add_element(group)

		group_size = group.compute_size_from_components(group.get_elements())
		group.set_original_size(((group_size[2] - group_size[0]), group_size[3] - group_size[1]))

		self.challenge_interface = ChallengeInterface([]).set_background_color(ColorProvider.get("bg"))
		self.global_countdown.on("timer_end", lambda _: scene_manager.set_active_scene(scene_manager.END_SCENE))

	def start_challenge(self, chall: Challenge):
		if self.active_challenge is not None:
			return

		for el in self.get_elements():
			if isinstance(el, ChallengeCard):
				el.set_enabled(False)
				el.get_start_button().set_enabled(False)
		self.add_element(self.challenge_interface)

		def anim_end_behavior(anim: Animation):
			anim.pause()
			chall.start_challenge()

		self.challenge_interface.get_animation("entry").reset().start().set_end_behavior(anim_end_behavior)
		self.challenge_interface.set_anchor("center").set_relative_pos((0.5, 0.5))
		self.active_challenge = chall

	def stop_challenge(self):
		self.rm_element(self.challenge_interface)
		for el in self.get_elements():
			if isinstance(el, ChallengeCard):
				if el.challenge == self.active_challenge:
					el.refresh_text()
					if el.get_challenge().is_fully_completed():
						el.on_fully_completed()
						continue
				el.set_enabled(True)
				el.get_start_button().set_enabled(True)
		self.points_display.set_content("Points : " + f"{challenge_manager.recompute_points():.2f}")
		self.active_challenge = None

