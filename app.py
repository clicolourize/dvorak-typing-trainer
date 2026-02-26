from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

DVORAK_KEYS = {
    '`': '`', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5',
    '6': '6', '7': '7', '8': '8', '9': '9', '0': '0', '-': '-', '=': '=',
    'q': "'", 'w': ',', 'e': '.', 'r': 'p', 't': 'y', 'y': 'f', 'u': 'g',
    'i': 'c', 'o': 'r', 'p': 'l', '[': '/', ']': '\\', '\\': '=',
    'a': 'o', 's': 'e', 'd': 'u', 'f': 'i', 'g': 'd', 'h': 'h', 'j': 't',
    'k': 'n', 'l': 's', ';': '-', "'": ';',
    'z': 'a', 'x': 'q', 'c': 'j', 'v': 'k', 'b': 'x', 'n': 'b', 'm': 'm',
    ',': 'w', '.': 'v', '/': 'z', ' ': ' '
}

DVORAK_TO_QWERTY = {
    '`': '`', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5',
    '6': '6', '7': '7', '8': '8', '9': '9', '0': '0', '-': "'", '=': '=',
    "'": 'q', ',': 'w', '.': 'e', 'p': 'r', 'y': 't', 'f': 'y', 'g': 'u',
    'c': 'i', 'r': 'o', 'l': 'p', '/': '[', '\\': ']',
    'o': 's', 'e': 'd', 'u': 'f', 'i': 'g', 'd': 'h', 'h': 'j', 't': 'k',
    'n': 'l', 's': ';', ';': 'z',
    'a': 'a', 'q': 'x', 'j': 'c', 'k': 'v', 'x': 'b', 'b': 'n', 'm': 'm',
    'w': ',', 'v': '.', 'z': '/', ' ': ' '
}

HOME_ROW_DVORAK = ['a', 'o', 'e', 'u', 'i', 'd', 'h', 't', 'n', 's']

QWERTY_TO_DVORAK = {
    '`': '`', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5',
    '6': '6', '7': '7', '8': '8', '9': '9', '0': '0', '-': '-', '=': '=',
    'q': "'", 'w': ',', 'e': '.', 'r': 'p', 't': 'y', 'y': 'f', 'u': 'g',
    'i': 'c', 'o': 'r', 'p': 'l', '[': '/', ']': '\\', '\\': '=',
    'a': 'o', 's': 'e', 'd': 'u', 'f': 'i', 'g': 'd', 'h': 'h', 'j': 't',
    'k': 'n', 'l': 's', ';': '-', "'": ';',
    'z': 'a', 'x': 'q', 'c': 'j', 'v': 'k', 'b': 'x', 'n': 'b', 'm': 'm',
    ',': 'w', '.': 'v', '/': 'z', ' ': ' '
}

LESSONS_2_LETTER = [
    {"pattern": "ao", "name": "Home Row - Left Hand"},
    {"pattern": "oe", "name": "Home Row - Right Hand"},
    {"pattern": "eo", "name": "Home Row Mix"},
    {"pattern": "uu", "name": "U Key Practice"},
    {"pattern": "ie", "name": "I and E Keys"},
    {"pattern": "id", "name": "I and D Keys"},
    {"pattern": "ht", "name": "H and T Keys"},
    {"pattern": "tn", "name": "T and N Keys"},
    {"pattern": "ns", "name": "N and S Keys"},
    {"pattern": "sh", "name": "S and H Keys"},
    {"pattern": "dn", "name": "D and N Keys"},
    {"pattern": "df", "name": "D and F Keys"},
    {"pattern": "fg", "name": "F and G Keys"},
    {"pattern": "gy", "name": "G and Y Keys"},
    {"pattern": "yp", "name": "Y and P Keys"},
    {"pattern": "pl", "name": "P and L Keys"},
    {"pattern": "lr", "name": "L and R Keys"},
    {"pattern": "rc", "name": "R and C Keys"},
    {"pattern": "c.", "name": "C and Period"},
    {"pattern": ",", "name": "Comma Practice"},
]

LESSONS_4_LETTER = [
    {"pattern": "etun", "name": "E T U N"},
    {"pattern": "aoid", "name": "A O I D"},
    {"pattern": "ehst", "name": "E H S T"},
    {"pattern": "uihn", "name": "U I H N"},
    {"pattern": "odht", "name": "O D H T"},
    {"pattern": "euna", "name": "E U N A"},
    {"pattern": "oids", "name": "O I D S"},
    {"pattern": "uhtn", "name": "U H T N"},
    {"pattern": "aoin", "name": "A O I N"},
    {"pattern": "ehus", "name": "E H U S"},
    {"pattern": "oadt", "name": "O A D T"},
    {"pattern": "iuhs", "name": "I U H S"},
    {"pattern": "daot", "name": "D A O T"},
    {"pattern": "hnse", "name": "H N S E"},
    {"pattern": "tuia", "name": "T U I A"},
    {"pattern": "sohd", "name": "S O H D"},
    {"pattern": "natu", "name": "N A T U"},
    {"pattern": "eiao", "name": "E I A O"},
    {"pattern": "dhtn", "name": "D H T N"},
    {"pattern": "sneo", "name": "S N E O"},
    {"pattern": "fhjk", "name": "F H J K"},
    {"pattern": "lpcr", "name": "L P C R"},
    {"pattern": "yfgc", "name": "Y F G C"},
    {"pattern": "aqjx", "name": "A Q J X"},
    {"pattern": "mv bw", "name": "M V B W"},
    {"pattern": "zx bv", "name": "Z X B V"},
]

