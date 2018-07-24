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
    barlen.add_sector(create_crypts_of_icamore)
    barlen.add_sector(create_tomb)
    barlen.add_sector(create_izeth_citadel_1f)

    barlen.sector_limits = acceptable_bounds()
    barlen.sector_template = create_sector_template(barlen)

    return barlen


def acceptable_bounds():
    return [
        (0, 3),
        (0, 2), (1, 2),
        (0, 1), (1, 1), (2, 1),
        (0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
        (1, -1), (2, -1), (4, -1), (5, -1),
        (1, -2), (2, -2), (6, -2),
        (2, -3)
    ]


def create_barlen_outskirts(region):
    def econ_seed(sector):
        econ = EconomicProfile()
        econ.demand[erukar.IurwoodLumber] = 2000
        econ.supply[erukar.IurwoodLumber] = 100
        econ.demand[erukar.AshLumber] = 1000
        econ.supply[erukar.AshLumber] = 100
        return econ
    sector = create_sector_template(region, econ_seed)
    sector.name = 'Barlen Town Outskirts'
    sector.environment_profile = EnvironmentProfile.CityOutdoors()
    sector.set_coordinates((0, 0))
    town = Location(sector)
    town.is_named = True
    town.name = 'Barlen Town Outskirts'
    town.dungeon_file_name = 'BarlenOutskirts'
    sector.locations.add(town)
    return sector


def create_razorwoods_camp(region):
    def econ_seed(sector):
        econ = EconomicProfile()
        econ.demand[erukar.IurwoodLumber] = 10
        econ.supply[erukar.IurwoodLumber] = 5000
        econ.demand[erukar.AshLumber] = 10
        econ.supply[erukar.AshLumber] = 5000
        return econ
    sector = create_sector_template(region, econ_seed)
    sector.name = 'Feriden Razorwoods Camp'
    sector.set_coordinates((3, 0))
    sector.environment_profile = EnvironmentProfile.SnowyWoodlands()

    camp = Location(sector)
    camp.is_named = True
    camp.name = 'Feriden Razorwoods Camp'
    camp.dungeon_file_name = 'RazorwoodsCamp'
    sector.locations.add(camp)

    return sector


def create_crypts_of_icamore(region):
    sector = create_sector_template(region)
    sector.name = 'Terrace of the Crypts of Icamore'
    sector.set_coordinates((0, 3))
    sector.environment_profile = EnvironmentProfile.SnowyWoodlands()

    terrace = Location(sector)
    terrace.is_named = True
    terrace.name = 'Izeth Citadel Terrace'
    terrace.chunks = [Chunk()]
    sector.locations.add(terrace)

    return sector


def create_tomb(region):
    sector = create_sector_template(region)
    sector.name = 'Terrace of the Tomb of Reastus III'
    sector.set_coordinates((6, -2))
    sector.environment_profile = EnvironmentProfile.SnowyWoodlands()

    terrace = Location(sector)
    terrace.is_named = True
    terrace.name = 'Tomb of Reastus III Terrace'
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


def create_sector_template(region=None, econ_seed_fn=None):
    sector = OverlandSector(region, econ_seed_fn)
    sector.environment_profile = EnvironmentProfile.SnowyWoodlands()
    return sector
