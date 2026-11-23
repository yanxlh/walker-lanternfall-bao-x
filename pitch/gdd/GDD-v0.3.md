<!-- Converted from Lanternfall_Game_Design_Document.docx (SHA-256 928c2258753b90efaafca5421cce5bceb2649969bf13e2671059836731f4477e) by pitch/gdd/docx_to_md.py. Text as written; images omitted. -->

# Lanternfall Game Design Document

Bao Xing   |   CSYE 7270   |   Assignment 4   |   Version 0.3   |   17 October 2026

Lanternfall is a top-down survival and delivery game set after an apocalypse in which supernatural fog has cut communication between human settlements. I control a courier whose light is both a weapon and a lifeline. Each mission carries a letter or supply package through hostile territory, and every successful delivery strengthens the destination as well as the courier network.

The current Godot prototype demonstrates a three-minute survival mission with one Lamp-Head Courier, two enemy types, automatic weapons, branching upgrades, the Sunflare evolution, win and loss states, sound, and a restart loop. The planned full game expands that foundation with multiple specialized couriers, additional weapons, deployable tools such as turrets, missions of different difficulty, and a post office that supports character selection and long-term progression.

Status convention. Current prototype identifies behavior already present in the build. Verified identifies behavior covered by existing project checks. Planned identifies an approved design direction that has not yet been implemented or verified.

## Game Name

Lanternfall

## Concept

After an apocalypse, an unnatural fog separates the remaining communities and blocks ordinary travel and communication. Lantern couriers cross the fog to carry letters, medicine, tools, and supplies between isolated settlements. Their lamps protect them from moths and fog-wraiths, but every route remains dangerous. Completing a delivery improves the receiving location and gradually reconnects the human network.

The design combines short survival runs with a longer campaign. During a mission, movement and positioning remain the main actions while weapons attack automatically. Between missions, the player returns to a post office to choose a courier, select a contract and difficulty, improve characters, and strengthen each character's starting weapon. Different courier specializations create different play styles without changing the readable, low-input combat foundation.

### Design Pillars and Player Experience Goals

P-01 Reconnection. Every delivery should make the isolated world feel more connected and visibly improve a destination.

P-02 Position over firing. Movement, route choice, and build decisions should matter more than manual aiming.

P-03 Readable light. Warm light communicates safety and power, while cold fog communicates danger; major events remain understandable without sound.

PX-01 Pressure and relief. A mission should alternate between crowd pressure, a short upgrade decision, and the relief of reaching a safer route.

PX-02 Distinct identity. Choosing a different courier should change the player's plan within the first thirty seconds.

PX-03 Visible consequence. A successful delivery should produce a destination change the player can recognize on the next visit.

## Game Flow

| Stage | Player experience |
|---|---|
| Post office and start | In the planned hub, the player chooses a courier, contract, and difficulty, then begins the route. The prototype starts directly with Enter, Space, or gamepad A. |
| Early run | The courier moves through the market while the Beam fires automatically at nearby enemies. |
| Collect and level | Enemies become lamp-oil gems. Collecting enough oil pauses the run and presents three upgrade cards. |
| Build a strategy | The player improves damage, attack speed, movement, pickup range, health, Beam, or Lamp-Moths. |
| Evolution | Maxing Beam and Lamp-Moths unlocks the Sunflare Lighthouse card, which replaces them with a radial burst. |
| Delivery result | Survive to 3:00 to complete the prototype route. The full game then applies the delivery's benefit to its destination and returns to the post office. |

## Game Elements and Assets

| Element | Purpose |
|---|---|
| Lamp-Head Courier | The player character and the warm visual center of the screen. |
| Moths | Fast, fragile enemies that pressure movement and provide frequent lamp-oil drops. |
| Fog-wraiths | Slower, tougher enemies that punish poor positioning and deal heavier contact damage. |
| Beam | The starting weapon. It automatically targets the nearest enemy. |
| Lamp-Moths | An unlockable orbiting weapon that controls space around the courier. |
| Lamp-oil gems | Experience pickups that fly into the satchel when the courier enters pickup range. |
| Market props | Stalls, noodle carts, lantern posts, crates, puddles, and leaves create paths and landmarks. |
| Upgrade cards | The main decision system. Three choices appear whenever the oil gauge fills. |
| Lantern Gate and shrine | Three-dimensional prototypes for later use as an entrance, obstacle, and upgrade landmark. |
| Post office | A planned campaign hub for choosing couriers, contracts, difficulty, and permanent improvements. |
| Courier roster | Planned characters with different specialties, starting weapons, and upgrade priorities. |
| Delivery network | Planned settlements and routes whose condition improves when letters and supplies arrive. |

