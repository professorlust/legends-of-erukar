from enum import Enum

class NpcQuality(Enum):
    CanSellBasic = 1
    CanSellMagic = 2
    CanRepairBasic = 3
    CanCraftBasic = 4
    CanRepairMagic = 5
    CanCraftMagic = 6
    CanProvideTransportation = 7
