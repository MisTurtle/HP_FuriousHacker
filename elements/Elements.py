import math
import random
import string

import pygame

from typing import Callable, Union, Any
from elements.Attributes import SpriteAnimation, Animation, FontSettings
from elements.Types import SceneElement, Hoverable, Pulsing, ElementGroup, Typable
from game import Challenge
from providers import ColorProvider, SpriteProvider
from scene import scene_manager
from utils import C, point_in_elliptical_disk


class Sprite(SceneElement):

	def __init__(self, spritesheet: SpriteAnimation, **kwargs):
		self.spritesheet = spritesheet
		w, h = self.spritesheet.get_frame_size()
		super().__init__(w, h, **kwargs)

	def get_spritesheet(self) -> SpriteAnimation:
		return self.spritesheet

	def set_spritesheet(self, sheet: SpriteAnimation) -> 'Sprite':
		self.spritesheet = sheet
		return self

	def tick(self, dt: float):
		super().tick(dt)
		self.get_spritesheet().tick(dt)

	def render(self) -> list[pygame.Surface]:
		return [self.spritesheet.extract()]


class TextDisplay(SceneElement):

	def __init__(self, display_settings: FontSettings, **kwargs):
		super().__init__(0, 0, **kwargs)
		self._display_settings = display_settings
		self._content = kwargs.get("content", "")
		self._max_width = -1
		self._word_positions = []
		self._recompute_size()

	def _recompute_size(self) -> 'TextDisplay':
		def _():
			self._word_positions.clear()
			font = self.get_display_settings().get_font()
			word_position = [0, 0]
			final_width, final_height = 0, 0

			for line in self._content.splitlines():
				subline = []
				for word in line.split(" "):
					next_content = " ".join(subline + [word])
					next_size = self.get_display_settings().get_font().size(next_content)[0]
					if next_size > self._max_width > 0:
						# Update word position and append to the list
						word_position[0] = 0
						word_position[1] += font.get_height()
						self._word_positions.append(word_position)

						# Increase text final size
						final_width = self._max_width
						final_height += font.get_height()

						# Reset line content
						subline = [] if len(subline) == 0 else [word]
					else:
						subline.append(word)
						# Append word position to the list and update next word's starting point
						self._word_positions.append(word_position)
						word_position[0] = next_size
						# Update final width
						final_width = max(final_width, next_size)
				final_height += font.get_height()

			self.set_original_size((final_width, final_height))
			self.get_display_settings().clear_dirty()
		self.lock_pos(_)
		return self

	def get_drawing_position(self, surface_id: int) -> tuple[float, float]:
		pos = super().get_drawing_position(surface_id)
		return pos[0], pos[1] + self.get_display_settings().get_font().get_height() * surface_id * self.get_zoom()[1]

	def get_display_settings(self) -> FontSettings:
		return self._display_settings

	def get_content(self) -> str:
		return self._content

	def set_content(self, new: str) -> 'TextDisplay':
		self._content = new
		return self._recompute_size()

	def set_max_width(self, width: int) -> 'TextDisplay':
		self._max_width = width
		self._recompute_size()
		return self

	def get_max_width(self) -> int:
		return self._max_width

	@staticmethod
	def render_text(text: str, font: FontSettings, max_width: int) -> list[pygame.Surface]:
		surfaces = []
		for line in text.splitlines():
			subline = []
			for word in line.split(" "):
				next_content = " ".join(subline + [word])
				next_size = font.get_font().size(next_content)[0]
				if next_size > max_width > 0:
					if len(subline) == 0:  # Support in case a single word takes more space than allocated, draw it anyway (Could split the word but whatever)
						surfaces.append(font.render_line(" ".join([word])))
						subline = []
					else:
						surfaces.append(font.render_line(" ".join(subline)))
						subline = [word]
				else:
					subline.append(word)
			if len(subline) > 0:
				surfaces.append(font.render_line(" ".join(subline)))
		return surfaces

	def render(self) -> list[pygame.Surface]:
		if self.get_display_settings().is_dirty():
			self._recompute_size()
		return self.render_text(self.get_content(), self.get_display_settings(), self._max_width)


