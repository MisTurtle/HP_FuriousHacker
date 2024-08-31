import hashlib
import json
import re

from elements.Attributes import SpriteAnimation
from elements.Elements import ChallengeInterface
from game import Challenge
from game.types.IdenticonDrawingChallenge import IdenticonDrawingChallenge
from game.types.StatementAnswerChallenge import StatementAnswerChallenge
from game.types.TypingChallenge import TypingChallenge
from game.types.WordMatchingChallenge import WordMatchingChallenge
from providers import FileProvider, SpriteProvider


class ChallengeManager:

	def __init__(self):
		self._challenges = []
		self._points = 0

	def get_challenge_count(self) -> int:
		return len(self._challenges)

	def get_challenges(self) -> list[Challenge]:
		return self._challenges

	def get_challenge(self, _id: int):
		return self._challenges[_id] or None

	def add_challenge(self, c):
		self._challenges.append(c)

	def get_points(self) -> float:
		return self._points

	def recompute_points(self) -> float:
		self._points = 0
		for chall in self.get_challenges():
			self._points += chall.compute_score(chall.get_result())
		return self._points

	def init_challenges(self, container: ChallengeInterface):
		self.add_challenge(TypingChallenge(
			len(self._challenges),
			"Newbie Typerman", "Ecris un programme court en moins de 25 secondes", 1,
			container, None,
			clock=25, text=FileProvider.get("NewbieTyperman_Sample.py")
		))
		self.add_challenge(TypingChallenge(
			len(self._challenges),
			"Expert Typerman", "Ecris un programme complexe en moins de 45 secondes", 4,
			container, None,
			clock=45, text=FileProvider.get("ExpertTyperman_Sample.py")
		))
		self.add_challenge(WordMatchingChallenge(
			len(self._challenges),
			"Hardly Clever", "Connaissance du matériel", 3,
			container, "You know your parts !",
			json.loads(FileProvider.get("HardwareGuessingList.json")),
			"Reconstitue le nom du matériel informatique avec les lettres mélangées"
		))
		self.add_challenge(IdenticonDrawingChallenge(
			len(self._challenges),
			"Identicon", "Recherce en source ouverte", 3,
			container, "Openly Intelligent ^_^",
			"Je suis Byron CHOLET, étudiant à Polytech Angers. Trouve l'identicon de mon compte Github en me recherchant sur internet.",
			[
				[True, True, True, True, True],
				[True, True, True, True, True],
				[True, False, True, False, True],
				[False, False, True, False, False],
				[True, False, False, False, True]
			]
		))
		# 47°28'47"N 0°35'23.2"W
		self.add_challenge(StatementAnswerChallenge(
			len(self._challenges),
			"Exact Positioning", "Des coordonnées pratiques", 2,
			container, "///what.the.f*ck", "Décrire l'arrêt Notre-dame-du-Lac (GPS : 47\u03b128'47\"N   0\u03b135'23.2\"W) avec 3 mots", "///inactif.isoler.drap", "///_______.______.____"
		))

		self.add_challenge(StatementAnswerChallenge(
			len(self._challenges),
			"Dot LED signal", "Dissimulation d'informations", 5,
			container, "|'-_-'|", "Un code à 4 chiffres se cache derrière ces signaux", "6279", "____",
			SpriteAnimation(SpriteProvider.get("Stega2.png"), [1], [64], (600, 250)))
		)

		self.add_challenge(StatementAnswerChallenge(
			len(self._challenges),
			"._.", "Bip boop, boop bip?", 1,
			container,
			# SOS
			"... --- ...",
			# desamorse
			"-.-.  ---  -..  .  /  ---...  /  -..  .  ...  .-  --  ---  .-.  ...  .", "desamorse", "_________"
		))

		self.add_challenge(StatementAnswerChallenge(
			len(self._challenges),
			"Magic Hashes", "Faille de typage", 5,
			container,
			"Welcome home, admin",
			"Trouver un mot de passe pour passer la vérification d'administrateur",
			# lambda answer: re.match("^0+e.*$", hashlib.md5(answer.encode('utf-8')).digest().decode("utf-8")) is not None,
			lambda answer: re.match("^0+e.*$", hashlib.md5(answer.encode('utf-8')).hexdigest()) is not None,
			None,
			SpriteAnimation(SpriteProvider.get("Hacking1.png"), [1], [64], (616, 355))
		))
		self.add_challenge(StatementAnswerChallenge(
			len(self._challenges),
			"Can't see no evil", "On peut pas zoomer ?", 1,
			container,
			"Decent sight ! D:",
			"\u03b1w\u03b1 Regarde de près", "h1ddenG3m", "_________", SpriteAnimation(SpriteProvider.get('Stega1.png'), [1], [64], (640, 452))
		))
		self.add_challenge(StatementAnswerChallenge(
			len(self._challenges),
			"Counting sheep", "1, 2, 3, 4, ..., zzz", 2,
			container,
			"Not asleep yet? Classic.",
			"Combien de carrés se cachent dans l'image?", lambda ans: ans == "385" or ans == "0x181", None, SpriteAnimation(SpriteProvider.get('Logic1.png'), [1], [64], (342, 342))
		))