## Main Characters

### Lamp Head Courier

The courier is a small traveler wearing a navy coat and satchel, with a glowing oil lamp in place of a head. The character does not speak. Direction, posture, the brightness of the lamp, and short poses communicate the courier's state. Warm gold and cream separate the courier from the cold blue-grey market.

The courier begins with the Beam and ten HP. Movement follows the keyboard, arrow keys, or left stick. The courier gains stronger attacks and passive abilities through level-up cards, but never receives a manual attack button. This keeps the player's attention on movement, spacing, and upgrade choices.

Current Lamp-Head Courier pose sheet used by the prototype

### Planned Courier Specializations

The Lamp-Head Courier is the first playable character, not the only one planned for the finished game. Later couriers will begin with different weapons and mechanics. One example is an engineer-style courier who can place automatic turrets. This character would trade immediate mobility or direct damage for controlling safe areas, deciding where to deploy equipment, and defending a delivery route. Other couriers can specialize in speed, close-range light, long-range attacks, support, or resource collection.

The post office will make these differences visible before a mission. Players will select a courier, review the starting weapon and specialty, choose a contract, and set the difficulty. Long-term upgrades will improve both the courier and that courier's initial weapon while preserving meaningful differences between characters.

### Initial Courier Roster

| Courier | Starting kit | Specialization | Tradeoff |
|---|---|---|---|
| Lamp-Head | Beam | Balanced light, weapon, and oil upgrades | No exceptional strength |
| Engineer | Deployable turret | Controls safe areas and defends routes | Lower direct damage and speed |
| Runner | Beacon knives | Builds speed and attack rate while moving | Lower maximum health |
| Guardian | Shield lantern | Protects cargo and knocks enemies back | Slow movement and weak range |
| Medic | Tonic burner | Oil pickups heal; excess healing boosts damage | Low base damage |
| Scavenger | Magnet hook | Finds more scrap and gathers from farther away | Weak early combat |

Later unlocks can include a long-range Hunter, a summon-focused Mothkeeper, a close-range Fog Walker, and an Archivist who can reroll or preserve upgrade cards. Each new courier must add one strong advantage, one rule change, and one meaningful weakness rather than only changing statistics.

## Story

After the apocalypse, survivors remain in scattered settlements, but the fog prevents radio signals, safe roads, and reliable contact. Without communication, communities cannot coordinate, share knowledge, or know whether neighboring towns still exist. Lantern couriers become the connection between them. They carry letters, medicine, plans, and supplies through territory filled with hostile insects and fog-wraiths.

Each completed delivery creates a visible improvement at its destination: new equipment becomes available, a damaged facility reopens, defenses improve, or residents provide a new route and contract. The post office records these connections and serves as the center of the courier network. The current prototype represents one dangerous market route; later missions will reveal additional settlements, characters, and pieces of the larger disaster.

## Gameplay

### Goal

Complete the assigned delivery by surviving the route and reaching the destination. In the current three-minute prototype, this means surviving until the fog lifts. The player also tries to collect enough lamp oil to improve both weapons and unlock Sunflare before the final wave.

### Game Mechanics

- Move with WASD, the arrow keys, or the gamepad left stick.
- Beam and Lamp-Moths attack automatically; the player chooses position rather than aiming or firing.
- Collect lamp-oil gems to fill the experience gauge.
- Choose one of three cards when leveling. The field pauses during the choice.
- Avoid contact damage, use solid market props carefully, and exploit short invulnerability after a hit.
- In planned character kits, use a specialization such as turret placement to shape safe routes and control enemy pressure.

### Abilities and Power Ups

| Upgrade | Effect |
|---|---|
| Beam | Improves through faster firing or extra pierce; reaches level 3. |
| Lamp-Moths | Adds orbiting moths or widens their orbit; reaches level 3. |
| Hotter Flame | Raises damage for every weapon. |
| Quick Hands | Raises overall attack speed. |
| Light Boots | Raises movement speed. |
| Magnet Satchel | Increases lamp-oil pickup range. |
| Thick Glass | Raises maximum health. |
| Sunflare Lighthouse | Appears after both weapons reach level 3 and creates a repeating radial light burst. |
| Deployable turret | A planned engineer-courier starting tool that attacks automatically after the player chooses its position. |
| Additional weapons | Planned character-linked weapons will create distinct builds, ranges, targeting rules, and evolution paths. |