class PulsingImage(Sprite, Pulsing):
	pass


class PulsingText(TextDisplay, Pulsing):
	pass


class Button(Hoverable, Sprite):

	HOVER_DURATION = 0.07
	HOVER_AMPLIFY = 0.07
	CLICK_DURATION = 0.19

	def __init__(self, spritesheet: SpriteAnimation, on_click: Callable[[], Any], **kwargs):
		super().__init__(spritesheet, **kwargs)
		self.set_click_callback(on_click)
		self.base_scale = self.get_zoom()
		self.add_animation("hover", Animation(self.HOVER_DURATION).set_end_behavior(Animation.PAUSE_ON_END))
		self.add_animation("click", Animation(self.CLICK_DURATION).set_end_behavior(Animation.RESET_ON_END))

	def set_click_callback(self, handler: Callable[[], Any]) -> 'Hoverable':
		self.clear("click")
		self.on("click", lambda el: el.get_animation("click").start().then(lambda: handler()))
		return self

	def set_relative_width(self, relw: float, keep_ratio: bool = True, holder: Union[pygame.Rect, None] = None) -> 'SceneElement':
		super().set_relative_width(relw, keep_ratio, holder)
		self.base_scale = self.get_zoom()
		return self

	def set_relative_height(self, relh: float, keep_ratio: bool = True, holder: Union[pygame.Rect, None] = None) -> 'SceneElement':
		super().set_relative_height(relh, keep_ratio, holder)
		self.base_scale = self.get_zoom()
		return self

	def on_mouse_enter(self):
		super().on_mouse_enter()
		if self.is_enabled():
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
			self.get_animation("hover").set_speed(1).start()
		else:
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)

	def on_mouse_leave(self):
		super().on_mouse_leave()
		if self.is_enabled():
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
			self.get_animation("hover").reverse().start().then(lambda: self.set_zoom(self.base_scale))

	def tick(self, dt: float):
		super().tick(dt)
		hover_anim = self.get_animation("hover")
		if self.is_hovered() or hover_anim.is_running():
			click_anim = self.get_animation("click")
			if click_anim.is_running():
				scale = self.HOVER_AMPLIFY - self.HOVER_AMPLIFY * math.sin(math.pi * click_anim.get_progress_percent())
			else:
				scale = hover_anim.get_progress_percent() * self.HOVER_AMPLIFY
			self.set_zoom((self.base_scale[0] + scale, self.base_scale[1] + scale))


class BinaryDropText(TextDisplay):

	MIN_DROP_SPEED = 50  # px / s
	MAX_DROP_SPEED = 250  # px / s
	MIN_ZOOM = 0.3
	MAX_ZOOM = 1.2
	MIN_CHAIN_SIZE = 5
	MAX_CHAIN_SIZE = 15

	_coefficient = 0.
	_speed = 0.
	_color_fg = pygame.Color(0, 0, 0)
	_color_bg = pygame.Color(255, 255, 255)

	def __init__(self, display_settings: FontSettings, **kwargs):
		super().__init__(display_settings, **kwargs)
		self.set_anchor("midtop")
		self._color_fg = ColorProvider.get("fg2")
		self._color_bg = ColorProvider.get("bg")
		self.__reset()

	def __reset(self):
		self._coefficient = random.random()
		zoom = self.MIN_ZOOM + self._coefficient * (self.MAX_ZOOM - self.MIN_ZOOM)

		self.set_content("\n".join([f"{random.randint(0, 1)!r}" for _ in range(random.randint(self.MIN_CHAIN_SIZE, self.MAX_CHAIN_SIZE))]))
		self.set_zoom((zoom, zoom))

		self.set_position((random.randint(0, C.DISPLAY_SIZE[0]), -self.height))
		self._speed = (self.MIN_DROP_SPEED + self._coefficient * (self.MAX_DROP_SPEED - self.MIN_DROP_SPEED))

		def cc(_from, _to) -> int:
			return int(_from + (_to - _from) * self._coefficient)

		self.get_display_settings().set_color(pygame.color.Color(
			cc(self._color_bg.r, self._color_fg.r), cc(self._color_bg.g, self._color_fg.g), cc(self._color_bg.b, self._color_fg.b))
		)

	def tick(self, dt: float):
		if self.move((0, self._speed * dt), self.WRAP_Y) & self.WRAP_Y:
			self.__reset()


