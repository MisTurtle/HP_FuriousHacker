# Solutions FuriousHacker - Édition 2024


<details>
    <summary>★ - Weak Password</summary>
    <h3>Énoncé</h3>
    <strong>La note suivante a été trouvée auprès du PC compromis: "Nom de mon club préféré, avec des chiffres à la place des lettres 'O', 'E' et 'A'</strong>
    <br /><br />
    Image : <strong>Logo du club sans le nom</strong>
    <h3>Démarche</h3>
    Le nom du club préféré étant bien évidemment <i>Honeypot Hacker</i>, la démarche attendue était de remplacer les lettres par un chiffre qui leur ressemble (0=O, 3=E, 4=A)
    <details>
        <summary>Solution</summary>
        &nbsp;&nbsp;&nbsp;&nbsp;H0n3yp0t H4ck3r
    </details>
</details>

<br/>

<details>
    <summary>★ - A Hacker's mark</summary>
    <h3>Énoncé</h3>
    <strong>En ouvrant la session, l'admin a trouvé un fichier README.txt avec le contenu suivant. Décode-le pour voir s'il contient des infos importantes: .. -- / .-- ....- - -.-. .... .---- -. --. / -.-- ----- ..-</strong>
    <h3>Démarche</h3>
    Utiliser une table de conversion pour le morse (complète, avec lettres et chiffres) et chercher les lettres une à une. Un traducteur automatique pouvait également être utilisé
    <details>
        <summary>Solution</summary>
        &nbsp;&nbsp;&nbsp;&nbsp;Im w4tch1ng y0u
    </details>
</details>

<br/>

<details>
    <summary>★ - Hacker OS</summary>
    <h3>Énoncé</h3>
    <strong>Connaître le système d'exploitation utilisé par le hacker pourrait nous servir à l'infiltrer à notre tour... Il s'agit probablement de celui dont le logo est présenté ci-dessous.</strong>
    <br /><br />
    Image : <strong>Logo d'un système d'exploitation</strong>
    <h3>Démarche</h3>
    Effectuer une recherche Google telle que "Système d'exploitation hacker" ou bien une recherche par image du logo
    <details>
        <summary>Solution</summary>
        &nbsp;&nbsp;&nbsp;&nbsp;Kali Linux
    </details>
</details>

<br/>

<details>
    <summary>★★ - Numeral Systems</summary>
    <h3>Énoncé</h3>
    <strong>Une capture réseau a dévoilé un flux constant de données vers la Russie. 0b1000_0011  paquets d'une taille de  0x4AD  octets ont été transmis chaque minute. Le nombre d'octets volés en 5 minutes est donc, en base 10, de:</strong>
    <h3>Démarche</h3>
    Convertir les deux nombres donnés (le premier étant en binaire et le second en hexadécimal) en base 10. Multiplier ces deux nombres pour obtenir la quantité d'octets transmise PAR MINUTE. Multiplier ce résultat par 5 pour connaître la taille totale en octets de la communication de 5 minutes.
    <details>
        <summary>Solution</summary>
        &nbsp;&nbsp;&nbsp;&nbsp;784035
    </details>
</details>

<br/>

<details>
    <summary>★★ - Network Mapping</summary>
    <h3>Énoncé</h3>
    <strong>Une adresse IP revient de manière récurrente dans les logs du PC. Le résultat d'un traceroute vers cette IP est joint ci-dessous. Dans quelle ville se situe le dernier serveur à répondre à la requête?</strong>
    <br /><br />
    Image : <strong>Capture d'écran d'une commande TRACERT</strong>
    <h3>Démarche</h3>
    Identifier l'adresse IP du dernier serveur à avoir répondu à la requête (216.6.90.22). Chercher un outil de localisation d'adresse IP (Ex: <a href="https://www.iplocation.net/ip-lookup">IP Location</a>). Y entrer l'adresse IP. Détecter la ville.
    <details>
        <summary>Solution</summary>
        &nbsp;&nbsp;&nbsp;&nbsp;New York City
    </details>
</details>

<br/>

<details>
    <summary>★★ - New Coordinates</summary>
    <h3>Énoncé</h3>
    <strong>On a retrouvé un indice étrange dans les fichiers de l'attaque: ///wagon.ronce.rouiller. Il s'agit peut-être d'un système de coordonnées? Retrouver depuis quel café l'individu s'est connecté</strong>
    <h3>Démarche</h3>
    Rechercher un type de coordonnées commençant par trois slashs. Le site <a href="https://what3words.com/">What3Words</a> apparaît dans les résultats. Y entrer les coordonnées spécifiées dans l'énnoncé.
    <details>
        <summary>Solution</summary>
        &nbsp;&nbsp;&nbsp;&nbsp;Starbucks
    </details>
