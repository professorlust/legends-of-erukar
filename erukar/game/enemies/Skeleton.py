from erukar.engine.lifeforms.Enemy import Enemy
from erukar.game.inventory.weapons.Sword import Sword

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
        self.right = Sword()
        self.name = "Skeleton"
