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
		self._challs_complete = 0

	def get_challenge_count(self) -> int:
		return len(self._challenges)

	def get_challenges(self) -> list[Challenge]:
		return self._challenges

	def get_challenge(self, _id: int):
		return self._challenges[_id] or None

	def add_challenge(self, c):
		self._challenges.append(c)

	def add_point(self, n_challs: int = 1, n_points: int = 1):
		self._challs_complete += n_challs
		self._points += n_points
		if self._challs_complete == len(self._challenges):
			scene_manager.set_active_scene(scene_manager.END_SCENE)

	def get_points(self) -> float:
		return self._points
	
	def get_max_points(self) -> int:
		return sum(c.get_difficulty() for c in self._challenges)
	
	def get_completed_challs(self) -> int:
		return self._challs_complete

	def init_challenges(self, container: ChallengeInterface):
		
		self.add_challenge(StatementAnswerChallenge(
			len(self._challenges),
			"Mot de passe faible", "Retrouve le mot de passe du PC",
			"Logique", 1,
			container, "Utilise toujours un mot de passe solide !",
			"La note suivante a été trouvée auprès du PC compromis:\n\n\"Nom de mon club préféré, avec des chiffres à la place des voyelles.\"",
			"H0n3yp0t H4ck3r", "________ ______",
			SpriteAnimation(SpriteProvider.get("HoneyPot_Logo_Nameless.png"), [1], [64], None)
		))

		self.add_challenge(WordMatchingChallenge(
			len(self._challenges),
			"Matériel", "Reconstitue le nom du matériel informatique",
			"Logique", 1,
			container, "Enregistrer sa CB sur Amazon, c'est dangereux...",
			json.loads(FileProvider.get('HardwareGuessingList.json')),
			"La carte bancaire de l'admin était enregistrée dans son navigateur.\nL'intrus en a profité pour faire ses courses et se construire un PC.\nReconsitue le nom du matériel informatique grâce aux lettres mélangées:"
		))
		
		self.add_challenge(StatementAnswerChallenge(
			len(self._challenges),
			"Message codé", "Il se phoque de nous?",
			"Cryptographie", 2,
			container, "Une menace en code morse? Beep boop beep beep !",
			"En ouvrant la session, l'admin a trouvé un fichier README.png avec l'image suivante.\nDécode son contenu pour voir s'il contient des infos importantes:",
			"get pwned", "___ _____", SpriteAnimation(SpriteProvider.get("morse.png"), [1], [64], None)
		))

		self.add_challenge(StatementAnswerChallenge(
			len(self._challenges),
			"Avez-vous les bases?", "Binaire... Hexadécimal???",
			"Logique", 2,
			container, "1 + 1 = 0b10",
			"Une capture réseau a dévoilé un flux constant de données vers la Russie.\n0b10011 paquets d'une taille de  0x4AD  octets sont transmis chaque seconde.\nLe nombre d'octets volés chaque seconde est donc, en base décimale:",
			"22743", "_____"
		))
		
		self.add_challenge(StatementAnswerChallenge(
			len(self._challenges),
			"Hacker OS", "Trouver le système d'exploitation du hacker",
			"OSINT", 3,
			container, "Rah c'est clairement pas un Script Kiddy !",
			"Connaître le système d'exploitation utilisé par le hacker pourrait nous servir à l'infiltrer à notre tour...\nIl s'agit probablement de celui dont le logo est affiché ci-dessous.",
			lambda x: x.lower() in ["kali", "kali linux", "linux kali"], None,
			SpriteAnimation(SpriteProvider.get('kali.png'), [1], [64], None)
		))

		self.add_challenge(StatementAnswerChallenge(
			len(self._challenges),
			"Ping !", "Trouver l'origine de l'attaque",
			"Network", 3,
			container, "On sait d'où provient l'attaque !",
			"Une adresse IP revient de manière récurrente dans les logs du PC.\nLe résultat d'un traceroute vers cette IP est joint ci-dessous\nDans quelle ville se situe le dernier serveur à répondre à la requête?",
			lambda x: x.lower().replace(" ", "") in ["newyork", "newyorkcity", "nyc"], None, SpriteAnimation(SpriteProvider.get("Network1.png"), [1], [64], None)
		))
		
		self.add_challenge(StatementAnswerChallenge(
			len(self._challenges),
			"Caché sous nos yeux", "Que signifie cette image...",
			"Stéganographie", 4,
			container, "Calcium, vraiment ?",
			"La stéganographie, l'art de cacher des informations dans un fichier, à la vue de tous... Un mot se cache clairement dans cette image, retrouvez le !",
			"calcium", "_______",
			SpriteAnimation(SpriteProvider.get("stega9.bmp"), [1], [64], None)
		))

		self.add_challenge(StatementAnswerChallenge(
			len(self._challenges),
			"Coordonnées étranges", "Localiser l'intrus",
			"OSINT", 4,
			container, "///what.the.f*ck\nPratique comme système !",
			"Le hacker a glissé un taunt dans les logs: \"Venez me chercher à ///aérien.huilant.baladant\"\nVous vous souvenez qu'il s'agit d'un système de coordonnées assez bizarre qui commence par trois slashs...\nRetrouvez depuis quel café l'individu s'est connecté",
			"Cafe Landwer", "____ _______"
		))

		self.add_challenge(StatementAnswerChallenge(
			len(self._challenges),
			"Contre-attaque", "Découvre le mot de passe du hacker",
			"Client Side", 5,
			container, "On a son mot de passe !",
			"Nous avons découvert à l'instant le code source du RAT fournissant un accès à distance au PC infecté.\nSi on trouve le mot de passe du hacker, on pourra s'infiltrer à notre tour sur ses serveurs.",
			"R3m0teR4T", "_________",
			SpriteAnimation(SpriteProvider.get("ClientSide1.png"), [1], [64], None),
			case_sensitive=True
		))
