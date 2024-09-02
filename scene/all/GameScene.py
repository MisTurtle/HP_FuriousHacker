import math
from typing import Union

import pygame

from elements.Attributes import FontSettings, Animation, TimerTrigger
from elements.Elements import ChallengeCard, Timer, TextDisplay, ChallengeInterface
from elements.Types import ElementGroup
from game import Challenge, challenge_manager
from providers import ColorProvider, ShaderProvider
from scene import Scene, scene_manager
from utils import C


class GameScene(Scene):

	GAME_TIME = 60 * 10 + 3  # seconds

	challenge_interface: ChallengeInterface = None
	global_countdown: Timer = None
	active_challenge: Union[Challenge, None] = None

	def __init__(self):
		super().__init__()

		# Create Timer Text
		self.points_display = TextDisplay(FontSettings("resources/fonts/Start.otf", 95, ColorProvider.get("fg"))).set_content("Points : 0")
		self.global_countdown = Timer(FontSettings("resources/fonts/Code.ttf", 65, ColorProvider.get("fg")), clock=self.GAME_TIME).as_countdown().start()
		self.display_group = ElementGroup([self.points_display, self.global_countdown])
		self.display_group.set_anchor("center").set_relative_pos((0.5, 0.5))
		self.points_display.set_relative_pos((0.5, 0.5)).move((0, - int(self.points_display.height / 2)))
		self.global_countdown.set_relative_pos((0.5, 0.5)).move((0, int(self.points_display.height / 2)))
		self.add_element(self.display_group)

		group_size = self.display_group.compute_size_from_components(self.display_group.get_elements())
		self.display_group.set_original_size(((group_size[2] - group_size[0]), group_size[3] - group_size[1]))

		# Create Challenge Interface
		self.challenge_interface = ChallengeInterface([]).set_background_color(ColorProvider.get("bg"))
		self.global_countdown.on("timer_end", lambda: scene_manager.set_active_scene(scene_manager.END_SCENE))

	def on_set_active(self):
		# Create End Timer Hooks
		emergency_starts = 60  # when timer drops below 60 seconds
		emergency_step_1 = 30
		emergency_step_2 = 15
		shaking_starts = 60
		shaking_level_2 = 30

		def emergency_shader(surface: pygame.Surface):
			if self.global_countdown.get_time() > emergency_step_1:
				period = 0.75
			elif self.global_countdown.get_time() > emergency_step_2:
				period = 0.35
			else:
				period = 0.20
			alpha = 1, 60
			emergency = pygame.Surface(surface.get_size())
			emergency.set_alpha(int(alpha[0] + (alpha[1] - alpha[0]) * (1 + math.cos(self.global_countdown.get_time() / period)) / 2))
			emergency.fill((255, 0, 0))
			surface.blit(emergency, (0, 0))

		self.global_countdown.add_trigger(TimerTrigger(TimerTrigger.DROPS_BELOW, emergency_starts, lambda: ShaderProvider.set("emergency_timer", emergency_shader)))
		self.global_countdown.add_trigger(TimerTrigger(TimerTrigger.DROPS_BELOW, shaking_starts, lambda: self.points_display.shake(5, shaking_starts, self.global_countdown.SHAKE_SMOOTH_IN)))
		self.global_countdown.add_trigger(TimerTrigger(TimerTrigger.DROPS_BELOW, shaking_level_2, lambda: self.global_countdown.shake(5, shaking_level_2, self.global_countdown.SHAKE_SMOOTH_IN)))

	def on_set_inactive(self):
		super().on_set_inactive()
		ShaderProvider.rm("emergency_timer")
		self.global_countdown.clear_triggers()

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
		self.points_display.set_content("Points : " + f"{challenge_manager.recompute_points():.0f}")
		self.active_challenge = None

