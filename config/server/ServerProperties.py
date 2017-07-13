def configure(shard):
    shard.properties.Name = 'Alar\'s Realm'
    shard.properties.Url = 'http://alars-realm.herokuapp.com'
    shard.properties.MaxPlayers = 10
    shard.properties.Description = 'A basic LoE server'

    shard.properties.AdminDetails = 'Legends of Erukar Official (admin@loe.dev)'
    shard.properties.PermaDeath = False

    shard.properties.StartingWealth = 1000
    shard.properties.StartingStatPoints = 20
    shard.properties.StartingSkillPoints = 2

    shard.properties.BaseHealth = 4
    shard.properties.BaseEvasion = 10