LESSONS_WORDS = [
    {"pattern": "the and ", "name": "the, and"},
    {"pattern": "of to in ", "name": "of, to, in"},
    {"pattern": "is it that ", "name": "is, it, that"},
    {"pattern": "for as with ", "name": "for, as, with"},
    {"pattern": "his her they ", "name": "his, her, they"},
    {"pattern": "at be by on ", "name": "at, be, by, on"},
    {"pattern": "not we but or ", "name": "not, we, but, or"},
    {"pattern": "all can had her ", "name": "all, can, had, her"},
    {"pattern": "was one our out ", "name": "was, one, our, out"},
    {"pattern": "day are have made ", "name": "day, are, have, made"},
    {"pattern": "from go get when ", "name": "from, go, get, when"},
    {"pattern": "if make just know ", "name": "if, make, just, know"},
    {"pattern": "take see than into ", "name": "take, see, than, into"},
    {"pattern": "come back good want ", "name": "come, back, good, want"},
    {"pattern": "give over most also ", "name": "give, over, most, also"},
    {"pattern": "after find long down ", "name": "after, find, long, down"},
    {"pattern": "been call other could ", "name": "been, call, other, could"},
    {"pattern": "first time many may ", "name": "first, time, many, may"},
    {"pattern": "then do two more ", "name": "then, do, two, more"},
    {"pattern": "way new work such no ", "name": "way, new, work, such, no"},
]

