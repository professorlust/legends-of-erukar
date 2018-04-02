from erukar.system.engine import Enemy
import erukar, random

class IurianCleric(Enemy):
    BriefDescription = "an Iurian Cleric"
    RandomizedWeapons = ['right' ]
    outline_pixels = [4,5,6,7,16,19,28,31,41,42,51,52,55,56,62,69,74,76,79,81,86,88,91,93,99,100,101,102,103,104,112,115,124,127,136,137,138,139]
    armor_pixels = [17,18,53,54,63,64,65,66,67,68,75,77,78,80,89,90,113,114,125,126]
    skin_pixels = [29,30,87,92]

    def __init__(self, random=True):
        super().__init__("Iurian Cleric")
        self.str_ratio = 0.2
        self.dex_ratio = 0.1
        self.vit_ratio = 0.1
        self.acu_ratio = 0.1
        self.sen_ratio = 0.3
        self.res_ratio = 0.2
        self.define_level(5)

    def generate_tile(self, dimensions, tile_id):
        outline = {'r':32, 'g': 32, 'b': 32, 'a': 1}
        armor_color = {'r':158, 'g': 158, 'b': 158, 'a': 1}
        skin_tone = {'r': 160, 'g':108, 'b':89, 'a':1}

        for index in range(0, 144):
            if index in self.outline_pixels: yield outline
            elif index in self.armor_pixels: yield armor_color
            elif index in self.skin_pixels: yield skin_tone
            else: yield {'r':0, 'g':0, 'b':0, 'a':0}