class ChallengeCard(ElementGroup, Hoverable):

	ENTRY_DURATION = 1.1

	@staticmethod
	def create_group_elements():
		start_button = Button(
			SpriteAnimation(SpriteProvider.get("Btn_StartChallenge.png"), [1], [60], (570, 60)),
			on_click=lambda _: None
		)
		title = TextDisplay(FontSettings("resources/fonts/Code.ttf", 28, ColorProvider.get("fg")))
		description = TextDisplay(FontSettings("resources/fonts/Start.otf", 26, ColorProvider.get("fg")))
		score = TextDisplay(FontSettings("resources/fonts/Code.ttf", 26, ColorProvider.get("fg")))
		difficulty = TextDisplay(FontSettings("resources/fonts/Starz 2.ttf", 26, ColorProvider.get("star_level_0")))

		return [start_button, title, description, score, difficulty]

	def __init__(self, challenge: Challenge):
		from game import challenge_manager
		self.challenge = challenge
		super().__init__(ChallengeCard.create_group_elements())
		self.setup_group_properties()
		self.setup_group_elements()
		self.anim_start_pos = C.DISPLAY_RECT.centerx - self.width / 2, C.DISPLAY_RECT.centery - self.height / 2

		entry_animation = Animation(self.ENTRY_DURATION)
		entry_animation.set_progress_percent((challenge_manager.get_challenge_count() - challenge.get_id()) / (1.3 * challenge_manager.get_challenge_count()))
		entry_animation.set_speed(-1).set_end_behavior(lambda anim: anim.reverse() if anim.get_speed() < 0 else anim.pause())
		self.add_animation("entry", entry_animation.start())

		s, coeff = C.DISPLAY_SIZE, 0.75
		a, b = max(s[0], s[1]) * coeff / 2, min(s[0], s[1]) * coeff / 2
		fixed_center = s[0] / 2 - self.width / 2, s[1] / 2 - self.height / 2
		self.target_location = point_in_elliptical_disk(2 * math.pi * challenge.get_id() / challenge_manager.get_challenge_count(), fixed_center, a, b)
		self._completed = False

	def get_start_button(self) -> Button:
		return self.get_elements()[0]

	def get_title_display(self) -> TextDisplay:
		return self.get_elements()[1]

	def get_description_display(self) -> TextDisplay:
		return self.get_elements()[2]

	def get_score_display(self) -> TextDisplay:
		return self.get_elements()[3]

	def get_difficulty_display(self) -> TextDisplay:
		return self.get_elements()[4]

	def get_target_location(self) -> tuple[float, float]:
		return self.target_location

	def set_target_location(self, pos: tuple[float, float]):
		self.target_location = pos

	def setup_group_properties(self):
		self.set_background_color(ColorProvider.get('fg'))
		self.set_relative_width(0.25, False).set_relative_height(0.15).set_original_size(self.size)
		self.set_anchor("center").set_relative_pos((0.5, 0.5))
		self.on("drag", lambda el: el.set_target_location(self.get_position()))

	def setup_group_elements(self):
		max_width = max(0, self.width - 20)  # Max width occupied by the elements
		score_bot_margin = 30  # px, margin between score display and difficulty display
		desc_bot_margin = 80  # px, margin between challenge description and its start button

		title = self.get_title_display()
		title.set_content(">/ " + self.challenge.get_name())\
			.set_anchor("midtop")\
			.set_relative_pos((0.5, 0.1))\
			.set_max_width(max_width)

		description = self.get_description_display()
		description.set_content(self.challenge.get_description()) \
			.set_anchor("midtop")\
			.set_max_width(max_width)\
			.set_absolute_pos(title.get_position())\
			.move((0, title.height))

		difficulty = self.get_difficulty_display()
		difficulty.set_content(("F" * self.challenge.get_difficulty()))\
			.set_anchor("midtop") \
			.set_absolute_pos(description.get_position())\
			.set_max_width(max_width)\
			.move((0, title.height + description.height))
		difficulty.get_display_settings().set_color(ColorProvider.get("star_level_" + str(self.challenge.get_difficulty())))

		score = self.get_score_display()
		score.set_content("Best : " + self.challenge.get_result_str())\
			.set_anchor("midtop")\
			.set_absolute_pos(difficulty.get_position())\
			.set_max_width(max_width)\
			.move((0, score_bot_margin))
		score.get_display_settings().set_color(ColorProvider.get('fg'))

		start_button = self.get_start_button()
		start_button.set_relative_width(0.9)

		self.set_original_size((self.width, title.height + description.height + difficulty.height + score_bot_margin + score.height + desc_bot_margin + start_button.height))

		start_button.set_anchor("midtop")\
			.set_absolute_pos(score.get_position())\
			.set_anchor("center") \
			.move((0, desc_bot_margin))
		start_button.set_click_callback(lambda: scene_manager.get_current_scene().start_challenge(self.challenge))

	def get_challenge(self) -> Challenge:
		return self.challenge

	def on_fully_completed(self):
		# Random angle method
		# out_r = math.sqrt((C.DISPLAY_SIZE[0]) ** 2 + (C.DISPLAY_SIZE[1] ** 2)) * 1.5
		# angle = random.random() * 2 * math.pi
		# self.set_target_location((out_r * math.cos(angle), out_r * math.sin(angle)))

		# Extended normalized direction method
		def _():
			out_r = math.sqrt((C.DISPLAY_SIZE[0]) ** 2 + (C.DISPLAY_SIZE[1] ** 2)) * 1.5
			center = C.DISPLAY_RECT.center
			current = self.get_position(C.DISPLAY_RECT)
			target_x = out_r * (current[0] - center[0]) / math.sqrt(((current[0] - center[0]) ** 2) + (current[1] - center[1]) ** 2)
			target_y = out_r * (current[1] - center[1]) / math.sqrt(((current[0] - center[0]) ** 2) + (current[1] - center[1]) ** 2)
			self.set_target_location((target_x, target_y))
			self.anim_start_pos = self.get_drawing_position(0)
			self.get_animation("entry").reset().start()

		for el in self.get_elements():
			el.shake(10, 1)
		self.shake(10, 1, _)

	def refresh_text(self):
		prefix = "Best"
		if self.challenge.is_fully_completed():
			prefix = "Score"
			self.get_start_button().set_enabled(False)
		self.get_score_display().set_content(prefix + " : " + self.challenge.get_result_str())

	def tick(self, dt: float):
		super().tick(dt)
		anim = self.get_animation("entry")
		if anim.is_running():
			progress = 1 / (1 + math.exp(-12 * ((anim.get_progress_percent() if anim.get_speed() > 0 else 0) - 0.5)))

			new_x = self.anim_start_pos[0] + (self.target_location[0] - self.anim_start_pos[0]) * progress
			new_y = self.anim_start_pos[1] + (self.target_location[1] - self.anim_start_pos[1]) * progress
			self.move((new_x - self.x, new_y - self.y))
			return

		self.set_draggable(True)


