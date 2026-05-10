import string
import random

class Weapon:
    def __init__(self):
        self.name = ""
        self.rarity = ""
        self.glyph = ''
        self.color = ""
        self.weapon1 = ""
        self.weapon2 = ""
        self.gemstone = ""
        self.mineral = ""

glyphs = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
colors = ['AMBER', 'BLUE', 'CYAN', 'DANDELION', 'EMERALD', 'FOREST', 'GREY', 'HONEYDEW', 'IVORY', 'JET', 'KHAKI', 'LAVENDER', 'MAROON', 'NAVY', 'OCHRE', 'PINK', 'QUICKSILVER', 'RUST', 'SCARLET', 'TURQUOISE', 'UMBER', 'VIOLET', 'WHITE', 'RANDOM', 'YELLOW', 'ZERO']
weapons1 = ['AXE', 'BOW', 'CLUB', 'DAGGER', 'EXPLOSIVE', 'FLAIL', 'GLAIVE', 'HATCHET', 'ICE PICK', 'JAVELIN', 'KNIFE', 'LANCE', 'MACE', 'NUNCHAKU', 'OAR', 'PISTOL', 'QUARTERSTAFF', 'RAZOR', 'SWORD', 'THROWING KNIFE', 'ULTRASONIC', 'VOLCANO', 'WHIP', 'XIPHOS', 'YO YO', 'ZWEIHANDER']
weapons2 = ['ATLATL', 'BALLISTA', 'CALTROP', 'DOUBLE BARREL', 'EMP', 'FLAMETHROWER', 'GUN', 'HARPOON', 'ION CANNON', 'JACKHAMMER', 'KATANA', 'LASER', 'MUSIC', 'NET GUN', 'OCCULT KNIFE', 'PICKAXE', 'QUICKSILVER', 'ROCKET', 'SCYTHE', 'TRIDENT', 'UZI', 'VARIABLE', 'WAND', 'X RAY', 'YARI', 'ZONE']
gemstones = ['AMETHYST', 'BLOODSTONE', 'CINNABAR', 'DIAMOND', 'EMERALD', 'FLUORITE', 'GOLD', 'HAUYNE', 'IRIDIUM', 'JADE', 'KYANITE', 'LARIMAR', 'MALACHITE', 'NEPTUNITE', 'OBSIDIAN', 'PEARL', 'QUARTZ', 'RUBY', 'SAPPHIRE', 'TOURMALINE', 'ULEXITE', 'VANADINITE', 'WAVELLITE', 'XONOTLITE', 'YUGAWARALITE', 'ZIRCON']
minerals = ['ASBESTOS', 'BISMUTH', 'CALCITE', 'DYSPROSIUM', 'ERYTHRITE', 'FELDSPAR', 'GADOLINITE', 'HEMATITE', 'ICE', 'JASPER', 'KRUT\'AITE', 'LOPEZITE', 'MAGNETITE', 'NICKEL', 'OTAVITE', 'PUMICE', 'QUETZALCOATLITE', 'RHENIITE', 'SILVER', 'TITANITE', 'URANINITE', 'VILLIAUMITE', 'WULFENITE', 'XENOTIME', 'YOSHIOKAITE', 'ZABUYELITE']
rarities = ['COMMON', 'UNCOMMON', 'RARE', 'EPIC', 'LEGENDARY', 'MYTHIC']
weights = [60, 25, 10, 4, 0.9, 0.1]

glyph_to_color = dict(zip(glyphs, colors))
glyph_to_weapon1 = dict(zip(glyphs, weapons1))
glyph_to_weapon2 = dict(zip(glyphs, weapons2))
glyph_to_gemstone = dict(zip(glyphs, gemstones))
glyph_to_mineral = dict(zip(glyphs, minerals))


length = 12
random_string = ''.join(random.choices(string.ascii_uppercase, k=length))

#random_string = "OZWHDLZTXRQG"

indiv_rng = random.Random(random_string)

weapon = Weapon()
weapon.name = random_string
weapon.rarity = indiv_rng.choices(rarities, weights=weights, k=1)[0]
weapon.glyph = random_string[0]
weapon.color = glyph_to_color[random_string[-1]]
weapon.weapon1 = glyph_to_weapon1[random_string[0]]
weapon.weapon2 = glyph_to_weapon2[random_string[1]]
#weapon.gemstone = glyph_to_gemstone[indiv_rng.choice(random_string)]
#weapon.mineral = glyph_to_mineral[indiv_rng.choice(random_string)]

print(f"Weapon Name: {weapon.name}")
print(f"Rarity: {weapon.rarity}")
print(f"Glyph: {weapon.glyph}")
print(f"Color: {weapon.color}")
print(f"Weapon1: {weapon.weapon1}")
print(f"Weapon2: {weapon.weapon2}")
print(f"Gemstone: {weapon.gemstone}")
print(f"Mineral: {weapon.mineral}")