### Levels and Challenges

The current prototype uses one three-minute market run divided into six thirty-second pressure steps. Enemy density rises at each step, fog-wraiths add heavier pressure, and enemy health increases after each full minute. In the planned campaign, the post office will offer multiple delivery contracts and difficulty levels. Harder routes can change enemy combinations, time limits, environmental hazards, and delivery conditions rather than only increasing enemy health. Future maps will connect different settlements and end with major threats such as a fog boss.

### Losing and Restarting

The player loses when HP reaches zero. The current result panel shows that the lamp went out, the survival time, and the restart control; R or gamepad Y begins a clean run immediately. The prototype does not yet carry progress between runs. In the planned campaign, successful deliveries will improve destinations and earn post-office resources for upgrading couriers and their starting weapons. Failure will return the player to the post office without applying the destination benefit.

### Player Skills

- Reading enemy movement and identifying an escape route before the crowd closes in.
- Maintaining useful distance so automatic weapons can work without taking contact damage.
- Choosing upgrades that support the current run instead of selecting only short-term damage.
- Using solid props as route constraints without becoming trapped against them.
- Balancing risky gem collection against health, time, and crowd density.
- Selecting a courier and placing specialist tools to suit each contract.

## Systems and Progression

| ID | System | Current or planned behavior |
|---|---|---|
| S-01 | Run progression | Current prototype: oil fills the experience gauge and offers one of three upgrade cards. |
| S-02 | Weapon evolution | Current prototype: maxing Beam and Lamp-Moths unlocks Sunflare Lighthouse. |
| S-03 | Delivery contracts | Planned: each contract defines destination, cargo, route condition, difficulty, and reward. |
| S-04 | Post office | Planned: select courier, starting kit, contract, difficulty, and permanent improvements. |
| S-05 | Settlement growth | Planned: successful deliveries reopen facilities, improve defenses, and reveal routes. |
| S-06 | Courier growth | Planned: resources improve a courier and that courier's starting weapon without erasing class weaknesses. |

The intended progression has two clocks. A single mission provides temporary upgrades that reset at the end of the route. The campaign provides slower, persistent improvements through the post office and destination network. Permanent growth should expand options and reliability without removing the need to move, position, and make upgrade choices during a run.

## Graphics and Styling

The game uses hard-edged 2D pixel art in a three-quarter top-down view. The courier, friendly effects, pickups, and upgrades use warm lamp gold and cream. Enemies, fog, and the cobblestone ground use cool navy and blue-grey. The player and pickups are the brightest objects, enemies sit at mid-value, and the ground remains darkest. Thick outlines and fixed palettes keep small sprites readable at the 640 by 360 logical resolution.

The market is intentionally irregular rather than arranged as two clean streets. Fourteen scattered prop clusters create narrow alleys, open wet squares, and isolated landmarks. Camera movement supports major moments: a slow title push-in, a brief hurt tilt, a Sunflare zoom-out, and a pull-back when the fog lifts.

Sunflare Lighthouse in the current Godot prototype

## Music and Sound Effects

A looping night-market track begins when the run starts. Level-up choices reduce the music by 6 dB, while pause applies a low-pass filter and lowers the volume further. Sunflare fades in a synchronized second music layer. Losing fades the loop over half a second before a loss stinger; winning uses a one-second fade before the win stinger.

| Event | Sound and visual feedback |
|---|---|
| Enemy defeated | A short warm pop; the enemy breaks into a visible lamp-oil gem. |
| Gem collected | A soft chime; the gem visibly flies into the courier's satchel. |
| Player hurt | A muffled thud; red flash, knockback, pose change, and HP loss remain visible. |
| Level up | A glassy bell; the game pauses and three cards appear. |
| Sunflare | A larger evolution sound; the banner, brighter palette, radial burst, and music layer appear. |
| Win or lose | A distinct stinger follows the music fade and the result panel appears. |

The game remains fully playable without audio. M mutes everything, 9 toggles music, and 0 toggles effects. Every sound-producing event also has visual feedback, and the HUD always shows the current music and effects state.

## Technical Description