class Timer(TextDisplay):

	def __init__(self, display_settings: FontSettings, **kwargs):
		"""

		:param display_settings:
		:param kwargs:
			-> format : %H, %M, %S => Hours, Minutes, Seconds with 1 leading zero
						%m => Milliseconds
			-> clock : Starting time, in seconds
			-> limit : Lower and upper limit
		"""
		super().__init__(display_settings, **kwargs)
		self.format = None
		self.clock = kwargs.get('clock', 60)  # in seconds
		self.limit = kwargs.get('limit', [0, 24 * 60 * 60])
		self.current = self.clock
		self.running = False
		self.set_format(kwargs.get('format', '%H:%M:%S.%m'))
		self.multiplier = 1

	def reset(self) -> 'Timer':
		self.current = self.clock
		self.set_content(self.get_display_time())
		return self

	def start(self) -> 'Timer':
		self.running = True
		return self

	def pause(self) -> 'Timer':
		self.running = False
		return self

	def as_countdown(self) -> 'Timer':
		self.multiplier = -1
		return self

	def as_timer(self) -> 'Timer':
		self.multiplier = 1
		return self

	def set_format(self, _format: str) -> 'Timer':
		self.format = _format
		self.set_content(self.get_display_time())
		return self

	def get_format(self) -> str:
		return self.format

	def get_time(self) -> float:
		return self.current

	def get_initial_time(self) -> float:
		return self.clock

	def get_passed_time(self) -> float:
		return abs(self.get_initial_time() - self.get_time())

	def get_display_time(self) -> str:
		ms = self.current
		hours = ms // 3600
		ms -= hours * 3600
		minutes = ms // 60
		ms -= minutes * 60
		seconds = math.floor(ms)
		return self.format.replace("%H", "%02d" % hours).replace("%M", "%02d" % minutes).replace("%S", "%02d" % seconds).replace("%m", "%03d" % ((ms - seconds) * 1000))

	def tick(self, dt: float):
		if self.running:
			self.current += dt * self.multiplier
			self.current = min(self.limit[1], max(self.limit[0], self.current))
			if (self.current == self.limit[1] and self.multiplier > 0) or (self.current == self.limit[0] and self.multiplier < 0):
				self.call('timer_end')
			self.set_content(self.get_display_time())


