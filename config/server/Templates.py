from erukar.system.engine import Lifeform
from erukar.content.inventory import *
from erukar.content.modifiers.material import *
import erukar


def configure(shard):
    shard.templates = [
        make_devout(),
        make_warrior(),
        make_arcanist(),
        make_deceiver()
    ]

    for template in shard.templates:
        template.skill_points = 0
        template.stat_points = 0
        template.wealth = 200


def make_devout():
    cleric = Lifeform(None)
    cleric.name = 'Cleric'
    cleric.stats = {}
    cleric.stats['strength']  = 3
    cleric.stats['dexterity'] = 1
    cleric.stats['vitality']  = 3
    cleric.stats['acuity']    = 1
    cleric.stats['sense']     = 5
    cleric.stats['resolve']   = 2
    
    cleric.inventory = [
        Mace(modifiers=[Iron]),
        Cuirass(modifiers=[Leather]),
        Leggings(modifiers=[Leather]),
        Boots(modifiers=[Leather]),
        HolyWater(5),
        PotionOfHealing(5),
    ]
    cleric.spell_words = [
    ]

    cleric.skills = [
        erukar.content.skills.SupernaturalSense(),
        erukar.content.skills.Smite()
    ]

    cleric.left  = cleric.inventory[0]
    cleric.chest = cleric.inventory[1]
    cleric.legs  = cleric.inventory[2]
    cleric.feet  = cleric.inventory[3]
    cleric.description = 'Clerics are holy warriors who specialize in purification and sanctification. Clerics use a weapon of their choice and a holy symbol, which provides bonuses while within hallowed areas. They have a strong sense score which allows them to sense otherworldly presences.\nClerics can use holy water or a consecration spell word to purify a room from evil. They also have access to a word which heals and one which persists effects for a duration of time.'

    return cleric

def make_warrior():
    fighter = Lifeform(None)
    fighter.name = 'Fighter'
    fighter.stats = {}
    fighter.stats['strength']  = 5
    fighter.stats['dexterity'] = 2
    fighter.stats['vitality']  = 5
    fighter.stats['acuity']    = 1
    fighter.stats['sense']     = 1
    fighter.stats['resolve']   = 1
    
    fighter.inventory = [
        Longsword(modifiers=[Iron]),
        HeaterShield(modifiers=[Oak]),
        Brigandine(modifiers=[Leather]),
        Leggings(modifiers=[Leather]),
        Boots(modifiers=[Leather]),
        Spear(modifiers=[Iron]),
    ]
    fighter.skills = [
        erukar.content.skills.MartialWeaponTraining(),
        erukar.content.skills.Defend(),
    ]
    fighter.right = fighter.inventory[0]
    fighter.left  = fighter.inventory[1]
    fighter.chest = fighter.inventory[2]
    fighter.legs  = fighter.inventory[3]
    fighter.feet  = fighter.inventory[4]
    fighter.description = 'Fighters are skilled in hand to hand combat. They specialize in advanced combat maneuvers and tightly controlled attacks which minimize opportunities for counterattacks.\nFighters start with no active spells but have advanced training in parrying, swords, spears, and shields.'

    return fighter


def make_arcanist():
    mage = Lifeform(None)
    mage.name = 'Mage'
    mage.stats = {}
    mage.stats['strength'] = 1
    mage.stats['dexterity'] = 2
    mage.stats['vitality'] = 1
    mage.stats['acuity'] = 6
    mage.stats['sense'] = 2
    mage.stats['resolve'] = 2

    mage.inventory = [
        erukar.Wand(modifiers=[erukar.Oak]),
        erukar.Focus(modifiers=[erukar.Oak]),
        erukar.Candle(),
        erukar.Robes(modifiers=[erukar.Cotton]),
        erukar.Sandals(modifiers=[erukar.Leather]),
        erukar.Breeches(modifiers=[erukar.Cotton]),
        erukar.PotionOfHealing(5),
        erukar.PotionOfRenewal(5)
    ]
    mage.spell_words = [
    ]
    mage.skills = [
        erukar.content.skills.ArcaneGift(),
        erukar.content.skills.PracticedSpellcasting(),
        erukar.content.skills.WandTraining()
    ]
    mage.right = mage.inventory[0]
    mage.left = mage.inventory[1]
    mage.chest = mage.inventory[2]
    mage.feet = mage.inventory[3]
    mage.legs = mage.inventory[4]

    mage.description = 'Arcanists excel in observation and intellect. '\
        'Their orders are highly diverse and tend to attract the '\
        'most intelligent of indivuals. Mages specialize in casting '\
        'arcane magics, though some may tend to prefer alchemy or '\
        'research.\nMages start with several Arcane Words: Three Elemental '\
        'Augments (Ice, Fire, and Electric) and two Spellshapes (Bolt, '\
        'Shield). By combining these words, they can shape their spells '\
        'to their needs with minimal downtime.'
    return mage


def make_deceiver():
    ranger = Lifeform(None)
    ranger.name = 'Ranger'
    ranger.stats = {}
    ranger.stats['strength'] = 3
    ranger.stats['dexterity'] = 5
    ranger.stats['vitality'] = 2
    ranger.stats['acuity'] = 2
    ranger.stats['sense'] = 2
    ranger.stats['resolve'] = 1

    ranger.inventory = [
        erukar.Longbow(modifiers=[erukar.Oak]),
        erukar.Boots(modifiers=[erukar.Leather]),
        erukar.Vest(modifiers=[erukar.Leather]),
        erukar.Breeches(modifiers=[erukar.Leather]),
        erukar.Arrow(quantity=25, modifiers=[erukar.Oak]),
        erukar.PotionOfHealing(5)
    ]

    ranger.skills = [
        erukar.content.skills.Dodge(),
        erukar.content.skills.EagleEye()
    ]
    ranger.right = ranger.inventory[0]
    ranger.feet = ranger.inventory[1]
    ranger.chest = ranger.inventory[2]
    ranger.legs = ranger.inventory[3]
    ranger.ammunition = ranger.inventory[4]

    ranger.description = 'Rangers are marksmen, specializing in the art '\
        'of archery and ranged combat. They tend to prefer keeping their '\
        'targets at a distance\nRangers start with advanced training in bows '\
        'and crossbows and have Snipe, an active skill which provides '\
        'additional accuracy at long ranges at the cost of damage.'
    return ranger
