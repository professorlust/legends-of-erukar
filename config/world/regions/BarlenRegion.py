import erukar
from erukar.system.engine import EnvironmentProfile, Sector, Region

def create():
    barlen = Region()
    barlen.name = "Greater Barlen Region"
    barlen.description = "A fertile area, known best for its vast barley and wheat fields. The seat of this region is a large town known as Barlen whose economy consists mostly on agriculture taxes and exports of the barley harvest."
    barlen.sectors = [
        create_barlen_outskirts(barlen),
        create_razorwoods_camp(barlen)
    ]
    barlen.sector_limits = list(acceptable_bounds())
    barlen.sector_template = create_sector_template()

    return barlen

def acceptable_bounds():
    for x in range(-1, 3):
        for alpha in range(-1, 3):
            for beta in range(-1, 3):
                yield (x, alpha, beta)

def create_barlen_outskirts(region):
    sector = create_sector_template(region) 
    sector.name = 'Barlen Town Outskirts'
    sector.set_coordinates((0, 0, 0))
    return sector

def create_razorwoods_camp(region):
    sector = create_sector_template(region) 
    sector.name = 'Ferelden Razorwoods Camp'
    sector.set_coordinates((2, 2, 2))
    return sector

def create_sector_template(region=None):
    sector = Sector(region)
    sector.environment_profile = EnvironmentProfile.Woodlands()
    return sector
