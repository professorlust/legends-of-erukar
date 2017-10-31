import erukar
from erukar.system.engine import EnvironmentProfile, Sector, Region, Location

def create():
    barlen = Region()
    barlen.name = "Greater Barlen Region"
    barlen.description = "A fertile area, known best for its vast barley and wheat fields. The seat of this region is a large town known as Barlen whose economy consists mostly on agriculture taxes and exports of the barley harvest."
    barlen.sectors = set([
        create_barlen_outskirts(barlen),
        create_razorwoods_camp(barlen)
    ])
    barlen.sector_limits = acceptable_bounds()
    barlen.sector_template = create_sector_template()

    return barlen

def acceptable_bounds():
    return [
        (0,0,0),
        (2,-2,0),
        (2,-3,1),
        (1,-1,0),
        (1,-2,1),
        (1,-3,2),
        (0,-1,1),
        (0,-2,2),
        (0,-3,3),
        (-1,0,1)
    ]

def create_barlen_outskirts(region):
    sector = create_sector_template(region) 
    sector.name = 'Barlen Town Outskirts'
    sector.environment_profile = EnvironmentProfile.CityOutdoors()
    sector.set_coordinates((0, 0, 0))
    return sector

def create_razorwoods_camp(region):
    sector = create_sector_template(region) 
    sector.name = 'Ferelden Razorwoods Camp'
    sector.set_coordinates((0, -3, 3))
    sector.environment_profile = EnvironmentProfile.SnowyWoodlands()

    camp = Location(sector)
    camp.is_named = True
    camp.name = 'Ferelden Razorwoods Camp'
    camp.dungeon_file_name = 'RazorwoodsCamp'
    sector.locations.add(camp)

    return sector

def create_sector_template(region=None):
    sector = Sector(region)
    sector.environment_profile = EnvironmentProfile.SnowyWoodlands()
    return sector