class ChallengeInterface(ElementGroup):

	ENTRY_DURATION = 0.8

	def __init__(self, elements: list[SceneElement], **kwargs):
		super().__init__(elements, **kwargs)
		self.setup_group_properties()

		def exit_behavior(anim: Animation):
			scene_manager.get_current_scene().stop_challenge()
			anim.reset()

		self.add_animation("entry", Animation(self.ENTRY_DURATION).set_end_behavior(lambda _: _))
		self.add_animation("exit", Animation(self.ENTRY_DURATION).set_end_behavior(exit_behavior))

	def setup_group_properties(self):
		self.set_relative_width(1, False).set_relative_height(1).set_original_size(self.size)
		self.set_anchor("center").set_relative_pos((0.5, 0.5))

	def close(self):
		self.clear_elements(True)
		self.get_animation("exit").start()

	def tick(self, dt: float):
		super().tick(dt)
		entry_anim = self.get_animation("entry")
		exit_anim = self.get_animation("exit")
		if not entry_anim.is_running() and not exit_anim.is_running():
			if self.get_zoom() != (1, 1):
				self.set_zoom((1, 1))
			return

		percent = entry_anim.get_progress_percent() if entry_anim.is_running() else 1 - exit_anim.get_progress_percent()
		# progress = math.sin(anim.get_progress_percent() * math.pi / 2)
		progress = 1 / (1 + math.exp(-12 * (percent - 0.5)))
		self.set_zoom((progress, progress))


