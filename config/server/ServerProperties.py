import os

def configure(shard):
    shard.properties.Name = os.environ.get('SERVER_NAME', 'Default Server Name')
    shard.properties.Url = os.environ.get('SERVER_URL', 'http://alars-realm.herokuapp.com')
    shard.properties.MaxPlayers = int(os.environ.get('MAX_PLAYERS',10))
    shard.properties.Description = os.environ.get('DESCRIPTION', 'A basic LoE server')

    shard.properties.AdminDetails = os.environ.get('ADMIN_DETAILS', 'Legends of Erukar Official (admin@loe.dev)')
    shard.properties.PermaDeath = True

    shard.properties.StartingWealth = 1000
    shard.properties.StartingStatPoints = 20
    shard.properties.StartingSkillPoints = 2

    shard.properties.BaseHealth = 4
    shard.properties.BaseEvasion = 10
