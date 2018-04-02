import erukar
from erukar.system.engine import EnvironmentProfile, OverlandSector,  Sector, Region, Location, Chunk

def create():
    barlen = Region()
    barlen.name = "Greater Barlen Region"
    barlen.description = "A fertile area, known best for its vast barley and wheat fields. The seat of this region is a large town known as Barlen whose economy consists mostly on agriculture taxes and exports of the barley harvest."
    barlen.add_sector(create_barlen_outskirts)
    barlen.add_sector(create_razorwoods_camp)
    barlen.add_sector(create_izeth_terrace)
    barlen.add_sector(create_izeth_citadel_1f)

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
    sector.set_coordinates((0,0,0))
    
    town = Location(sector)
    town.is_named = True
    town.name = 'Barlen Town Outskirts'
    town.dungeon_file_name = 'BarlenOutskirts'
    sector.locations.add(town)
    return sector

def create_razorwoods_camp(region):
    sector = create_sector_template(region) 
    sector.name = 'Feriden Razorwoods Camp'
    sector.set_coordinates((0,-3,3))
    sector.environment_profile = EnvironmentProfile.SnowyWoodlands()

    camp = Location(sector)
    camp.is_named = True
    camp.name = 'Feriden Razorwoods Camp'
    camp.dungeon_file_name = 'RazorwoodsCamp'
    sector.locations.add(camp)

    return sector

def create_izeth_terrace(region):
    sector = create_sector_template(region)
    sector.name = 'Izeth Citadel Terrace'
    sector.set_coordinates((0,-2,2))
    sector.environment_profile = EnvironmentProfile.SnowyWoodlands()

    terrace = Location(sector)
    terrace.is_named = True
    terrace.name = 'Izeth Citadel Terrace'
    terrace.chunks = [Chunk()]
    sector.locations.add(terrace)

    return sector

def create_izeth_citadel_1f(region):
    sector = Sector(region)
    sector.name = 'Izeth Citadel 1F'
    sector.set_coordinates("IzethCitadel1F")

    citadel_1f = Location(sector)
    citadel_1f.is_named = True
    citadel_1f.name = 'Izeth Citadel 1F'
    citadel_1f.dungeon_file_name = 'IzethCitadel1F'
    sector.locations.add(citadel_1f)

    return sector

def create_sector_template(region=None):
    sector = OverlandSector(region)
    sector.environment_profile = EnvironmentProfile.SnowyWoodlands()
    return sector