| Area | Implementation |
|---|---|
| Engine | Godot 4.7.2 using GDScript and the GL Compatibility renderer. |
| Display | 640 by 360 logical viewport displayed in a 1280 by 720 window with nearest-neighbor filtering. |
| Game structure | A signal-driven state machine controls menu, play, level-up, pause, win, loss, and restart states. |
| Content | 2D pixel sprites, WAV sound effects, looping music, UI cards, and a separate Godot 3D asset room. |
| Input | Keyboard and gamepad movement; keyboard or gamepad card selection and restart controls. |
| Testing | Headless Godot checks cover logic, movement, weapons, progression, audio independence, win and loss, restart, and asset imports. |
| Current platform | Developed and tested on macOS 26 with Apple M4 Pro. The Godot project is designed to remain portable. |

### Platform Scope

The approved target is a single-player desktop build with keyboard and gamepad support. Mobile touch controls, networked multiplayer, and XR are outside the current course build. They have not been implemented or verified, and this document does not claim support for them. A future mobile version would require a redesigned touch interface and device testing; networked play would require authority, synchronization, and security decisions; XR would require a separate interaction and comfort design.

## Development Scope

The course version should first polish the existing three-minute loop: clearer enemy readability, stronger integration of the Lantern Gate, Supply Stack, and Lamp-oil Shrine, and continued balance testing. The next playable milestone should add the post-office hub, a simple contract and difficulty selector, persistent destination improvements, and one additional courier: an engineer who places automatic turrets.

After that foundation is stable, the game can expand with more specialized couriers, distinct starting weapons, additional evolution recipes, new delivery conditions, more settlements and market maps, a fog boss, deeper character and weapon upgrades, and saving. These items describe the intended full game and are not presented as features already implemented in the current prototype.

### Feature Priorities

| ID | Feature | State | Priority |
|---|---|---|---|
| F-01 | Three-minute survival route | Implemented | Core |
| F-02 | Automatic combat and movement | Implemented | Core |
| F-03 | Run upgrades and Sunflare | Implemented | Core |
| F-04 | Delivery objective and result | Planned | Core |
| F-05 | Post-office hub | Planned | High |
| F-06 | Six-courier initial roster | Planned | High |
| F-07 | Contracts and difficulty | Planned | High |
| F-08 | Destination improvements | Planned | High |
| F-09 | Additional maps and fog boss | Planned | Later |
| F-10 | Saving and deeper progression | Planned | Later |

## Out of Scope

- Multiplayer, competitive modes, and shared online settlements for the current course version.
- Mobile and XR releases, including their platform-specific controls and hardware testing.
- A large open world; missions use bounded routes and reusable settlement hubs.
- All proposed couriers at once; the next milestone adds only the Engineer after the Lamp-Head Courier.
- Fully voiced dialogue or cinematic cutscenes; narrative is carried by letters, locations, and visible settlement changes.

## Risks and Mitigations

| ID | Risk | Mitigation |
|---|---|---|
| R-01 | The hub, roster, and meta-progression expand scope too quickly. | Build one post-office screen, one contract, and the Engineer before adding more content. |
| R-02 | Couriers feel like statistical variations instead of new play styles. | Require one advantage, one rule change, and one weakness for every character. |
| R-03 | Turrets create pathing clutter or excessive runtime cost. | Limit active turrets, reuse objects, and test readability and frame time under maximum enemy load. |
| R-04 | Permanent upgrades make early missions trivial. | Favor new options and starting-kit improvements over unlimited numerical scaling. |
| R-05 | Delivery consequences feel abstract. | Show a visible destination change and state the unlocked benefit after every successful contract. |

## Open Questions

- Q-01 Should every delivery end by surviving a timer, reaching an exit, or satisfying a contract-specific condition?
- Q-02 Should active specialties such as turret placement use one shared ability button for every courier?
- Q-03 What resources, if any, should a failed delivery return to the post office?
- Q-04 Are six couriers required for the first public version, or should four ship before the remaining two?
- Q-05 How much can a starting weapon improve before character weaknesses lose their meaning?

## Revision History

| Version | Date | Change |
|---|---|---|
| 0.1 | 17 Oct 2026 | Initial GDD based on the playable Lanternfall prototype. |
| 0.2 | 17 Oct 2026 | Added the apocalypse, courier network, post office, and persistent destination growth. |
| 0.3 | 17 Oct 2026 | Added courier specializations, stable IDs, priorities, scope boundaries, risks, and open questions. |
