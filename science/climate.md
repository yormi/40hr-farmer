# Climate — temperature as the crop's rate dial


## Model


### The 24-hour average


- **24-hour weighted average temperature** → crop development rate   (the speed dial; how fast everything happens)

- instantaneous **spikes** → stress, not rate   (a spike hurts the plant; it does not move the average enough to change speed)

- **fruit load** → the target average, downward   (more clusters carried → run cooler)

- **light received** → the target average, upward   (warmth without light builds weak, leggy stems)

- cloud cover, day length, seasonal sun angle, and plastic cleanliness all move the target daily

- **sensor placement** → every downstream decision   (one badly placed sensor overstates temperature and corrupts the whole chain)


### The day / night split


- **flat day-to-night profile** → vegetative

- **wide day-to-night gap** → energy into fruit (generative)

- night temperature carries full weight in the average while contributing no photosynthesis   (see the respiration asymmetry in [`leaf-energy.md`](leaf-energy.md))


### Cold limits


| Average below | Consequence |
|---|---|
| 60 °F | abnormal flowers, pollen failure, blossom drop |
| 55 °F | floor for deliberate correction |
| 50 °F | catfacing, fused fruit, zippering |

- **cloudy day** → target drops toward 63 °F


### Heat


- **healthy plant tolerance** ≫ grower expectation   (the large greenhouse-tomato regions are hot Spain and Mexico)

- **fruit removed** → heat headroom   (~2 °F of extra tolerance per fruit dropped)

- **shade** → light lost 1:1 → yield lost 1:1   (shade blocks light whenever it is deployed, including on days that were not the problem)

- shade helps only where roots genuinely cannot supply water fast enough for transpiration   (a water-supply problem, not a heat problem)

- heat damage to a crop is usually a **revealed** weakness, not a caused one   (a healthy plant absorbs the same heat that breaks a compromised one)


### Air movement


- **HAF fans** → canopy drying → less disease

- **closed vents + HAF stopped** → CO₂ depletes in the canopy → photosynthesis stalls

- so HAF running is the default whenever vents are shut


## Invariants


- The 24-hour average sets rate. Instantaneous temperature sets stress. They are different questions.

- Lowering the average to rescue a thin stem trades yield for stability. It is a holding action, never a fix.


## Boundaries


- Covers temperature as a rate and stress driver, and air movement.

- Air dryness and VPD → [`water.md`](water.md).

- Temperature's effect on fruit development timing → [`fruit.md`](fruit.md).

- Temperature's effect on respiration → [`leaf-energy.md`](leaf-energy.md).


## Vocabulary


**24-hour weighted average** — the mean temperature across a full day and night, weighted by time at each temperature. The number that sets crop speed.

**HAF** — horizontal air flow; fans that move air along the length of the house to dry the canopy and keep CO₂ mixed.