class TextArea(TextDisplay, Typable):

	PROMPT_BLINK_SPEED = 0.5
	BLINK_TIME = 0.5
	BLINK_FREQUENCY = 2

	BLINK_PATTERN = 0b01
	BLINK_CONTENT = 0b10
	BLINK_BOTH = 0b11

	pattern = None

	def __init__(self, display_settings: FontSettings, **kwargs):
		super().__init__(display_settings, **kwargs)
		self.add_animation("prompt_blink", Animation(TextArea.PROMPT_BLINK_SPEED).set_end_behavior(Animation.REWIND_ON_END).start())
		self.add_animation("error_blink", Animation(TextArea.BLINK_TIME).set_end_behavior(Animation.RESET_ON_END))

		self.pattern = kwargs.get("pattern", None)
		self.pattern_size, self.content_size = 0, 0
		self.pattern_color = kwargs.get("pattern_color", ColorProvider.get('placeholder'))
		self.pattern_display = FontSettings(display_settings.get_font_path(), display_settings.get_font_size(), self.pattern_color)
		self.require_pattern = kwargs.get("require_pattern", True)
		self.blink_color = ColorProvider.get("error")
		self.blink_mode = kwargs.get("blink_mode", TextArea.BLINK_PATTERN)
		self.enabled = True
		self.enable_multiline = kwargs.get("multiline", True)

		self.on("type", lambda _: self._recompute_size())
		self.on("erase", lambda _: self._recompute_size())
		self._recompute_size()

	def blink(self, color: Union[pygame.Color, None], then: Union[Callable[[], Any], None]):
		if color is not None:
			self.blink_color = color
		self.get_animation("error_blink").start()

		def end_behavior(anim):
			anim.reset()
			if then is not None:
				then()

		self.get_animation("error_blink").set_end_behavior(end_behavior)

	def _recompute_size(self) -> 'TextDisplay':
		if self.has_pattern():
			def _():
				self._word_positions.clear()
				font = self.get_display_settings().get_font()
				word_position = [0, 0]
				final_width, final_height = 0, 0

				for line in self.pattern.splitlines():
					subline = []
					for word in line.split(" "):
						next_content = " ".join(subline + [word])
						next_size = self.get_display_settings().get_font().size(next_content)[0]
						if next_size > self._max_width > 0:
							# Update word position and append to the list
							word_position[0] = 0
							word_position[1] += font.get_height()
							self._word_positions.append(word_position)

							# Increase text final size
							final_width = self._max_width
							final_height += font.get_height()

							# Reset line content
							subline = [] if len(subline) == 0 else [word]
						else:
							subline.append(word)
							# Append word position to the list and update next word's starting point
							self._word_positions.append(word_position)
							word_position[0] = next_size
							# Update final width
							final_width = max(final_width, next_size)
					final_height += font.get_height()
				self.set_original_size((final_width, final_height))
				self.get_display_settings().clear_dirty()
			self.lock_pos(_)
			return self
		else:
			self.content_size = len(self.get_content().splitlines())
			return super()._recompute_size()

	def is_enabled(self) -> bool:
		return self.enabled

	def enable(self) -> 'TextArea':
		self.enabled = True
		return self

	def disable(self) -> 'TextArea':
		self.enabled = False
		return self

	def get_next_character(self, n: int = 1) -> str:
		if not self.has_pattern() or self.is_complete():
			return ""
		return self.pattern[len(self.get_content()):len(self.get_content()) + n]

	def has_pattern(self) -> bool:
		return self.pattern is not None

	def get_pattern(self) -> Union[str, None]:
		return self.pattern

	def set_pattern(self, pattern: str) -> 'TextArea':
		self.pattern = pattern
		self._recompute_size()
		return self

	def set_require_pattern(self, require: bool) -> 'TextArea':
		self.require_pattern = require
		return self

	def is_pattern_required(self) -> bool:
		return self.has_pattern() and self.require_pattern

	def is_complete(self) -> bool:
		return self.has_pattern() and self.get_content() == self.pattern

	def is_multiline(self) -> bool:
		return (self.has_pattern() and self.pattern_size > 1) or self.enable_multiline

	def on_type(self, letter: str):
		if not self.is_enabled():
			return
		if letter == "":
			return
		if letter == "\n" and not self.is_multiline():
			return
		if letter == "\x08" and not self.is_pattern_required():
			# Support backspaces
			if self.get_content() == "":
				return
			self.set_content(self.get_content()[:-1])
			self.get_animation("prompt_blink").reset().start()
			self.call("erase")
			return
		if letter == "\t" and self.get_next_character(4) == "    ":
			letter = "    "
		elif letter != self.get_next_character() and self.is_pattern_required():
			self.blink(ColorProvider.get("error"), None)
			return
		elif letter not in string.printable or letter == "\t":
			return
		self.set_content(self.get_content() + letter)
		self.get_animation("prompt_blink").reset().start()
		self.call("type")
		if self.is_complete():
			self.call("text_complete")

	def get_drawing_position(self, surface_id: int) -> tuple[float, float]:
		if self.has_pattern():
			is_bar = surface_id >= self.content_size + self.pattern_size
		else:
			is_bar = surface_id >= self.content_size

		if is_bar:
			# Compute cursor position
			pos = super().get_drawing_position(max(0, self.content_size - 1))
			last_line = "" if self.get_content() == "" else self.get_content().splitlines()[-1]
			last_line_size = self.get_display_settings().get_font().size(last_line)[0] if last_line != "" else 0
			width_fix = (0.5 * self.get_display_settings().get_font().size(" ")[0])
			return pos[0] + last_line_size * self.get_zoom()[0] - (width_fix if last_line != "" else 0), pos[1]
		if self.has_pattern() and surface_id >= self.pattern_size > 0:
			surface_id -= self.pattern_size
		return super().get_drawing_position(surface_id)

	def render(self) -> list[pygame.Surface]:
		pattern_color_save, content_color_save = None, None
		blink_animation = self.get_animation("error_blink")
		prompt_anim = self.get_animation("prompt_blink")
		if blink_animation.is_running() and math.cos(blink_animation.get_progress_percent() * self.BLINK_FREQUENCY * math.pi) > 0:
			if self.blink_mode & TextArea.BLINK_PATTERN:
				pattern_color_save = self.pattern_display.get_color()
				self.pattern_display.set_color(self.blink_color)
			if self.blink_mode & TextArea.BLINK_CONTENT:
				content_color_save = self.get_display_settings().get_color()
				self.get_display_settings().set_color(self.blink_color)
			prompt_anim.reset()

		bar = [self.get_display_settings().render_line("|")] if prompt_anim.get_progress_percent() <= 0.5 else []

		if not self.has_pattern():
			result = super().render() + bar
		else:
			pattern_lines = TextArea.render_text(self.get_pattern(), self.pattern_display, self.get_max_width())
			content_lines = super().render()

			self.pattern_size = len(pattern_lines)
			self.content_size = len(content_lines) + (1 if self.get_content().endswith("\n") else 0)

			result = pattern_lines + content_lines + bar

		if pattern_color_save is not None:
			self.pattern_display.set_color(pattern_color_save)
		if content_color_save is not None:
			self.get_display_settings().set_color(content_color_save)

		return result

	def reset(self):
		self.set_content("")


