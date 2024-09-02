import os
import sys

if getattr(sys, 'frozen', False):
	os.chdir(sys._MEIPASS)

import contextlib
with contextlib.redirect_stdout(None):
	import pygame

import providers
from typing import Callable, Any

from game import challenge_manager
from scene import scene_manager
from scene.all.EndScene import EndScene
from scene.all.GameScene import GameScene
from scene.all.MenuScene import MenuScene
from utils import AppState, C, Provider

# Initialize pygame and compute screen size
pygame.init()
info = pygame.display.Info()
C.DISPLAY_SIZE = info.current_w, info.current_h
C.DISPLAY_RECT = pygame.Rect((0, 0), C.DISPLAY_SIZE)
screen = pygame.display.set_mode(C.DISPLAY_SIZE, pygame.FULLSCREEN)

# Initialize base providers (font, sprite, ...)
providers.init()

# Initialize window icon and title
pygame.display.set_caption("FuriousHacker by Honeypot")
pygame.display.set_icon(providers.SpriteProvider.get('HoneyPot_Logo_NOBG_Centered.png'))

# Register scenes
scene_manager.set(scene_manager.MENU_SCENE, MenuScene())
game_scene = GameScene()
scene_manager.set(scene_manager.GAME_SCENE, game_scene)
scene_manager.set(scene_manager.END_SCENE, EndScene())

challenge_manager.init_challenges(game_scene.challenge_interface)

# Add Challenges
for challenge in challenge_manager.get_challenges():
	game_scene.add_element(challenge.create_card())

# Create Scene Manager
scene_manager.set_active_scene(scene_manager.MENU_SCENE)

# Register event handlers
EventHandlers: Provider[int, Callable[[pygame.event.Event], Any]] = Provider[
	int, Callable[[pygame.event.Event], None]]()
EventHandlers.set(pygame.QUIT, lambda _: AppState.stop())
EventHandlers.set(pygame.MOUSEMOTION, lambda ev: scene_manager.set_cursor(ev.pos))
EventHandlers.set(pygame.MOUSEBUTTONDOWN, lambda ev: scene_manager.handle_click(ev.pos, ev.button))
EventHandlers.set(pygame.MOUSEBUTTONUP, lambda ev: scene_manager.handle_release(ev.button))
EventHandlers.set(pygame.KEYDOWN, lambda ev: scene_manager.type(ev.unicode))

# Begin main loop
clock = pygame.time.Clock()
elapsed = .0
while AppState.is_running() and scene_manager.get_current_scene() is not None:
	for event in pygame.event.get():
		EventHandlers.get(event.type, lambda _: None)(event)
	scene_manager.get_current_scene().update(elapsed / 1000)
	scene_manager.get_current_scene().draw(screen)
	for shader in providers.ShaderProvider.get_all().values():
		shader(screen)
	pygame.display.update()
	elapsed = clock.tick(AppState.get_target_frame_rate())
	AppState.register_frame_time(1000 / elapsed)
