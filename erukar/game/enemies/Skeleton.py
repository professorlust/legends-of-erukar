from erukar.engine.lifeforms.Enemy import Enemy
from erukar.game.inventory.weapons.Sword import Sword
from erukar.game.inventory.armor.shields.Buckler import Buckler

class Skeleton(Enemy):
    critical_health = [
        'The skeleton is nearly destroyed!',
        'The skeleton is mangled and seems to have no unbroken bones.' ]

    badly_wounded = [
        'The skeleton has been damage to such an extent that it\'s bones bow or hinge in a state of brokenness.',
        'Most of the bones on the skeleton are broken or missing.' ]

    wounded = [
        'The skeleton appears to have endured a heavy beating, and many bones are cracked.',
        'Many bones on this skeleton are broken.']

    slightly_wounded = [
        'The skeleton has some cracked or broken bones, but those are few and far between.',
        'This skeleton has taken a beating but still stands nonetheless.']

    full_health = [
        'The skeleton\'s bones are putrid and unpleasant but none of them are broken.',
        'This skeleton seems to be recently reanimated.']

    def __init__(self):
        super().__init__("Skeleton")
        self.dexterity = -2
        self.name = "Skeleton"
        self.randomize_equipment()
        self.set_vision_results('You see a {alias}.','You see a {alias}. {describe}',(0,1))
        self.set_sensory_results('You hear movement.','You hear a {alias}.',(0, 1))
        self.set_detailed_results('There is a skeleton holding a {describe|right}.','The skeleton is holding a {describe|right} in its right hand and {describe|left} in its left. ')

    def randomize_equipment(self):
        self.right = Sword()
        self.left = Buckler()
