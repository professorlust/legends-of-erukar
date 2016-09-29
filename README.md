# The Legends of Erukar
[![Code Climate](https://codeclimate.com/github/etkirsch/pyna-rpg/badges/gpa.svg)](https://codeclimate.com/github/etkirsch/pyna-rpg) [![Test Coverage](https://codeclimate.com/github/etkirsch/pyna-rpg/badges/coverage.svg)](https://codeclimate.com/github/etkirsch/pyna-rpg/coverage) [![Issue Count](https://codeclimate.com/github/etkirsch/pyna-rpg/badges/issue_count.svg)](https://codeclimate.com/github/etkirsch/pyna-rpg) [![Build Status](https://travis-ci.org/etkirsch/legends-of-erukar.svg?branch=master)](https://travis-ci.org/etkirsch/legends-of-erukar)

The Legends of Erukar is a procedurally-generated multiplayer online dungeon (MUD) set in the world of Tolmea. Every single thing is stochastically generated per shard. Locations, though their names may be consistent from shard to shard, will be generated on creation and persisted. Dungeons may or may not be persisted; this will be determined at a later point in time.

Track my progress on [Trello](https://trello.com/b/1M9LUBqx/legends-of-erukar) and on my [Personal Page](https://evankirsch.io)! Below are the latest development blogs.

* 09/29/2016 -- [Auras and Dynamic Lighting Optimizations](https://evankirsch.io/blogs/loe-devblog-092916)
* 09/15/2016 -- [Under the Hood: Architecture and Design](https://evankirsch.io/blogs/loe-devblog-091516)
* 09/08/2016 -- [Narrative on a per-character basis](https://evankirsch.io/blogs/loe-devblog-090916)
* 08/19/2016 -- [Procedural Generation of Dungeons and Items](https://evankirsch.io/blogs/loe-devblog-081916)

## Getting Legends of Erukar on your System
You will need a few tools to make Legends of Erukar work. LoE has been developed in Ubuntu 16.04, therefore all installation steps provided here at the moment will be specific to that. In addition, LoE is meant to be run in Python 3.4+ and there is no compatibility with Python 2.

1. Get postgreSQL: `sudo apt-get install postgresql postgresql-contrib`
2. Ensure that you have `postgresql-devel` installed; you can install via `apt-get install libpq-dev`
3. Run `pip3 install -r requirements.txt` or `pip install -r requirements.txt`
4. run `install.py`


Set up your postgresql using [this guide.](https://www.digitalocean.com/community/tutorials/how-to-create-remove-manage-tables-in-postgresql-on-a-cloud-server). If you have authentication issues, confer with [this post](http://stackoverflow.com/questions/18664074/getting-error-peer-authentication-failed-for-user-postgres-when-trying-to-ge)

## Documentation
* [Mechanics](docs/mechanics.md)
* [Commands](docs/commands.md)
* [Character Progression](docs/progression.md)
* [Networking: Shards and Instancing](docs/networking.md)
* [Procedural Generation](docs/procedural-generation-modifiers.md)