FRENCH_TEXTS = {
    "easy": [
        "Le chat est sur le lit. Il est noir et blanc. Le chat dort beaucoup. Il aime manger du poisson. Le chat est doux. Le chat est calme. Le chat est gentil. Le chat est mignon. Le chat est blanc. Le chat est noir. Le chat est gris. Le chat est roux. Le chat mange. Le chat boit. Le chat joue. Le chat court. Le chat saute. Le chat dort. Le chat voit. Le chat entend. Le chat sent. Le chat touche. Le chat est là. Le chat est là. Le chat est là. Le chat est là. Le chat est là. Le chat est là. Le chat est là. Le chat est là. Le chat est là. Le chat est là. Le chat est là. Le chat est là. Le chat est là. Le chat est là. Le chat est là. Le chat est là. Le chat est là. Le chat est là. Le chat est là. Le chat est là. Le chat est là.",
        "Un chien court dans le jardin. Le chien est content. Il joue avec la balle. Le maître rit. Le chien est grand. Le chien est petit. Le chien est brun. Le chien est blanc. Le chien est noir. Le chien est gris. Le chien aboie. Le chien mord. Le chien court. Le chien saute. Le chien mange. Le chien boit. Le chien dort. Le chien joue. Le chien sent. Le chien voit. Le chien entend. Le chien est là. Le chien est là. Le chien est là. Le chien est là. Le chien est là. Le chien est là. Le chien est là. Le chien est là. Le chien est là. Le chien est là. Le chien est là. Le chien est là. Le chien est là. Le chien est là. Le chien est là. Le chien est là. Le chien est là. Le chien est là. Le chien est là.",
        "La maison est grande. Il y a trois chambres. La porte est bleue. Le soleil brille. La maison est belle. La maison est vieille. La maison est nouvelle. La maison est haute. La maison est basse. La maison a un toit. La maison a des murs. La maison a des portes. La maison a des fenêtres. La maison a un jardin. La maison a une cuisine. La maison a une salle. La maison a une cave. La maison a un grenier. La maison est là. La maison est là. La maison est là. La maison est là. La maison est là. La maison est là. La maison est là. La maison est là. La maison est là. La maison est là. La maison est là. La maison est là. La maison est là.",
        "Je mange une pomme rouge. Elle est douce et bonne. J'aime les fruits. Ils sont frais. Je mange une orange. Je mange une banane. Je mange une fraise. Je mange un raisin. Je mange une tomate. Je mange une carotte. Je mange une salade. Je mange du pain. Je mange du fromage. Je mange de la viande. Je bois du lait. Je bois de l'eau. Je bois du jus. Je bois du café. Je bois du thé. Le fruit est bon. Le fruit est frais. Le fruit est mûr. Le fruit est sucré. Le fruit est juteux. Le fruit est rouge. Le fruit est vert. Le fruit est jaune. Le fruit est orange.",
        "Le père lit un livre. La mère cuisine. L'enfant dessine. La famille est ensemble. Le père est grand. Le père est fort. Le père est bon. Le père est gentil. La mère est belle. La mère est douce. La mère est bonne. La mère est gentille. L'enfant est petit. L'enfant est mignon. L'enfant est sage. L'enfant est intelligent. La famille est grande. La famille est unie. La famille est heureu se. Le père travaille. La mère travaille. L'enfant étudie. Le père lit. La mère cuisine. L'enfant dessine. Le père court. La mère saute. L'enfant joue. Le père mange. La mère mange. L'enfant mange. Le père boit. La mère boit."
    ],
    "medium": [
        "Un lapin mignon est allé sur la lune. La lune était faite de fromage! Le lapin a mangé et mangé. Puis le lapin a couru vers une fusée. Le lapin était blanc. Le lapin était gris. Le lapin était noir. Le lapin était brun. Le lapin saute haut. Le lapin court vite. Le lapin mange des carottes. Le lapin mange de l'herbe. Le lapin boit de l'eau. Le lapin dort beaucoup. Le lapin est mignon. Le lapin est gentil. Le lapin est doux. Le lapin est calme. Le lapin est rapide. Le lapin est courageux. Le lapin est intelligent. Le lapin est rusé. Le lapin est malin. Le lapin est joueur. Le lapin est curieux. Le lapin est brave. Le lapin est fort. Le lapin est faible. Le lapin est grand.",
        "Il était une fois un petit canard qui voulait apprendre à nager. Elle a essayé et essayé. Un jour, un grand poisson l'a aidée. Le canard était petit. Le canard était jaune. Le canard était mignon. Le canard voulait nager. Le canard voulait voler. Le canard voulait plonger. Le canard pouvait nager. Le canard pouvait voler. Le canard pouvait plonger. Le canard était content. Le canard était heureux. Le canard était triste. Le canard était fatigué. Le canard était affamé. Le canard était assoiffé. Le canard mange du pain. Le canard mange des grains. Le canard mange des vers. Le canard mange des algues. Le canard boit de l'eau. Le canard booze de la boue. Le canard nage dans l'eau. Le canard vole dans le ciel.",
        "Le zèbre a couru au magasin pour acheter des bonbons. Les bonbons étaient délicieux et sucrés. Le zèbre a partagé avec un ami. Le zèbre était rayé. Le zèbre était blanc. Le zèbre était noir. Le zèbre court très vite. Le zèbre saute haut. Le zèbre mange de l'herbe. Le zèbre booze de l'eau. Le zèbre dort debout. Le zèbre est sauvage. Le zèbre est rapide. Le zèbre est fort. Le zèbre est brave. Le zèbre est beau. Le zèbre est grand. Le zèbre est petit. Le zèbre est jeune. Le zèbre est vieux. Le zèbre est mignon. Le zèbre est gentil. Le zèbre est doux. Le zèbre est calme. Le zèbre est rapide. Le zèbre est courageux. Le zèbre est intelligent.",
        "Une tortue aimait les pizzas. Chaque jour elle commandait une grande pizza au fromage. La pizza est la meilleure nourriture! La tortue était verte. La tortue était lente. La tortue était sage. La tortue était intelligente. La tortue aimait les pizzas. La tortue aimait les fromages. La tortue aimait les tomates. La tortue aimait les champignons. La tortue aimait les olives. La tortue aimait les pepperonis. La tortue aimait les anchois. La tortue commandait des pizzas. La tortue mangeait des pizzas. La tortue dévorait des pizzas. La tortue appréciée les pizzas. La tortue était satisfaite. La tortue était heureu se. La tortue était rassasiée. La tortue était repue. La tortue dormait. La tortue rêvait. La tortue marchait. La tortue nagait. La tortue plongeait. La tortue sortait.",
        "Le robot est allé à la plage. Le soleil était chaud. Le robot s'est refroidi avec une glace. Ensuite le robot a construit un château de sable. Le robot était métallique. Le robot était brillant. Le robot était neuf. Le robot était vieux. Le robot marchait. Le robot courait. Le robot sautait. Le robot dansait. Le robot travaillait. Le robot réfléchissait. Le robot parlait. Le robot écoutait. Le robot voyait. Le robot entendait. Le robot sentait. Le robot touchait. Le robot était content. Le robot était triste. Le robot était fatigué. Le robot était heureux. Le robot était malaisé. Le robot était chaud. Le robot était froid. Le robot était blème. Le robot était rouge. Le robot mangeait. Le robot buvait. Le robot dormait."
    ],
    "hard": [
        "Portez ce vieux whisky au juge blond qui fume. Mon ami fait du très bon travail. Les français peuvent réciter tous les alphabets avec des phrases amusantes et rapides. Le juge est blond. Le juge est sévère. Le juge est juste. Le juge est sage. Le juge est intelligent. Le whisky est vieux. Le whisky est bon. Le whisky est excellent. Le whisky est précieux. Le whisky est rare. Le travail est difficile. Le travail est facile. Le travail est intéressant. Le travail est important. Le travail est urgent. Les français sont intelligents. Les français sont créatifs. Les français sont drôles. Les français sont sympas. Les français sont gentils. L'alphabet est long. L'alphabet est court. L'alphabet est compliqué. L'alphabet est simple. La phrase est longue. La phrase est courte. La phrase est drôle. La phrase est sérieuse. Le juge fume la pipe. Le juge fume le cigare. Le juge fume la cigarette. Le whisky est dans le verre. Le juge prend le whisky.",
        "Mon île est froide mais quand même délicieux. Les français peuvent réciter l'alphabet avec des phrases drôles et promptes. L'île est froide. L'île est chaude. L'île est grande. L'île est petite. L'île est belle. L'île est magnifique. Le climat est froid. Le climat est chaud. Le climat est tempéré. Le climat est tropical. Le climat est polaire. Les français sont variés. Les français sont divers. Les français sont nombreux. Les français sont peu nombreux. La phrase est drôle. La phrase est sérieuse. La phrase est intéressante. La phrase est longue. La phrase est courte. La phrase est complexe. La phrase est simple. L'alphabet français est long. L'alphabet français est compliqué. L'alphabet français est intéressant. Mon île est délicieux. Mon île est belle. Mon île est magnifique. Mon île est romantique. Mon île est sauvage.",
        "Voyez le brick gros Jean qui pète plus haut que le cul. Ça sera dans notre poche, pas dans la sienne. Le travail bien fait rapporte toujours. Le brick est gros. Le brick est lourd. Le brick est léger. Le brick est grand. Le brick est petit. Jean est grand. Jean est petit. Jean est gros. Jean est mince. Jean est fort. Jean est faible. Le pète est fort. Le pète est faible. Le pète est drôle. Le pète est gênant. La poche est pleine. La poche est vide. La poche est grande. La poche est petite. Le travail est fait. Le travail est bien fait. Le travail est mal fait. Le travail est terminé. Le travail commence. Le travail continue. Le résultat est bon. Le résultat est mauvais. Le résultat est excellent. Le résultat est médiocre. Le travail rapporte. Le travail paie. Le travail coûte. Le travail vaut.",
        "Les français disent ça gaze entre les copains. Un ninja très rapide bâtit des records dans la forêt. Vraiment très chaud ici ce soir. Les français parlent. Les français écoutent. Les français discutent. Les français débattent. Les français conviennent. Le ninja est rapide. Le ninja est silencieux. Le ninja est secret. Le ninja est mystérieux. Le ninja est courageux. Le ninja est fort. Le ninja est faible. Le ninja bâtit. Le ninja détruit. Le ninja construit. Le ninja répare. Le record est battu. Le record est établi. Le record est nouveau. Le record est ancien. La forêt est grande. La forêt est profonde. La forêt est sombre. La forêt est claire. La forêt est dense. Ce soir il fait chaud. Ce soir il fait froid. Ce soir il fait beau. Ce soir il fait mauvais. Vraiment c'est incroyable.",
        "Les Wagoners font un safari dans la jungle. Le soleil brille fort. Mon vieux scooter est cassé depuis plusieurs semaines. Les Wagoners voyagent. Les Wagoners explorent. Les Wagoners découvrent. Les Wagoners photographient. Les Wagoners apprécient. Le safari est passionnant. Le safari est intéressant. Le safari est dangereux. Le safari est une aventure. Le soleil brille. Le soleil luit. Le soleil éclaire. Le soleil réchauffe. Le vieux scooter est cassé. Le vieux scooter est abimé. Le vieux scooter est usé. Le vieux scooter est vieux. Plusieurs semaines passent. Plusieurs jours passent. Plusieurs mois passent. Le scooter ne marche pas. Le scooter ne fonctionne pas. Le scooter est en panne. Le scooter a besoin de réparation. Le scooter doit être réparé. Le scooter doit être remorqué."
    ]
}