class DrawingCell(Hoverable):

	COLOR_TRANSITION_DURATION = 0.5

	def __init__(self, width: int, height: int, **kwargs):
		super().__init__(width, height, **kwargs)
		self._hover_color = kwargs.get("hover_color", ColorProvider.get("fg"))
		self._empty_color = kwargs.get("empty_color", ColorProvider.get("bg"))
		self._filled_color = kwargs.get("filled_color", ColorProvider.get("fg"))
		self._border_color = kwargs.get("border_color", ColorProvider.get("fg2"))
		self._filled = kwargs.get("filled", False)
		self.add_animation("hover_color_transition", Animation(DrawingCell.COLOR_TRANSITION_DURATION).set_end_behavior(Animation.PAUSE_ON_END))
		self.on("click", lambda _: self.invert_filled_state())
		self.on("mouse_enter", lambda _: self.get_animation("hover_color_transition").set_progress_percent(1))
		self.on("mouse_enter", lambda _: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND))
		self.on("mouse_leave", lambda _: self.get_animation("hover_color_transition").set_speed(-1).start() if not self.is_filled() else None)
		self.on("mouse_leave", lambda _: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW))

	def is_filled(self) -> bool:
		return self._filled

	def set_filled(self, filled: bool) -> 'DrawingCell':
		self._filled = filled
		return self

	def get_filled_color(self) -> pygame.Color:
		return self._filled_color

	def set_filled_color(self, color: pygame.Color) -> 'DrawingCell':
		self._filled_color = color
		return self

	def invert_filled_state(self):
		self._filled = not self._filled
		if self._filled:
			self.get_animation("hover_color_transition").reset()
		else:
			self.get_animation("hover_color_transition").set_progress_percent(1)

	def get_drawing_color(self) -> pygame.Color:
		hover_anim = self.get_animation("hover_color_transition")
		color = self._filled_color if self.is_filled() else self._empty_color
		if hover_anim.is_running():
			to_color = self._hover_color
			progress = hover_anim.get_progress_percent()
			color = pygame.Color(int(color.r + progress * (to_color.r - color.r)), int(color.g + progress * (to_color.g - color.g)), int(color.b + progress * (to_color.b - color.b)))
		elif self.is_hovered() and not self.is_filled():
			return self._hover_color
		return color

	def render(self) -> list[pygame.Surface]:
		s = pygame.Surface(self.size)
		pygame.draw.rect(s, self.get_drawing_color(), s.get_rect())
		pygame.draw.lines(s, self._border_color, True, ((0, 0), (0, s.get_height() - 1), (s.get_width() - 1, s.get_height() - 1), (s.get_width() - 1, 0)))
		return [s]


