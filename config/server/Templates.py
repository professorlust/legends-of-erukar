from erukar.system.engine import Lifeform
from erukar.content.inventory import *
from erukar.content.modifiers.material import *
import erukar

def configure(shard):
    shard.templates = [
        make_barbarian(),
        make_cleric(),
        make_fighter(),
        make_mage(),
        make_ranger()
    ]

def make_barbarian():
    barbarian = Lifeform(None)
    barbarian.name = 'Barbarian'
    barbarian.stats = {}
    barbarian.stats['strength']  = 4
    barbarian.stats['dexterity'] = 1
    barbarian.stats['vitality']  = 4
    barbarian.stats['acuity']    = 1
    barbarian.stats['sense']     = 1
    barbarian.stats['resolve']   = 4
    
    barbarian.inventory = [
        Axe(modifiers=[Iron]),
        Mace(modifiers=[Iurwood]),
        Breeches(modifiers=[Leather]),
        Candle(),
    ]

    barbarian.left  = barbarian.inventory[0]
    barbarian.right = barbarian.inventory[1]
    barbarian.legs  = barbarian.inventory[2]

    barbarian.spell_words = [
    ]
    barbarian.skills = [
        erukar.content.skills.Bloodlust(),
        erukar.content.skills.Rage(),
    ]

    barbarian.description = 'Barbarians are hardy melee fighters capable of dealing lots of damage in bursts. Their raw strength allows them great amounts of damage with heavy, blunted weapons such as Maces and Staves.\nEach barbarian has access to a skill called "Rage" which temporarily grants bonuses to attack damage/health equal to the barbarian\'s resolve score and a 33% increase to physical damage mitigation.'

    return barbarian

def make_cleric():
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
        Piece(modifiers=[Chainmail]),
        Leggings(modifiers=[Chainmail]),
        Treads(modifiers=[Leather]),
        Potion(5),
    ]
    cleric.spell_words = [
    ]

    cleric.left  = cleric.inventory[0]
    cleric.chest = cleric.inventory[1]
    cleric.legs  = cleric.inventory[2]
    cleric.feet  = cleric.inventory[3]
    cleric.description = 'Clerics are holy warriors who specialize in purification and sanctification. Clerics use a weapon of their choice and a holy symbol, which provides bonuses while within hallowed areas. They have a strong sense score which allows them to sense otherworldly presences.\nClerics can use holy water or a consecration spell word to purify a room from evil. They also have access to a word which heals and one which persists effects for a duration of time.'

    return cleric

def make_fighter():
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
        Sword(modifiers=[Iron]),
        HeaterShield(modifiers=[Oak]),
        Piece(modifiers=[Chainmail]),
        Leggings(modifiers=[Chainmail]),
        Treads(modifiers=[Leather]),
        Spear(modifiers=[Iron]),
    ]
    fighter.right = fighter.inventory[0]
    fighter.left  = fighter.inventory[1]
    fighter.chest = fighter.inventory[2]
    fighter.legs  = fighter.inventory[3]
    fighter.feet  = fighter.inventory[4]
    fighter.description = 'Fighters are skilled in hand to hand combat. They specialize in advanced combat maneuvers and tightly controlled attacks which minimize opportunities for counterattacks.\nFighters start with no active spells but have advanced training in parrying, swords, spears, and shields.'

    return fighter

def make_mage():
    mage = Lifeform(None)
    mage.name = 'Mage'
    mage.stats = {}
    mage.stats['strength']  = 1
    mage.stats['dexterity'] = 2
    mage.stats['vitality']  = 1
    mage.stats['acuity']    = 6
    mage.stats['sense']     = 2
    mage.stats['resolve']   = 2
    
    mage.inventory = [
        Wand(modifiers=[Oak]),
        Candle(),
        Robes(modifiers=[Cotton]),
        Sandals(modifiers=[Leather]),
        Breeches(modifiers=[Cotton]),
        Potion(5)
    ]
    mage.spell_words = [
    ]
    mage.skills = [
        erukar.content.skills.ArcaneGift(),
        erukar.content.skills.ArcaneTraining(),
    ]
    mage.right = mage.inventory[0]
    mage.left  = mage.inventory[1]
    mage.chest = mage.inventory[2]
    mage.feet  = mage.inventory[3]
    mage.legs  = mage.inventory[4]

    mage.description = 'Mages excel in observation and intellect. Their orders are highly diverse and tend to attract the most intelligent of indivuals. Mages specialize in casting arcane magics, though some may tend to prefer alchemy or research.\nMages start with several Arcane Words: Three Elemental Augments (Ice, Fire, and Electric) and two Spellshapes (Bolt, Shield). By combining these words, they can shape their spells to their needs with minimal downtime.'
    return mage

def make_ranger():
    ranger = Lifeform(None)
    ranger.name = 'Ranger'
    ranger.stats = {}
    ranger.stats['strength']  = 3
    ranger.stats['dexterity'] = 5
    ranger.stats['vitality']  = 2
    ranger.stats['acuity']    = 2
    ranger.stats['sense']     = 2
    ranger.stats['resolve']   = 1
    
    ranger.inventory = [
        Bow(modifiers=[Oak]),
        Boots(modifiers=[Leather]),
        Vest(modifiers=[Leather]),
        Breeches(modifiers=[Leather]),
        Arrow(modifiers=[Oak]),
        Potion(5) # This should be replaced with ammo
    ]
    ranger.right = ranger.inventory[0]
    ranger.feet  = ranger.inventory[1]
    ranger.chest = ranger.inventory[2]
    ranger.legs  = ranger.inventory[3]
    ranger.ammunition = ranger.inventory[4]
    
    ranger.description = 'Rangers are marksmen, specializing in the art of archery and ranged combat. They tend to prefer keeping ther targets at a distance\nRangers start with advanced training in bows and crossbows and have Snipe, an active skill which provides additional accuracy at long ranges at the cost of damage.'
    return ranger
