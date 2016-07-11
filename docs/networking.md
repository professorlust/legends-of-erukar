# Networking
The networking in Legends of Erukar is fairly simplistic. There is a single `Shard` which serves as the point of interaction for all players and many `Instances`. The Shard runs on the main thread, then spins up as many Dungeon Instances as necessary on other threads. 

## Impetus
The existence of each dungeon instance on a separate, exclusive thread was primarily motivated by the fact that Legends of Erukar is meant to be highly multiplayer, yet still turn-based. At substantially high load, having each dungeon exist on the same thread would bog down the system, especially when calculating the AI's pathfinding. Granted, the GIL makes this a bit complicated, but this is an issue I am actively investigating.
