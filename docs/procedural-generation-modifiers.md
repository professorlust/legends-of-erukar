# Procedural Generation: Modification
The Modifiers that are used in Legends of Erukar are determined through a means of pseudorandom clustering. That is to say, we create a simplified multivariate distribution treating environmental factors already established as input random variables. We treat all random variables as if they were on the range -1.0 to 1.0.

## Example: Arctic Temple
Let us assume we have a temple that occurs in a cold region. The environment has two variables which are explicitly defined (temperature and fabrication) and two variables which are indeterminant (altitude and sanctity). The breakdown can be defined within the following ranges.

```python
-1 < temperature <= -0.6  # defines the temperature of a location
0.8 < fabrication < 1.0   # defines how much of the environment is man-made
-0.4 < altitude <= 0.4    # defines how far above or below sea this environment is
-0.25 < sanctity <= 0.25  # defines how (un)holy this environment is
```

Naturally, temperature and altitude are slightly dependent. Sanctity and Fabrication are conversely independent variables. Therefore, we can calculate the probability distribution for the environment as the following.

```python
f(temp, fabr, alt, sanc) = prob(alt) * prob(temp | alt) * prob(fabr) * prob(sanc)
```

Using these parameters we can drive downward (procedural) generation of the dungeon itself and later to the contents within those rooms. The generators which modify the dungeon's rooms then use the Generation Parameters (as shown above) and conditional probabilities to create weights for a completely new distribution. We can take this distribution and use it to determine random properties for rooms. Take the following three (simplified) objects,

```python
class Temple:
    ProbabilityFromTemperature:  0.0
    ProbabilityFromFabrication:  1.0
    ProbabilityfromAltitude:     0.0
    ProbabilityFromSanctity:     1.0
    
class Cave:
    ProbabilityFromTemperature:  0.0
    ProbabilityFromFabrication: -1.0
    ProbabilityFromAltitude:    -0.4
    ProbabilityFromSanctity:    -0.1

class WarmthRoom: # whatever that means
    ProbabilityFromTemperature: -1.0
    ProbabilityFromFabrication:  1.0
    ProbabilityFromAltitude:     0.0
    ProbabilityFromSanctity:     0.0
```

We can see that each room has a set of conditional probabilities that correspond to each of thegeneration parameters from the dungeon itself. The resulting probabilities (unnormalized) are then multiplied with the generational parameters from the dungeon and summed. This gives the resulting probabilities of approximately 1.0, -1.0, and 2.0 for the Temple, Cave, and WarmthRoom respectively. Normalizing these weights we get approximately 0.0% chance for a Cave to appear, 33% for a Temple to appear, and a 67% likelihood that the room will be a WarmthRoom.

This sequence of events then applies downward. A Temple room should have a higher sanctity value than the WarmthRooms yielding more divine weapons, armors, and the like. The WarmthRooms, however, are more likely to yield warm-blooded monsters because they have a higher temperature value and likely also some anti-cold gear, such as Flaming Arrows, Potions of Warmth, et cetera.
