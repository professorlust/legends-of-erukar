import erukar
from erukar.system.engine import EnvironmentProfile, OverlandSector,  Sector
from erukar import Region, Location, Chunk, EconomicProfile


def create():
    barlen = Region()
    barlen.name = "Greater Barlen Region"
    barlen.description = \
        "A fertile area, known best for its vast barley and '\
        'wheat fields. The seat of this region is a large town known as '\
        'Barlen whose economy consists mostly on agriculture taxes and '\
        'exports of the barley harvest."
    barlen.add_sector(create_barlen_outskirts)
    barlen.add_sector(create_razorwoods_camp)
    barlen.add_sector(create_izeth_terrace)
    barlen.add_sector(create_izeth_citadel_1f)

    barlen.sector_limits = acceptable_bounds()
    barlen.sector_template = create_sector_template(barlen)

    return barlen


def acceptable_bounds():
    return [
        (0, 3),
        (0, 2),
        (1, 1), (2, 1),
        (1, 0), (3, 0),
        (1, -1), (4, -1),
        (2, -2),
        (2, -3)
    ]