SPANISH_TEXTS = {
    "easy": [
        "El gato está en la cama. Es negro y blanco. El gato duerme mucho. Le gusta comer pescado. El gato es suave. El gato es calmo. El gato es amable. El gato es lindo. El gato es blanco. El gato es negro. El gato es gris. El gato come. El gato bebe. El gato juega. El gato corre. El gato salta. El gato duerme. El gato ve. El gato oye. El gato huele. El gato toca. El gato está aquí. El gato está allá. El gato está allá. El gato está allá. El gato está allá. El gato está allá. El gato está allá. El gato está allá. El gato está allá. El gato está allá. El gato está allá. El gato está allá. El gato está allá. El gato está allá. El gato está allá. El gato está allá. El gato está allá. El gato está allá. El gato está allá.",
        "Un perro corre en el jardín. El perro está feliz. Juega con la pelota. El amo ríe. El perro es grande. El perro es pequeño. El perro es moreno. El perro es blanco. El perro es negro. El perro ladra. El perro muerde. El perro corre. El perro salta. El perro come. El perro bebe. El perro duerme. El perro juega. El perro huele. El perro ve. El perro oye. El perro está aquí. El perro está allá. El perro está allá. El perro está allá. El perro está allá. El perro está allá. El perro está allá. El perro está allá. El perro está allá. El perro está allá. El perro está allá. El perro está allá. El perro está allá. El perro está allá. El perro está allá. El perro está allá. El perro está allá. El perro está allá. El perro está allá.",
        "La casa es grande. Hay tres habitaciones. La puerta es azul. El sol brilla. La casa es bella. La casa es vieja. La casa es nueva. La casa es alta. La casa es baja. La casa tiene un techo. La casa tiene paredes. La casa tiene puertas. La casa tiene ventanas. La casa tiene un jardín. La casa tiene una cocina. La casa tiene un salón. La casa tiene un sótano. La casa tiene un ático. La casa está ahí. La casa está ahí. La casa está ahí. La casa está ahí. La casa está ahí. La casa está ahí. La casa está ahí. La casa está ahí. La casa está ahí. La casa está ahí. La casa está ahí. La casa está ahí. La casa está ahí.",
        "Yo como una manzana roja. Es dulce y buena. Me gusta la fruta. Está fresca. Yo como una naranja. Yo como un plátano. Yo como una fresa. Yo como una uva. Yo como un tomate. Yo como una zanahoria. Yo como una ensalada. Yo como pan. Yo como queso. Yo como carne. Yo bebo leche. Yo bebo agua. Yo bebo jugos. Yo bebo café. Yo bebo té. La fruta es buena. La fruta es fresca. La fruta está madura. La fruta es dulce. La fruta es jugosa. La fruta es roja. La fruta es verde. La fruta es amarilla. La fruta es naranja.",
        "El padre lee un libro. La madre cocina. El niño dibuja. La familia está junta. El padre es alto. El padre es fuerte. El padre es bueno. El padre es amable. La madre es bella. La madre es dulce. La madre es buena. La madre es amable. El niño es pequeño. El niño es lindo. El niño es obediente. El niño es inteligente. La familia es grande. La familia está unite. La familia es feliz. El padre trabaja. La madre trabaja. El niño estudia. El padre lee. La madre cocina. El niño dibuja. El padre corre. La madre salta. El niño juega. El padre come. La madre come. El niño come. El padre bebe. La madre bebe."
    ],
    "medium": [
        "Un conejo divertido fue a la luna. La luna estaba hecha de queso. El conejo comió y comió. Luego el conejo corrió hacia un cohete. El conejo era blanco. El conejo era gris. El conejo era negro. El conejo era marrón. El conejo salta alto. El conejo corre rápido. El conejo come zanahorias. El conejo come pasto. El conejo bebe agua. El conejo duerme mucho. El conejo es lindo. El conejo es amable. El conejo es dulce. El conejo es calmo. El conejo es rápido. El conejo es valiente. El conejo es inteligente. El conejo es astuto. El conejo es vivo. El conejo es juguetón. El conejo es valiente. El conejo es fuerte. El conejo es débil. El conejo es grande.",
        "Había una vez un patito que quería aprender a volar. Intentó y tentou. Un día, un pájaro grande ayudó al patito. El patito era pequeño. El patito era amarillo. El patito era lindo. El patito quería volar. El patito quería nadar. El patito quería bucear. El patito podía nadar. El patito podía volar. El patito podía bucear. El patito estaba feliz. El patito estaba triste. El patito estaba cansado. El patito estaba hambriento. El patito estaba sediento. El patito come pan. El patito come semillas. El patito come gusanos. El patito come algas. El patito bebe agua. El patito bebe lodo. El patito nada en el agua. El patito vuela en el cielo.",
        "La cebra corrió a la tienda para comprar dulces. Los dulces estaban deliciosos y dulces. La cebra compartió con un amigo. La cebra era rayada. La cebra era blanca. La cebra era negra. La cebra corre muy rápido. La cebra salta alto. La cebra come pasto. La cebra bebe agua. La cebra duerme de pie. La cebra es salvaje. La cebra es rápida. La cebra es fuerte. La cebra es valiente. La cebra es hermosa. La cebra es grande. La cebra es pequeña. La cebra es joven. La cebra es vieja. La cebra es linda. La cebra es amable. La cebra es dulce. La cebra es calmo. La cebra es rápida. La cebra es valiente. La cebra es inteligente.",
        "Una tortuga amaba las pizzas. Cada día ordenaba una pizza grande con queso. La pizza es la mejor comida! La tortuga era verde. La tortuga era lenta. La tortuga era sabia. La tortuga era inteligente. La tortuga amaba las pizzas. La tortuga amaba los quesos. La tortuga amaba los tomates. La tortuga amaba los champiñones. La tortuga amaba las aceitunas. La tortuga amaba los pepperonis. La tortuga ordenaba pizzas. La tortuga comía pizzas. La tortuga devoraba pizzas. La tortuga apreciaba las pizzas. La tortuga estaba contenta. La tortuga estaba feliz. La tortuga estaba satisfecha. La tortuga estaba llena. La tortuga dormía. La tortuga soñaba. La tortuga caminaba. La tortuga nadaba. La tortuga buceaba. La tortuga salía.",
        "El robot fue a la playa. El sol estaba caliente. El robot se enfrío con un helado. Luego el robot construyó un castillo de arena. El robot era metálico. El robot era brillante. El robot era nuevo. El robot era viejo. El robot camina. El robot corre. El robot salta. El robot dança. El robot trabaja. El robot piensa. El robot habla. El robot escucha. El robot ve. El robot oye. El robot huele. El robot toca. El robot está contenta. El robot está triste. El robot está cansado. El robot está feliz. El robot está mal. El robot está caliente. El robot está frío. El robot está rojo. El robot come. El robot bebe. El robot duerme."
    ],
    "hard": [
        "El veloz murciélago hindú comía feliz cardillo y kiwi. La cigüeña tocaba el saxofón detrás del palenque de paja. El murciélago vuela de noche. El murciélago come frutas. El murciélago vive en cuevas. El murciélago es un mamífero. El murciélago tiene alas. El murciélago usa la ecolocación. La cigüeña toca el saxofón. La cigüeña es un pájaro. La cigüeña tiene largas patas. La cigüeña vive cerca del agua. La cigüeña come peces. La cigüeña vuela alto. El volcan está activo. El volcan está dormido. El volcan tiene lava. El volcan tiene ceniza. El volcan está caliente. El ninja es rápido. El ninja es silencioso. El ninja es secreto. El ninja es misterioso. El ninja es valiente. El ninja es fuerte. El ninja es débil. El ninja eliminó. El ninja destroyó. El ninja construyó. El ninja reparó. La selva es grande. La selva es densa. La selva es verde. La selva tiene muchos animales.",
        "El zorro café salta sobre el perro perezoso. El trabajo requiere mucho esfuerzo y energía de cada trabajador joven. El zorro es astuto. El zorro es listo. El zorro es inteligente. El zorro es rápido. El zorro es valiente. El zorro es cauteloso. El zorro café es color café. El zorro café es hermoso. El zorro café es elegante. El perro perezoso duerme mucho. El perro perezoso es relajado. El perro perezoso es tranquillo. El perro perezoso es calmado. El perro perezoso es perezoso. El trabajo requiere esfuerzo. El trabajo requiere energía. El trabajo requiere tiempo. El trabajo requiere dedicación. El trabajo requiere paciencia. El trabajo requiere fuerza. El trabajador es joven. El trabajador es fuerte. El trabajador es valiente. El trabajador es inteligente. El trabajador es trabajador. El trabajador es amable.",
        "La cigüeña tocaba el violín detrás del volcán. El ninja rápido eliminó a todos los enemigos en la selva. La cigüeña toca el violín. La cigüeña es un pájaro. La cigüeña tiene largas patas. La cigüeña vive cerca del agua. La cigüeña come peces. La cigüeña vuela alto. El volcan está activo. El volcan está dormido. El volcan tiene lava. El volcan tiene ceniza. El volcan está caliente. El ninja es rápido. El ninja es silencioso. El ninja es secreto. El ninja es misterioso. El ninja es valiente. El ninja es fuerte. El ninja es débil. El ninja eliminó. El ninja destroyó. El ninja construyó. El ninja reparó. La selva es grande. La selva es densa. La selva es verde. La selva tiene muchos animales. La selva tiene muchos colores.",
        "El ninja veloz boxea rápidamente. El mago debe trabajar rápidamente en la computadora. El sol brilla sobre la montaña. El ninja boxea. El ninja pega. El ninja golpea. El ninja esquiva. El ninja defensa. El ninja ataca. El ninja es veloz. El ninja es rápido. El ninja es veloz. El mago trabaja. El mago estudia. El mago aprende. El mago enseña. El mago crea. El mago destruye. El mago debe trabajar. El mago necesita trabajar. El mago tiene que trabajar. La computadora es moderna. La computadora es rápida. La computadora es lenta. La computadora es nueva. La computadora es vieja. El sol brilla. El sol alumbra. El sol calienta. El sol brilla fuerte. El sol está alto. La montaña es alta. La montaña es grande. La montaña tiene nieve. La montaña tiene piedra.",
        "Las montañas son muy altas. Los ríos fluyen hacia el mar. Los pájaros cantan en los árboles. La vida es hermosa. Las montañas son altas. Las montañas son grandes. Las montañas son majestuosas. Las montañas tienen nieve. Las montañas tienen picos. Las montañas tienen valles. Los ríos fluyen. Los ríos corriente. Los ríos van al mar. Los ríos son largos. Los ríos son anchos. Los pájaros cantan. Los pájaros vuelan. Los pájaros construyen nidos. Los pájaros buscan comida. Los pájaros crían hijos. Los árboles son verdes. Los árboles tienen hojas. Los árboles dan sombra. Los árboles producen oxígeno. La vida es hermosa. La vida es bella. La vida es maravillosa. La vida es un regalo. La vida es preciada."
    ]
}

