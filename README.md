# The Legends of Erukar
[![Code Climate](https://codeclimate.com/github/etkirsch/pyna-rpg/badges/gpa.svg)](https://codeclimate.com/github/etkirsch/pyna-rpg) [![Test Coverage](https://codeclimate.com/github/etkirsch/pyna-rpg/badges/coverage.svg)](https://codeclimate.com/github/etkirsch/pyna-rpg/coverage) [![Issue Count](https://codeclimate.com/github/etkirsch/pyna-rpg/badges/issue_count.svg)](https://codeclimate.com/github/etkirsch/pyna-rpg) [![Build Status](https://travis-ci.org/etkirsch/legends-of-erukar.svg?branch=master)](https://travis-ci.org/etkirsch/legends-of-erukar)

The Legends of Erukar is a procedurally-generated multiplayer online dungeon (MUD) set in the world of Tolmea. Every single thing is stochastically generated per shard. Locations, though their names may be consistent from shard to shard, will be generated on creation and persisted. Dungeons may or may not be persisted; this will be determined at a later point in time.

### Stochastic Generation
All weapons, armor, items, monsters, etc. will be random. The basis for generation is as follows.

1. Determine object type to generate (Weapon example: Longsword, rapier, dagger, pike)
2. Assign the object's **quality probability density function** to random variable **P(Rarity)**
  * This is to allow certain objects, e.g. those that are more rare, to skew their pdfs towards higher values
3. Get the area's **difficulty probability density function** and assign it to random variable **P(Difficulty)**
  * This is so that harder dungeons and areas can skew their pdfs towards higher values
4. Combine **P(Rarity)** and **P(Difficulty)** into a bivariate density function **P(Quality)**
5. Using the bivariate **P(Quality)**, get *N* modifiers to apply to the object such that the statement `calculated_quality <= sum([m.quality for m in modifiers])`
  * Each modifier has a real number quality attached to it
  * Beneficial modifiers have increasingly more prohibitive quality costs
  * Detrimental modifiers have negative quality, offsetting the cost to beneficial modifiers
  * The modifiers are arranged along **P(Quality)** from most detrimental to most beneficial, yielding significantly better results for items of high rarity within high difficulty zones

## Dexterity Influence on Turn Order
Each lifeform posesses a `turn_order_modifier` method in order to determine turn orders. The TurnManager iterates over the range (0, 100] and permits action by a Lifeform if its `turn_order_modifier`'s result modulused by the range's current value is zero. The Lifeform's dexterity attribute directly affects the value of the `turn_order_modifier` method using the following formula

```python
# Where d is a value within the range [-2, 20]
turn_order_modifier = min_turn_mod + max_turn_mod * (1 - (1 + exp( (10 - d) / 5)))
```

![](docs/plots/turn_order_modifier.png)

Through the use of this sigmoid function, the amount of time between turns (turn_order_modifier) decreases slightly initially, then drastically, eventually tapering off as the dexterity attribute approaches its maximum. At -2 dexterity, the Lifeform should have roughly 2 turns per 100 TurnManager ticks. At 20 dexterity, the Lifeform should have approximately 6 turns per 100 TurnManager ticks.

## Documentation
* [Mechanics](docs/mechanics.md)
* [Commands](docs/commands.md)
* [Character Progression](docs/progression.md)
* [Networking: Shards and Instancing](docs/networking.md)
* [Procedural Generation](docs/procedural-generation-modifiers.md)
