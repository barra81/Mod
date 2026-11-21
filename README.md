# WTP Resettled

A modmod for **[We the People](https://github.com/We-the-People-civ4col-mod/Mod)** (WTP), the large overhaul mod for *Sid Meier's Civilization IV: Colonization*.

WTP Resettled keeps everything WTP offers and adds a reworked AI, automation for everyday chores, siege warfare, forts, new map generators, economy balancing and a set of interface improvements.

> **Download:** get the latest version from the [Releases](../../releases) page.

---

## Installation

1. Download the release archive from [Releases](../../releases).
2. Extract it into `Civilization IV Colonization\Mods\` so that the mod folder sits directly inside `Mods`.
3. Start Colonization, choose **Advanced → Load a Mod** and select the mod.

Requires *Civilization IV: Colonization* (patched to 1.01f, as for WTP itself). Savegames of plain WTP may not work as intended when loaded.

---

## Features

### AI

- **Colonial AI overhaul:** better expansion and settling, transport and ship use, purchases in Europe, pioneer work and a workforce planner that assigns colonists to the jobs where they are most useful.
- **Native AI overhaul:** native trade, supply and war behaviour reworked.
- **War AI:** parts of the K-Mod war planning as a basis, extended with our own additions: counter units against siege stacks, defenders sent to the threatened border, and an AI that knows how to lay siege to cities.
- AI respects forts that block trade with native villages.
- Faster turn changes: cheaper trade route path searches, a faster pathfinder, cached travel times for the workforce planner.

### Siege warfare

- Cities are besieged instead of taken in a single attack.
- Artillery duels and gunpowder supply, including a powder wagon unit.
- Siege camps with their own art on the map.

### Automation

- **Colonist automation:** auto-assign a job, *Transport to City / Plot*, automate a transport with colonists, job menu.
- **Automate Transport:** fills free cargo slots for colonies on the way, tops up partly filled slots, makes small detours only when they are worth it, respects import limits of the receiving colony.
- **Assigned trade routes:** fill the hold and stop at colonies on the way; trade orders of automated transports shown in the tooltip.
- **Trade route presets**, reserved and private trade routes, trip limit for land transports.
- **Automatic market imports.**
- **Automate Treasure / Fetch Treasures.**
- **Patrol** button.
- **Pioneer plan** and private pioneers.
- An automated transport stays selected and is followed on the map until another unit is selected.

### Forts

- Forts can be built on native land.
- A fort controls the trade of nearby native villages.
- Barracks space in forts; movement rules around occupied forts.

### Economy and balancing

- Reworked yields, Europe prices, ship costs and market memory.
- **Market boom** event at game start.
- Natives: missions, trade posts, bargaining, braves and native prices rebalanced; native land costs, bought land is not flipped by culture.
- Army upkeep for the human player, with an upkeep multiplier per game speed.
- Extra warehouse storage (adjustable), Custom House sell threshold respects protected building projects, storage overflow forecast.
- More cargo slots for wagon trains, stagecoaches and treks.
- Many smaller rule changes and fixes (barracks limit, enemy roads, production overflow, random founding fathers, canals, pirates and more).

### Game options

- Dropdowns for the **storage multiplier** (50–200 %) and the **military upkeep multiplier** (50–200 %).
- Checkbox to make upkeep depend on game speed.

### Interface

- **Nested tooltips:** an own tooltip window at the mouse cursor with foldable unit, city and plot details; freeze a tooltip (X), stack them (Shift+X), open child windows with Colopedia links and give unit commands from the tooltip.
- **Waypoints:** set, rename and delete up to 5 waypoints each for ships and land units directly from a unit's tooltip.
- **Message panel:** mod messages on top, clickable messages jump to their place on the map, a waypoint list, and quick contact to the tribe from raid and battle messages.
- **Import/export window:** colored frames for import and export settings, marks for goods that limit production, filter view from the city tooltip, warning before unsaved changes are lost, Shift + mouse wheel changes amounts.
- **Building upgrade panel:** click a building in the city screen to queue its upgrade.
- **Amount dialog:** movable with the arrow keys, also in diplomacy and in the harbor.
- **Harbor:** Shift + click sells the goods of all ships in port; port buttons highlighted when an own ship is in Europe, Africa or Port Royal.
- **Unload all:** Shift + click or Ctrl+Shift+U unloads all own transports on the plot.
- **Advisors:** clicks in the domestic, military and native advisors jump to the city, unit or diplomacy screen.
- Shift doubles the map scroll speed; restored color coding in info texts; tidier HUD (gold, upkeep and domestic market lines).
- Human action log and travel log.

### Maps

- **Random New World:** a generator based on plate tectonics.
- **Fantasy New World:** a fantasy map of the Americas with interesting features, balanced for gameplay.
- **Eporue:** a flipped Europe scenario.

### Art

- Smaller city buildings and lower walls.
- Lumber mill, lumberjack camp and lodge keep the forest around them.

---

## Contributing

Contributions are welcome. Each feature lives on its own `feature/<name>` branch based on WTP's `develop`, so it can also be offered to WTP itself. `main` combines all features and is what the releases are built from. Which feature is built on which is shown in [docs/BRANCHES.md](docs/BRANCHES.md).

1. Fork the repository and create a `feature/<name>` branch.
2. Open a pull request against `main` (or against the matching `feature/*` branch).
3. Keep savegame compatibility in mind: add new enum values only at the end.

Bug reports and ideas go to [Issues](../../issues).

---

## Credits

- **The We the People team** — the base mod this work builds on.
- **FeldherrTilly** — AI, automation, siege warfare, forts, maps, balancing, art.
- **barra81** — nested tooltips, waypoints, message panel, import/export window, trade route logic, game options, harbor and HUD improvements.