TEXTS = {
    "easy": [
        "The cat sat on a hat. It was a fat cat. The cat ran to a pan. It can hop. Hop, cat, hop! The cat is fat. The cat can run. The cat can sit. The cat can hit. The cat is in a rut. The cat can nip. The cat can sip. The cat can rip. The cat is lit. The cat can bit. The cat can fit. The cat is wit. The cat has wit. The cat has hit. The cat has sit. The cat has lit. The cat has bit. The cat has fit. The cat has wit. The cat has it. The cat has a. The cat has hit a sit. The cat has a lit. The cat has a bit. The cat has a fit. The cat has a wit. The cat has it. The cat has at. The cat has an it. The cat has an at. The cat has an am. The cat has an is. The cat has an as. The cat has an us. The cat has an if. The cat has an of. The cat has an on. The cat has an in. The cat has an to. The cat has an so. The cat has an no. The cat has an go. The cat has an do. The cat has an be. The cat has an am. The cat has an is. The cat has an as. The cat has an us. The cat has an if. The cat has an of. The cat has an on. The cat has an in. The cat has an to. The cat has an so. The cat has an no. The cat has an go. The cat has an do. The cat has an be.",
        "A bug ran on a rug. The bug can run. It ran to a cup. The bug is in the cup now. The bug is big. The bug is red. The bug has a leg. The bug has a web. The bug can rub. The bug can tub. The bug can sub. The bug can bub. The bug can cub. The bug can dub. The bug can hub. The bug can rub. The bug can tub. The bug can sub. The bug has a dad. The bug has a mom. The bug has a pet. The bug has a net. The bug has a vet. The bug has a bet. The bug has a jet. The bug has a let. The bug has a met. The bug has a net. The bug has a set. The bug has a wet. The bug has a yet. The bug has a get. The bug has a bet. The bug has a let. The bug has a met. The bug has a net. The bug has a set. The bug has a wet.",
        "The sun is up. The sky is blue. I see a bird. The bird can sing. Sing, bird, sing! The sun is hot. The sky is clear. I see a plane. The plane can fly. Fly, plane, fly! The sun is warm. The sky is gray. I see a cloud. The cloud can float. Float, cloud, float! The sun is bright. The sky is dark. I see a star. The star can shine. Shine, star, shine! The sun is red. The sky is red. I see a moon. The moon can glow. Glow, moon, glow! The sun is up. The sky is blue. I see a bird. The bird can sing. Sing, bird, sing!",
        "I can run and jump. I can hop and sit. I like to run. Run, run, run! I can swim and dive. I can splash and play. I like to swim. Swim, swim, swim! I can walk and talk. I can laugh and cry. I like to walk. Walk, walk, walk! I can read and write. I can think and dream. I like to read. Read, read, read! I can sing and dance. I can clap and sway. I like to sing. Sing, sing, sing! I can eat and drink. I can chew and sip. I like to eat. Eat, eat, eat!",
        "A pig can dig. The pig is big. It dug a hole. The hole is deep. Dig, pig, dig! A dog can wag. The dog is glad. It wagged its tail. Wag, dog, wag! A frog can leap. The frog is green. It leaped a stream. Leap, frog, leap! A bear can growl. The bear is brown. It growled at me. Growl, bear, growl! A duck can quack. The duck is white. It quacked at night. Quack, duck, quack! A cow can moo. The cow is black. It mooed at me. Moo, cow, moo! A sheep can baa. The sheep is wool. It baed at dawn. Baa, sheep, baa!"
    ],
    "medium": [
        "A funny bunny went to the moon. The moon was made of cheese! The bunny ate and ate. Then the bunny ran to a rocket. The rocket went zip-zap! Now the bunny is home. Home is where the carrot is. Eat, bunny, eat! The bunny was hungry. The bunny was happy. The bunny was silly. The bunny was funny. The bunny was cute. The bunny was sweet. The bunny was kind. The bunny was smart. The bunny was brave. The bunny was fast. The bunny was strong. The bunny was cool. The bunny was hot. The bunny was cold. The bunny was new. The bunny was old. The bunny was red. The bunny was blue. The bunny was green. The bunny was pink. The bunny was purple. The bunny was orange. The bunny was yellow. The bunny was brown. The bunny was black. The bunny was white. The bunny was gray.",
        "Once upon a time, a little duck wanted to learn to fly. It tried and tried, but it could only hop. One day, a big bird helped the duck. Now the duck can fly high in the sky! The duck was small. The duck was yellow. The duck was cute. The duck was sweet. The duck was kind. The duck was gentle. The duck was brave. The duck was bold. The duck was shy. The duck was quiet. The duck was loud. The duck was fast. The duck was slow. The duck was happy. The duck was sad. The duck was tired. The duck was awake. The duck was hungry. The duck was thirsty. The duck was full. The duck was silly. The duck was funny. The duck was smart. The duck was wise. The duck was clever. The duck was quick.",
        "The zebra ran to the store to buy some candy. The candy was yummy and sweet. The zebra shared with a friend. They danced and played all day long. The zebra was striped. The zebra was fast. The zebra was brave. The zebra was bold. The zebra was kind. The zebra was sweet. The zebra was nice. The zebra was good. The zebra was great. The zebra was cool. The zebra was hot. The zebra was warm. The zebra was cold. The zebra was happy. The zebra was sad. The zebra was tired. The zebra was awake. The zebra was hungry. The zebra was full. The zebra was silly. The zebra was funny. The zebra was smart. The zebra was wise. The zebra was clever. The zebra was quick.",
        "A ninja turtle loved to eat pizza. Every day he ordered a large pepperoni pizza. He also liked cheese pizza. Pizza is the best food ever! The turtle was green. The turtle was slow. The turtle was wise. The turtle was smart. The turtle was kind. The turtle was brave. The turtle was strong. The turtle was cool. The turtle was awesome. The turtle was amazing. The turtle was incredible. The turtle was fantastic. The turtle was wonderful. The turtle was great. The turtle was excellent. The turtle was superb. The turtle was brilliant. The turtle was clever. The turtle was intelligent. The turtle was wise. The turtle was thoughtful. The turtle was careful. The turtle was cautious. The turtle was careful. The turtle was mindful. The turtle was aware.",
        "The robot went to the beach. The sun was hot. The robot cooled down with ice cream. Then the robot built a sandcastle. What a fun day at the beach! The robot was metal. The robot was shiny. The robot was new. The robot was old. The robot was fast. The robot was slow. The robot was strong. The robot was weak. The robot was smart. The robot was silly. The robot was funny. The robot was cool. The robot was hot. The robot was cold. The robot was warm. The robot was happy. The robot was sad. The robot was tired. The robot was awake. The robot was hungry. The robot was full. The robot was ready. The robot was willing. The robot was able. The robot was kind."
    ],
    "hard": [
        "Peter Piper picked a peck of pickled peppers. A peck of pickled peppers Peter Piper picked. Where's the peck of pickled peppers Peter Piper picked? Sally sells seashells by the seashore. She sells yew trees too. The quick brown fox jumps over the lazy dog. How vexingly quick daft zebras jump! The job requires extra pluck and zeal from every young wage earner. If the boy can spell, he may be a great scholar. Few black taxis drive up major roads on hazy quays. Amazingly few discotheques provide jukeboxes. The wizard quickly jinxed five vexing gnomes. Six big devils from beyond eagerly fight the galaxy hero. My jinxed vexu blob-walk quickly spawns extreme quavers. The job requires extra pluck and zeal from every young wage earner. If the boy can spell, he may be a great scholar. Few black taxis drive up major roads on hazy quays.",
        "Amazingly few discotheques provide jukeboxes. The job requires extra pluck and zeal from every young wage earner. If the boy can spell, he may be a great scholar. Few black taxis drive up major roads on hazy quays. Pack my box with five dozen liquor jugs. The quick brown fox jumps over the lazy dog. A wizard's job is to vex chumps quickly in fog. Watch Jeopardy, Alex Trebek's fun TV quiz game! Sphinx of black quartz, judge my vow! Two driven jocks help fax my big quiz. The five boxing wizards jump quickly. Jackdaws love my big sphinx of quartz. Crazy Frederick bought many very exquisite opal jewels! We promptly judged antique ivory buckles for the next prize. A quick movement of the enemy will jeopardize six gunboats. The jay, pig, fox, zebra and my wolves quack!",
        "How vexingly quick daft zebras jump! The five boxing wizards jump quickly. Jackdaws love my big sphinx of quartz. Crazy Frederick bought many very exquisite opal jewels! We promptly judged antique ivory buckles for the next prize. A quick brown fox jumps over the lazy dog. Pack my box with five dozen liquor jugs. The job requires extra pluck and zeal from every young wage earner. If the boy can spell, he may be a great scholar. Amazingly few discotheques provide jukeboxes. Sphinx of black quartz, judge my vow! Two driven jocks help fax my big quiz. The five boxing wizards jump quickly. Jackdaws love my big sphinx of quartz. Crazy Frederick bought many very exquisite opal jewels! We promptly judged antique ivory buckles for the next prize.",
        "Sphinx of black quartz, judge my vow! Two driven jocks help fax my big quiz. The job requires extra pluck and zeal from every young wage earner. If the boy can spell, he may be a great scholar. Amazingly few discotheques provide jukeboxes. The quick brown fox jumps over the lazy dog. A wizard's job is to vex chumps quickly in fog. Watch Jeopardy, Alex Trebek's fun TV quiz game! Pack my box with five dozen liquor jugs. The job requires extra pluck and zeal from every young wage earner. If the boy can spell, he may be a great scholar. Few black taxis drive up major roads on hazy quays. Amazingly few discotheques provide jukeboxes. Sphinx of black quartz, judge my vow! Two driven jocks help fax my big quiz. The five boxing wizards jump quickly. Jackdaws love my big sphinx of quartz.",
        "Pack my box with five dozen liquor jugs. The quick brown fox jumps over the lazy dog. A wizard's job is to vex chumps quickly in fog. Watch Jeopardy, Alex Trebek's fun TV quiz game! The job requires extra pluck and zeal from every young wage earner. If the boy can spell, he may be a great scholar. Few black taxis drive up major roads on hazy quays. Amazingly few discotheques provide jukeboxes. The five boxing wizards jump quickly. Jackdaws love my big sphinx of quartz. Crazy Frederick bought many very exquisite opal jewels! We promptly judged antique ivory buckles for the next prize. Sphinx of black quartz, judge my vow! Two driven jocks help fax my big quiz. How vexingly quick daft zebras jump! The quick brown fox jumps over the lazy dog."
    ]
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/lessons/2letter')
def get_2letter_lessons():
    return jsonify(LESSONS_2_LETTER)

@app.route('/api/lessons/4letter')
def get_4letter_lessons():
    return jsonify(LESSONS_4_LETTER)

@app.route('/api/lessons/words')
def get_words_lessons():
    return jsonify(LESSONS_WORDS)

@app.route('/api/texts')
def get_texts():
    all_texts = {
        "english": TEXTS,
        "french": FRENCH_TEXTS,
        "spanish": SPANISH_TEXTS
    }
    return jsonify(all_texts)

@app.route('/api/keymap')
def get_keymap():
    return jsonify(QWERTY_TO_DVORAK)

@app.route('/api/dvormap')
def get_dvormap():
    return jsonify(DVORAK_TO_QWERTY)

@app.route('/api/homerow')
def get_homerow():
    return jsonify(HOME_ROW_DVORAK)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
