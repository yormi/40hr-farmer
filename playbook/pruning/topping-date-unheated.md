# Topping date — unheated greenhouse

Pick the topping date so the last truss reaches breaker before
the house goes cold. Harvest at breaker, finish warm indoors.

Why → [`science/fruit.md`](../../science/fruit.md)

After the cut → [`post-topping-drawdown.md`](post-topping-drawdown.md)


## Rule

- **Top 9 weeks before the date the outside daily mean first
  hits 55 °F.**
- Anchor date from climate normals → one lookup, in July.
- Top above a truss already set, never one still in flower.
- Start generative steering 2–3 weeks before the top date.


## Formula (cross-check, first year)

- Degree-days, base 50 °F: `DD = Σ (inside daily mean − 50)`
- Inside daily mean = outside daily mean + 2–5 °F house offset.
- Budget needed, set → breaker: **~845 DD + 10%** (~930).
- Top on the latest date whose remaining budget covers it.
- Accumulation past the 55 °F anchor (~100 DD) = buffer, don't
  count it.


## Live tracking

- 7-day running mean, never a single day.
- Cold or dark stretch in August → recount. Earlier costs
  little; later risks a green truss.


## Caveats

- Assumes ~70 °F house daily mean on topping day and a steady
  fall slide. Plateau-then-crash falls shortchange the rule →
  run the formula once alongside to calibrate.
- Vine-red instead of breaker: ~12 weeks, budget ~1,080 DD.
