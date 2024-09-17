import json
import re

from elements.Attributes import SpriteAnimation
from elements.Elements import ChallengeInterface
from game import Challenge
from game.types.IdenticonDrawingChallenge import IdenticonDrawingChallenge
from game.types.StatementAnswerChallenge import StatementAnswerChallenge
from game.types.WordMatchingChallenge import WordMatchingChallenge
from providers import SpriteProvider, FileProvider
from scene import scene_manager


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

	def add_point(self):
		self._points += 1
		if self._points == len(self._challenges):
			scene_manager.set_active_scene(scene_manager.END_SCENE)

	def get_points(self) -> float:
		return self._points

	def init_challenges(self, container: ChallengeInterface):
		self.add_challenge(StatementAnswerChallenge(
			len(self._challenges),
			"Weak password", "Retrouve le mot de passe du PC",
			"Logique", 1,
			container, "That's how they got in...\nAlways use strong passwords !",
			"La note suivante a été trouvée auprès du PC compromis:\n\n\"Nom de mon club préféré, avec des chiffres à la place des lettres 'O', 'E' et 'A'",
			"H0n3yp0t H4ck3r", "________ ______",
			SpriteAnimation(SpriteProvider.get("HoneyPot_Logo_Nameless.png"), [1], [64], None)
		))
		self.add_challenge(StatementAnswerChallenge(
			len(self._challenges),
			"A Hacker's mark", "Un message codé?",
			"Cryptographie", 1,
			container, "Seriously, morse code ?!",
			"En ouvrant la session, l'admin a trouvé un fichier README.txt avec le contenu suivant.\nDécode-le pour voir s'il contient des infos importantes:\n.. -- / .-- ....- - -.-. .... .---- -. --. / -.-- ----- ..-",
			"Im w4tch1ng y0u", "__ ________ ___", case_sensitive=True
		))
		self.add_challenge(StatementAnswerChallenge(
			len(self._challenges),
			"Hacker OS", "Trouver le système d'exploitation du hacker",
			"OSINT", 1,
			container, "Damn it, they know what they're doing !",
			"Connaître le système d'exploitation utilisé par le hacker pourrait nous servir à l'infiltrer à notre tour...\nIl s'agit probablement de celui dont le logo est présenté ci-dessous.",
			lambda x: x.lower() in ["kali", "kali linux", "linux kali"], None,
			SpriteAnimation(SpriteProvider.get('kali.png'), [1], [64], None)
		))
		self.add_challenge(StatementAnswerChallenge(
			len(self._challenges),
			"Numeral Systems", "Comptons comme un ordinateur",
			"Logique", 2,
			container, "A hacker knows its numerals",
			"Une capture réseau a dévoilé un flux constant de données vers la Russie.\n0b1000_0011  paquets d'une taille de  0x4AD  octets ont été transmis chaque minute.\nLe nombre d'octets volés en 5 minutes est donc, en base 10, de:",
			"784035", None
		))
		self.add_challenge(StatementAnswerChallenge(
			len(self._challenges),
			"Network Mapping", "Mapper l'origine de l'attaque",
			"Network", 2,
			container, "We know where the attack came from !",
			"Une adresse IP revient de manière récurrente dans les logs du PC.\nLe résultat d'un traceroute vers cette IP est joint ci-dessous\nDans quelle ville se situe le dernier serveur à répondre à la requête?",
			lambda x: x.lower().replace(" ", "") in ["newyork", "newyorkcity", "nyc"], None, SpriteAnimation(SpriteProvider.get("Network1.png"), [1], [64], None)
		))
		self.add_challenge(StatementAnswerChallenge(
			len(self._challenges),
			"New Coordinates", "Localiser le pc de l'intrus",
			"OSINT", 2,
			container, "///what.the.f*ck\n\nThey were at Starbucks !",
			# "Des coordonnées GPS pointant vers l'intrus sont apparues: 47°28'29.5875\"N, 0°35'42.1800\"W\nOn devrait pouvoir s'en souvenir facilement...\nLe système ///what.3.words pourrait être idéal dans notre cas !",
			"On a retrouvé un indice étrange dans les fichiers de l'attaque: ///wagon.ronce.rouiller\nIl s'agit peut-être d'un système de coordonnées? Retrouver depuis quel café l'individu s'est connecté",
			"Starbucks", "_________"
		))
		self.add_challenge(WordMatchingChallenge(
			len(self._challenges),
			"Grocery List", "Reconstitue le nom du matériel informatique",
			"Benchmark", 3,
			container, "Hardly clever, I cancelled the order",
			json.loads(FileProvider.get('HardwareGuessingList.json')),
			"La carte bancaire de l'admin était enregistrée dans son navigateur.\nL'intrus en a profité pour faire ses courses et se construire un PC.\nReconsitue le nom du matériel informatique depuis les lettres mélangées:"
		))
		self.add_challenge(StatementAnswerChallenge(
			len(self._challenges),
			"Compromised User", "Découvre le mot de passe du hacker",
			"Client Side", 3,
			container, "You have their credentials !  B-)",
			"Nous avons découvert à l'instant le code source du RAT fournissant un accès à distance au PC infecté.\nSi on trouve le mot de passe du hacker, on pourra peut-être nous infiltrer à notre tour sur ses serveurs.",
			"R3m0teR4T", "_________",
			SpriteAnimation(SpriteProvider.get("ClientSide1.png"), [1], [64], None),
			case_sensitive=True
		))
		self.add_challenge(StatementAnswerChallenge(
			len(self._challenges),
			"Hidden Data", "Nouveau fond d'écran",
			"Stéganographie", 3,
			container, "They be toying with us !",
			"Le hacker a osé changer le fond d'écran de l'admin !!!\nIl doit y avoir une information cachée sur l'image si on regarde de près !",
			"h1ddenG3m", "_________",
			SpriteAnimation(SpriteProvider.get("Stega1.png"), [1], [64], None),
			case_sensitive=True
		))
		self.add_challenge(IdenticonDrawingChallenge(
			len(self._challenges),
			"Online Identity", "L'identicon GitHub du hacker.",
			"OSINT", 4,
			container, "We discovered their online identity !",
			"L'info la plus précieuse que nous possédons de l'intrus est le pseudo de son compte GitHub:  MisTurtle.\nIl faudrait que l'on puisse retrouver son identicon Github pour le tracer en ligne.\nJe crois qu'il y a un lien GitHub officiel pour l'obtenir...",
			[
				[True, True, True, True, True],
				[True, True, True, True, True],
				[True, False, True, False, True],
				[False, False, True, False, False],
				[True, False, False, False, True]
			]
		))
