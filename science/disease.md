# Disease — what drives it and how fast it moves


## Model


### The two drivers


- **leaf wetness duration** → infection   (the primary lever; nearly every fungal and bacterial disease needs free water or saturated air on tissue)

- **variety genetics** → susceptibility   (the second lever, set once at seed order)

- everything else — sprays, culling, sanitation — is downstream of these two

- **drying the zone at least once every 90 minutes** interrupts the wetness window every disease depends on


### Wound and tissue entry


- **pruning wound** → entry point while wet   (root pressure on a non-transpiring plant pushes a droplet out of the wound, the droplet catches spores, the plant draws it back in)

- **pruning stub** → never heals → standing entry point for botrytis

- **senescing tissue** → botrytis substrate   (dying leaves are colonised before healthy ones)

- **soil splash** → early blight onto lower leaves   (mulch interrupts it)


### Spread rate sets the response


| Disease | Plant to plant | Ceiling if ignored |
|---|---|---|
| Late blight | **1 day** | house lost in a week |
| Bacterial spot | 5 days | fruit out of the pack |
| Botrytis | 4 days | fruit rot; stem girdle kills the plant |
| Leaf mold | 1 week | yield drag, plant survives |
| Powdery mildew | 1 week | vigour and yield sapped, plant survives |
| Early blight | 2 weeks | steady yield bleed, plant survives |
| Sclerotinia | 2 weeks | plant lost; soil banked 8 years |

- **spread rate** → whether detection can wait for a weekly pass   (1-day spread cannot; 1-week spread can)

- **late blight infection extent** ≫ visible symptoms   (the colonised zone runs ahead of what shows, so a spotted leaf implies a colonised plant)

- **sclerotinia** → soil bank persisting ~8 years   (a single plant loss becomes a site liability)


### What control can achieve


| Disease | Realistic ceiling |
|---|---|
| Leaf mold | climate and variety clear it; sprays are inefficient |
| Bacterial spot | suppression only; copper resistance common |
| Powdery mildew | managed, never cleared; a low background haze is success |
| Botrytis | held only while the house stays dry; recurrence expected |
| Late blight | often unwinnable once inside; goal is saving the house, not the plants |
| Sclerotinia | the plant is lost; goal is saving the bed |
| Early blight | usually held to the lower leaves all season |

- a **dry house** substitutes for most spraying; sprays on top of a dry house add little

- **spray under heat** → phytotoxicity   (sulfur above 85 °F burns fruit and leaves)

- **sulfur and oil within ~2 weeks of each other** → phytotoxicity


### Protocol design


- **decision count** → adherence   (a stretched grower follows a one-decision protocol and abandons a five-decision one)

- so fixed rules are preferred over mid-season judgment calls, paid for with some surplus spray or labour

- **detect** and **diagnose** are separable roles   (the whole crew can flag; one trained eye names)


## Invariants


- Climate and genetics decide the disease outcome. Sprays adjust it at the margin.

- Late blight is the only disease whose spread rate outruns a weekly cadence. Everything else can batch.

- Cutting a spotted leaf off a late-blight plant leaves the infection in place.


## Boundaries


- Covers what drives disease and how fast it moves.

- Canopy wetness and VPD → [`water.md`](water.md).

- Air movement and drying → [`climate.md`](climate.md).

- Product choice, rates, re-entry, and pre-harvest intervals are regulatory and label matters, held in the protocol cards.


## Vocabulary


**leaf wetness duration** — how long free water or saturating humidity sits on tissue; the exposure that decides whether a spore establishes.

**inoculum** — viable spores or bacteria present and able to start an infection.

**phytotoxicity** — crop damage caused by the treatment itself.

**girdle** — a lesion encircling the stem, cutting everything above it off from the roots.