</details>

<br/>

<details>
    <summary>★★★ - Grocery List</summary>
    <h3>Énoncé</h3>
    <strong>La carte bancaire de l'admin était enregistrée dans son navigateur. L'intrus en a profité pour faire ses courses et se construire un PC. Reconsitue le nom du matériel informatique depuis les lettres mélangées:</strong>
    <h3>Démarche</h3>
    Aucune démarche particulière attendue.
    <details>
        <summary>Solution</summary>
        <code>
        {
          "ecran": "rcnea",
          "clavier": "ialcevr",
          "processeur": "rsurpceoes",
          "carte graphique": "raetc epihaqgur",
          "alimentation": "anitmonlaiet",
          "disque": "usedqi",
          "microphone": "eominchpro",
          "carte mere": "traec reem",
          "souris": "isrous",
          "camera": "cmraea",
          "memoire ram": "imeoerm mra"
        }
        </code>
    </details>
</details>

<br/>

<details>
    <summary>★★★ - Compromised User</summary>
    <h3>Énoncé</h3>
    <strong>Nous avons découvert à l'instant le code source du RAT fournissant un accès à distance au PC infecté. Si on trouve le mot de passe du hacker, on pourra peut-être nous infiltrer à notre tour sur ses serveurs.</strong>
    <br /><br />
    Image : <strong>Capture d'écran d'un programme rédigé en Python</strong>
    <h3>Démarche</h3>
    Connaître ou chercher le rôle de la fonction <code>ord</code> en Python. En déduire que la liste de nombres au début du code fournit correspond à des caractères ASCII.
    <details>
        <summary>Solution</summary>
        &nbsp;&nbsp;&nbsp;&nbsp;R3m0teR4T
    </details>
</details>

<br/>

<details>
    <summary>★★★ - Hidden Data</summary>
    <h3>Énoncé</h3>
    <strong>Le hacker a osé changer le fond d'écran de l'admin !!! Il doit y avoir une information cachée sur l'image si on regarde de près !</strong>
    <br /><br />
    Image : <strong>Une image avec un texte caché dessus</strong>
    <h3>Démarche</h3>
    Faire attention aux détails de l'image et découvrir le texte caché par contraste indiquant la réponse à l'épreuve.
    <details>
        <summary>Solution</summary>
        &nbsp;&nbsp;&nbsp;&nbsp;h1ddenG3m
    </details>
</details>

<br/>

<details>
    <summary>★★★★ - Online Identity</summary>
    <h3>Énoncé</h3>
    <strong>L'info la plus précieuse que nous possédons de l'intrus est le pseudo de son compte GitHub:  MisTurtle. Il faudrait que l'on puisse retrouver son identicon Github pour le tracer en ligne. Je crois qu'il y a un lien GitHub officiel pour l'obtenir...</strong>
    <h3>Démarche</h3>
    Effectuer une recherche Google telle que "Find GitHub user identicon". Trouver le lien vers la page <a href="https://identicons.github.com/{pseudo}.png">GitHub officielle</a>. Remplacer le placeholder {pseudo} par celui donné dans l'énoncé.
    <details>
        <summary>Solution</summary>
        &nbsp;&nbsp;&nbsp;&nbsp;⬛⬛⬛⬛⬛ <br>
        &nbsp;&nbsp;&nbsp;&nbsp;⬛⬛⬛⬛⬛ <br>
        &nbsp;&nbsp;&nbsp;&nbsp;⬛⬜⬛⬜⬛ <br>
        &nbsp;&nbsp;&nbsp;&nbsp;⬜⬜⬛⬜⬜ <br>
        &nbsp;&nbsp;&nbsp;&nbsp;⬛⬜⬜⬜⬛
    </details>
</details>

<br/>


<details>
    <summary>>>> Problèmes rencontrés</summary>
    <ul>
        <li>Espacement pas assez lisible entre les caractères en morse</li>
        <li>Epreuve du morse sensible à la casse</li>
        <li>Difficulté trop élevée pour les épreuves de plus de 2 étoiles</li>
        <li>Différentes méthodes pour l'épreuve de Network Mapping ne donnaient pas le même résultat</li>
        <li>Trop d'éléments dans l'épreuve Grocery List</li>
        <li>Trop d'éléments dans l'épreuve Compromised User - Peut être flouter les parties non importantes pour une prochaine édition</li>
    </ul>
</details>