class DrawingGrid(ElementGroup):

	BLINK_TIME = 0.5
	BLINK_FREQUENCY = 2

	def __init__(self, grid_size: tuple[int, int], **kwargs):
		assert grid_size[0] != 0 and grid_size[1] != 0
		super().__init__([DrawingCell(20, 20, **kwargs).set_anchor("topleft") for _ in range(grid_size[0] * grid_size[1])], **kwargs)
		self._grid_size = grid_size
		self._filled_color = kwargs.get("filled_color", ColorProvider.get("fg"))
		self._blink_color = ColorProvider.get("error")
		self.set_original_size((20 * grid_size[0], 20 * grid_size[1]))
		self.on("resize", lambda _: self.refresh_cells_size())
		self.on("move", lambda _: self.refresh_cells_size())
		self.add_animation("blink", Animation(DrawingGrid.BLINK_TIME).set_end_behavior(Animation.RESET_ON_END))

	def set_relative_width(self, relw: float, keep_ratio: bool = True, holder: Union[pygame.Rect, None] = None) -> 'SceneElement':
		return super().set_relative_width(relw, True, holder)

	def set_relative_height(self, relh: float, keep_ratio: bool = True, holder: Union[pygame.Rect, None] = None) -> 'SceneElement':
		return super().set_relative_height(relh, True, holder)

	def blink(self, color: pygame.Color, then: Union[Callable[[], Any], None]):
		self._blink_color = color
		self.get_animation("blink").start()

		def end_behavior(anim):
			anim.reset()
			_cell: DrawingCell
			for _cell in self.get_elements():
				_cell.set_enabled(True)
				_cell.set_filled_color(self._filled_color)
				_cell.set_filled(False)
			if then is not None:
				then()

		cell: DrawingCell
		for cell in self.get_elements():
			cell.set_enabled(False)

		self.get_animation("blink").set_end_behavior(end_behavior)

	def refresh_cells_size(self):
		unit_size = int(self.width / self._grid_size[0]), int(self.height / self._grid_size[1])
		x, y = 0, 0
		for cell in self.get_elements():
			cell.set_original_size(unit_size)
			cell.set_relative_pos((x / self._grid_size[0], y / self._grid_size[1]))
			x += 1
			if x == self._grid_size[0]:
				x, y = 0, y + 1

	def compare(self, pattern: list[list[bool]]) -> bool:
		x, y = 0, 0
		cell: DrawingCell
		for cell in self.get_elements():
			if cell.is_filled() != pattern[y][x]:
				return False
			x += 1
			if x == self._grid_size[0]:
				x, y = 0, y + 1
		return True

	def tick(self, dt: float):
		super().tick(dt)

		blink_animation = self.get_animation("blink")
		if not blink_animation.is_running():
			return
		if not math.cos(blink_animation.get_progress_percent() * self.BLINK_FREQUENCY * math.pi) > 0:
			cell_color = self._filled_color
		else:
			cell_color = self._blink_color

		cell: DrawingCell
		for cell in self.get_elements():
			cell.set_filled_color(cell_color)

