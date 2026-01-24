import re
import numpy as np
from clash_utils import find_closest_match

# Original list of card names
original_list = [
    "MinionsCard",
    "ArchersCard",
    "KnightCard",
    "SpearGoblinsCard",
    "GoblinsCard",
    "BomberCard",
    "SkeletonsCard",
    "BarbariansCard",
    "ElectroSpiritCard",
    "SkeletonDragonsCard",
    "FireSpiritCard",
    "BatsCard",
    "RoyalRecruitsCard",
    "RoyalGiantCard",
    "IceSpiritCard",
    "BerserkerCard",
    "SkeletonBarrelCard",
    "GoblinGangCard",
    "EliteBarbariansCard",
    "MinionHordeCard",
    "FirecrackerCard",
    "RascalsCard",
    "MiniPEKKACard",
    "MusketeerCard",
    "GiantCard",
    "ValkyrieCard",
    "MegaMinionCard",
    "BattleRamCard",
    "WizardCard",
    "FlyingMachineCard",
    "HogRiderCard",
    "RoyalHogsCard",
    "ThreeMusketeersCard",
    "BattleHealerCard",
    "IceGolemCard",
    "DartGoblinCard",
    "ZappiesCard",
    "GoblinDemolisherCard",
    "HealSpiritCard",
    "SuspiciousBushCard",
    "ElixirGolemCard",
    "GuardsCard",
    "BabyDragonCard",
    "SkeletonArmyCard",
    "WitchCard",
    "PEKKACard",
    "DarkPrinceCard",
    "PrinceCard",
    "BalloonCard",
    "GiantSkeletonCard",
    "RuneGiantCard",
    "GoblinGiantCard",
    "HunterCard",
    "GolemCard",
    "ElectroDragonCard",
    "WallBreakersCard",
    "ElectroGiantCard",
    "BowlerCard",
    "ExecutionerCard",
    "CannonCartCard",
    "MegaKnightCard",
    "RamRiderCard",
    "ElectroWizardCard",
    "InfernoDragonCard",
    "SparkyCard",
    "MinerCard",
    "PrincessCard",
    "PhoenixCard",
    "RoyalGhostCard",
    "IceWizardCard",
    "MagicArcherCard",
    "BanditCard",
    "LavaHoundCard",
    "NightWitchCard",
    "LumberjackCard",
    "GoblinMachineCard",
    "MotherWitchCard",
    "FishermanCard",
    "GoldenKnightCard",
    "SkeletonKingCard",
    "BossBanditCard",
    "ArcherQueenCard",
    "MightyMinerCard",
    "GoblinsteinCard",
    "LittlePrinceCard",
    "MonkCard",
    "ArrowsCard",
    "ZapCard",
    "GiantSnowballCard",
    "RoyalDeliveryCard",
    "FireballCard",
    "RocketCard",
    "EarthquakeCard",
    "GoblinBarrelCard",
    "LightningCard",
    "FreezeCard",
    "BarbarianBarrelCard",
    "PoisonCard",
    "GoblinCurseCard",
    "RageCard",
    "CloneCard",
    "TornadoCard",
    "MirrorCard",
    "VoidCard",
    "TheLogCard",
    "GraveyardCard",
    "CannonCard",
    "MortarCard",
    "TeslaCard",
    "GoblinCageCard",
    "GoblinHutCard",
    "TombstoneCard",
    "BombTowerCard",
    "InfernoTowerCard",
    "BarbarianHutCard",
    "FurnaceCard",
    "ElixirCollectorCard",
    "X-BowCard",
    "GoblinDrillCard",
    "TowerPrincessCard",
    "CannoneerCard",
    "DaggerDuchessCard",
    "RoyalChefCard",
]

# HTML content with elixir costs
html_content = """
<div class="mb-4 flex items-center">

<span class="text-fuchsia-600 mb-0 text-3xl min-w-[3.23rem]"><img src="/img/elixirdrop.png" class="h-6 inline-block" alt=""> 1</span>

<div class="flex flex-wrap items-center">
<a href="/card/detail/skeletons"><img src="/img/c/Skellies.png" alt="Skeletons" class="card"></a>
<a href="/card/detail/electro-spirit"><img src="/img/c/ElectroSpirit.png" alt="Electro Spirit" class="card"></a>
<a href="/card/detail/fire-spirit"><img src="/img/c/FireSpirit.png" alt="Fire Spirit" class="card"></a>
<a href="/card/detail/ice-spirit"><img src="/img/c/IceSpirit.png" alt="Ice Spirit" class="card"></a>
<a href="/card/detail/heal-spirit"><img src="/img/c/HealSpirit.png" alt="Heal Spirit" class="card"></a>
</div>
</div>


<div class="mb-4 flex items-center">

<span class="text-fuchsia-600 mb-0 text-3xl min-w-[3.23rem]"><img src="/img/elixirdrop.png" class="h-6 inline-block" alt=""> 2</span>

<div class="flex flex-wrap items-center">
<a href="/card/detail/goblins"><img src="/img/c/Gobs.png" alt="Goblins" class="card"></a>
<a href="/card/detail/spear-goblins"><img src="/img/c/SpearGobs.png" alt="Spear Goblins" class="card"></a>
<a href="/card/detail/bomber"><img src="/img/c/Bomber.png" alt="Bomber" class="card"></a>
<a href="/card/detail/bats"><img src="/img/c/Bats.png" alt="Bats" class="card"></a>
<a href="/card/detail/zap"><img src="/img/c/Zap.png" alt="Zap" class="card"></a>
<a href="/card/detail/giant-snowball"><img src="/img/c/Snowball.png" alt="Giant Snowball" class="card"></a>
<a href="/card/detail/berserker"><img src="/img/c/Berserker.png" alt="Berserker" class="card"></a>
<a href="/card/detail/ice-golem"><img src="/img/c/IceGolem.png" alt="Ice Golem" class="card"></a>
<a href="/card/detail/suspicious-bush"><img src="/img/c/SuspiciousBush.png" alt="Suspicious Bush" class="card"></a>
<a href="/card/detail/barbarian-barrel"><img src="/img/c/BarbBarrel.png" alt="Barbarian Barrel" class="card"></a>
<a href="/card/detail/wall-breakers"><img src="/img/c/WallBreakers.png" alt="Wall Breakers" class="card"></a>
<a href="/card/detail/goblin-curse"><img src="/img/c/GoblinCurse.png" alt="Goblin Curse" class="card"></a>
<a href="/card/detail/rage"><img src="/img/c/Rage.png" alt="Rage" class="card"></a>
<a href="/card/detail/the-log"><img src="/img/c/Log.png" alt="The Log" class="card"></a>
</div>
</div>


<div class="mb-4 flex items-center">

<span class="text-fuchsia-600 mb-0 text-3xl min-w-[3.23rem]"><img src="/img/elixirdrop.png" class="h-6 inline-block" alt=""> 3</span>

<div class="flex flex-wrap items-center">
<a href="/card/detail/archers"><img src="/img/c/Archers.png" alt="Archers" class="card"></a>
<a href="/card/detail/arrows"><img src="/img/c/Arrows.png" alt="Arrows" class="card"></a>
<a href="/card/detail/knight"><img src="/img/c/Knight.png" alt="Knight" class="card"></a>
<a href="/card/detail/minions"><img src="/img/c/Minions.png" alt="Minions" class="card"></a>
<a href="/card/detail/cannon"><img src="/img/c/Cannon.png" alt="Cannon" class="card"></a>
<a href="/card/detail/goblin-gang"><img src="/img/c/GobGang.png" alt="Goblin Gang" class="card"></a>
<a href="/card/detail/skeleton-barrel"><img src="/img/c/SkellyBarrel.png" alt="Skeleton Barrel" class="card"></a>
<a href="/card/detail/firecracker"><img src="/img/c/Firecracker.png" alt="Firecracker" class="card"></a>
<a href="/card/detail/royal-delivery"><img src="/img/c/RoyalDelivery.png" alt="Royal Delivery" class="card"></a>
<a href="/card/detail/tombstone"><img src="/img/c/Tombstone.png" alt="Tombstone" class="card"></a>
<a href="/card/detail/mega-minion"><img src="/img/c/MM.png" alt="Mega Minion" class="card"></a>
<a href="/card/detail/dart-goblin"><img src="/img/c/DartGob.png" alt="Dart Goblin" class="card"></a>
<a href="/card/detail/earthquake"><img src="/img/c/Earthquake.png" alt="Earthquake" class="card"></a>
<a href="/card/detail/elixir-golem"><img src="/img/c/ElixirGolem.png" alt="Elixir Golem" class="card"></a>
<a href="/card/detail/goblin-barrel"><img src="/img/c/Barrel.png" alt="Goblin Barrel" class="card"></a>
<a href="/card/detail/guards"><img src="/img/c/Guards.png" alt="Guards" class="card"></a>
<a href="/card/detail/skeleton-army"><img src="/img/c/Skarmy.png" alt="Skeleton Army" class="card"></a>
<a href="/card/detail/clone"><img src="/img/c/Clone.png" alt="Clone" class="card"></a>
<a href="/card/detail/tornado"><img src="/img/c/Tornado.png" alt="Tornado" class="card"></a>
<a href="/card/detail/void"><img src="/img/c/Void.png" alt="Void" class="card"></a>
<a href="/card/detail/miner"><img src="/img/c/Miner.png" alt="Miner" class="card"></a>
<a href="/card/detail/princess"><img src="/img/c/Princess.png" alt="Princess" class="card"></a>
<a href="/card/detail/ice-wizard"><img src="/img/c/IceWiz.png" alt="Ice Wizard" class="card"></a>
<a href="/card/detail/royal-ghost"><img src="/img/c/Ghost.png" alt="Royal Ghost" class="card"></a>
<a href="/card/detail/bandit"><img src="/img/c/Bandit.png" alt="Bandit" class="card"></a>
<a href="/card/detail/fisherman"><img src="/img/c/Fisherman.png" alt="Fisherman" class="card"></a>
<a href="/card/detail/little-prince"><img src="/img/c/LittlePrince.png" alt="Little Prince" class="card"></a>
</div>
</div>


<div class="mb-4 flex items-center">

<span class="text-fuchsia-600 mb-0 text-3xl min-w-[3.23rem]"><img src="/img/elixirdrop.png" class="h-6 inline-block" alt=""> 4</span>

<div class="flex flex-wrap items-center">
<a href="/card/detail/skeleton-dragons"><img src="/img/c/SkeletonDragons.png" alt="Skeleton Dragons" class="card"></a>
<a href="/card/detail/mortar"><img src="/img/c/Mortar.png" alt="Mortar" class="card"></a>
<a href="/card/detail/tesla"><img src="/img/c/Tesla.png" alt="Tesla" class="card"></a>
<a href="/card/detail/fireball"><img src="/img/c/Fireball.png" alt="Fireball" class="card"></a>
<a href="/card/detail/mini-pekka"><img src="/img/c/MP.png" alt="Mini P.E.K.K.A" class="card"></a>
<a href="/card/detail/musketeer"><img src="/img/c/Musk.png" alt="Musketeer" class="card"></a>
<a href="/card/detail/goblin-cage"><img src="/img/c/GoblinCage.png" alt="Goblin Cage" class="card"></a>
<a href="/card/detail/goblin-hut"><img src="/img/c/GobHut.png" alt="Goblin Hut" class="card"></a>
<a href="/card/detail/valkyrie"><img src="/img/c/Valk.png" alt="Valkyrie" class="card"></a>
<a href="/card/detail/battle-ram"><img src="/img/c/Ram.png" alt="Battle Ram" class="card"></a>
<a href="/card/detail/bomb-tower"><img src="/img/c/BombTower.png" alt="Bomb Tower" class="card"></a>
<a href="/card/detail/flying-machine"><img src="/img/c/FlyingMachine.png" alt="Flying Machine" class="card"></a>
<a href="/card/detail/hog-rider"><img src="/img/c/Hog.png" alt="Hog Rider" class="card"></a>
<a href="/card/detail/battle-healer"><img src="/img/c/BattleHealer.png" alt="Battle Healer" class="card"></a>
<a href="/card/detail/furnace"><img src="/img/c/Furnace.png" alt="Furnace" class="card"></a>
<a href="/card/detail/zappies"><img src="/img/c/Zappies.png" alt="Zappies" class="card"></a>
<a href="/card/detail/goblin-demolisher"><img src="/img/c/GoblinDemolisher.png" alt="Goblin Demolisher" class="card"></a>
<a href="/card/detail/baby-dragon"><img src="/img/c/BabyD.png" alt="Baby Dragon" class="card"></a>
<a href="/card/detail/dark-prince"><img src="/img/c/DarkPrince.png" alt="Dark Prince" class="card"></a>
<a href="/card/detail/freeze"><img src="/img/c/Freeze.png" alt="Freeze" class="card"></a>
<a href="/card/detail/poison"><img src="/img/c/Poison.png" alt="Poison" class="card"></a>
<a href="/card/detail/rune-giant"><img src="/img/c/RuneGiant.png" alt="Rune Giant" class="card"></a>
<a href="/card/detail/hunter"><img src="/img/c/Hunter.png" alt="Hunter" class="card"></a>
<a href="/card/detail/goblin-drill"><img src="/img/c/GoblinDrill.png" alt="Goblin Drill" class="card"></a>
<a href="/card/detail/electro-wizard"><img src="/img/c/eWiz.png" alt="Electro Wizard" class="card"></a>
<a href="/card/detail/inferno-dragon"><img src="/img/c/InfernoD.png" alt="Inferno Dragon" class="card"></a>
<a href="/card/detail/phoenix"><img src="/img/c/Phoenix.png" alt="Phoenix" class="card"></a>
<a href="/card/detail/magic-archer"><img src="/img/c/MagicArcher.png" alt="Magic Archer" class="card"></a>
<a href="/card/detail/lumberjack"><img src="/img/c/Lumber.png" alt="Lumberjack" class="card"></a>
<a href="/card/detail/night-witch"><img src="/img/c/NightWitch.png" alt="Night Witch" class="card"></a>
<a href="/card/detail/mother-witch"><img src="/img/c/MotherWitch.png" alt="Mother Witch" class="card"></a>
<a href="/card/detail/golden-knight"><img src="/img/c/GoldenKnight.png" alt="Golden Knight" class="card"></a>
<a href="/card/detail/skeleton-king"><img src="/img/c/SkeletonKing.png" alt="Skeleton King" class="card"></a>
<a href="/card/detail/mighty-miner"><img src="/img/c/MightyMiner.png" alt="Mighty Miner" class="card"></a>
</div>
</div>


<div class="mb-4 flex items-center">

<span class="text-fuchsia-600 mb-0 text-3xl min-w-[3.23rem]"><img src="/img/elixirdrop.png" class="h-6 inline-block" alt=""> 5</span>

<div class="flex flex-wrap items-center">
<a href="/card/detail/barbarians"><img src="/img/c/Barbs.png" alt="Barbarians" class="card"></a>
<a href="/card/detail/minion-horde"><img src="/img/c/Horde.png" alt="Minion Horde" class="card"></a>
<a href="/card/detail/rascals"><img src="/img/c/Rascals.png" alt="Rascals" class="card"></a>
<a href="/card/detail/giant"><img src="/img/c/Giant.png" alt="Giant" class="card"></a>
<a href="/card/detail/inferno-tower"><img src="/img/c/Inferno.png" alt="Inferno Tower" class="card"></a>
<a href="/card/detail/wizard"><img src="/img/c/Wiz.png" alt="Wizard" class="card"></a>
<a href="/card/detail/royal-hogs"><img src="/img/c/RoyalHogs.png" alt="Royal Hogs" class="card"></a>
<a href="/card/detail/witch"><img src="/img/c/Witch.png" alt="Witch" class="card"></a>
<a href="/card/detail/balloon"><img src="/img/c/Balloon.png" alt="Balloon" class="card"></a>
<a href="/card/detail/prince"><img src="/img/c/Prince.png" alt="Prince" class="card"></a>
<a href="/card/detail/electro-dragon"><img src="/img/c/eDragon.png" alt="Electro Dragon" class="card"></a>
<a href="/card/detail/bowler"><img src="/img/c/Bowler.png" alt="Bowler" class="card"></a>
<a href="/card/detail/executioner"><img src="/img/c/Exe.png" alt="Executioner" class="card"></a>
<a href="/card/detail/cannon-cart"><img src="/img/c/CannonCart.png" alt="Cannon Cart" class="card"></a>
<a href="/card/detail/ram-rider"><img src="/img/c/RamRider.png" alt="Ram Rider" class="card"></a>
<a href="/card/detail/graveyard"><img src="/img/c/Graveyard.png" alt="Graveyard" class="card"></a>
<a href="/card/detail/goblin-machine"><img src="/img/c/GoblinMachine.png" alt="Goblin Machine" class="card"></a>
<a href="/card/detail/archer-queen"><img src="/img/c/ArcherQueen.png" alt="Archer Queen" class="card"></a>
<a href="/card/detail/goblinstein"><img src="/img/c/Goblinstein.png" alt="Goblinstein" class="card"></a>
<a href="/card/detail/monk"><img src="/img/c/Monk.png" alt="Monk" class="card"></a>
</div>
</div>


<div class="mb-4 flex items-center">

<span class="text-fuchsia-600 mb-0 text-3xl min-w-[3.23rem]"><img src="/img/elixirdrop.png" class="h-6 inline-block" alt=""> 6</span>

<div class="flex flex-wrap items-center">
<a href="/card/detail/royal-giant"><img src="/img/c/RG.png" alt="Royal Giant" class="card"></a>
<a href="/card/detail/elite-barbarians"><img src="/img/c/eBarbs.png" alt="Elite Barbarians" class="card"></a>
<a href="/card/detail/rocket"><img src="/img/c/Rocket.png" alt="Rocket" class="card"></a>
<a href="/card/detail/barbarian-hut"><img src="/img/c/BarbHut.png" alt="Barbarian Hut" class="card"></a>
<a href="/card/detail/elixir-collector"><img src="/img/c/Pump.png" alt="Elixir Collector" class="card"></a>
<a href="/card/detail/giant-skeleton"><img src="/img/c/GiantSkelly.png" alt="Giant Skeleton" class="card"></a>
<a href="/card/detail/lightning"><img src="/img/c/Lightning.png" alt="Lightning" class="card"></a>
<a href="/card/detail/goblin-giant"><img src="/img/c/GobGiant.png" alt="Goblin Giant" class="card"></a>
<a href="/card/detail/x-bow"><img src="/img/c/XBow.png" alt="X-Bow" class="card"></a>
<a href="/card/detail/sparky"><img src="/img/c/Sparky.png" alt="Sparky" class="card"></a>
<a href="/card/detail/boss-bandit"><img src="/img/c/BossBandit.png" alt="Boss Bandit" class="card"></a>
</div>
</div>


<div class="mb-4 flex items-center">

<span class="text-fuchsia-600 mb-0 text-3xl min-w-[3.23rem]"><img src="/img/elixirdrop.png" class="h-6 inline-block" alt=""> 7</span>

<div class="flex flex-wrap items-center">
<a href="/card/detail/royal-recruits"><img src="/img/c/RoyalRecruits.png" alt="Royal Recruits" class="card"></a>
<a href="/card/detail/pekka"><img src="/img/c/PEKKA.png" alt="P.E.K.K.A" class="card"></a>
<a href="/card/detail/electro-giant"><img src="/img/c/ElectroGiant.png" alt="Electro Giant" class="card"></a>
<a href="/card/detail/mega-knight"><img src="/img/c/MegaKnight.png" alt="Mega Knight" class="card"></a>
<a href="/card/detail/lava-hound"><img src="/img/c/Lava.png" alt="Lava Hound" class="card"></a>
</div>
</div>


<div class="mb-4 flex items-center">

<span class="text-fuchsia-600 mb-0 text-3xl min-w-[3.23rem]"><img src="/img/elixirdrop.png" class="h-6 inline-block" alt=""> 8</span>

<div class="flex flex-wrap items-center">
<a href="/card/detail/golem"><img src="/img/c/Golem.png" alt="Golem" class="card"></a>
</div>
</div>


<div class="mb-4 flex items-center">

<span class="text-fuchsia-600 mb-0 text-3xl min-w-[3.23rem]"><img src="/img/elixirdrop.png" class="h-6 inline-block" alt=""> 9</span>

<div class="flex flex-wrap items-center">
<a href="/card/detail/three-musketeers"><img src="/img/c/3M.png" alt="Three Musketeers" class="card"></a>
</div>
</div>


<div class="mb-4 flex items-center">

<span class="text-fuchsia-600 mb-0 text-3xl min-w-[3.23rem]"><img src="/img/elixirdrop.png" class="h-6 inline-block" alt=""> 10</span>

<div class="flex flex-wrap items-center">
</div>
</div>
"""


# Function to extract card names and their elixir costs from HTML
def extract_cards_and_costs(html):
    card_costs = {}
    pattern = re.compile(
        r'<span class="text-fuchsia-600 mb-0 text-3xl min-w-\[3\.23rem\]"><img src="/img/elixirdrop\.png" class="h-6 inline-block" alt=""> (\d+)</span>.*?<div class="flex flex-wrap items-center">(.*?)</div>',
        re.DOTALL,
    )
    matches = pattern.findall(html)
    for match in matches:
        cost = int(match[0])
        cards_html = match[1]
        card_names = re.findall(r'alt="([^"]+)"', cards_html)
        card_costs[cost] = card_names
    return card_costs


# Extract card names and their elixir costs from HTML
card_costs = extract_cards_and_costs(html_content)


# Initialize arrays for each elixir cost
elixir_cost_arrays = {i: [] for i in range(1, 10)}

# Match card names from HTML to original list and group them by elixir cost
for cost, cards in card_costs.items():
    for card in cards:
        closest_match = find_closest_match(card, original_list)
        if closest_match:
            elixir_cost_arrays[cost].append(closest_match)

# Print the arrays for each elixir cost
for cost, cards in elixir_cost_arrays.items():
    print(f"Elixir Cost {cost}: {cards}")

# Print how many cards were in the original list
print(f"Total cards in original list: {len(original_list)}")
# Print how many cards were matched
matched_count = sum(len(cards) for cards in elixir_cost_arrays.values())
print(f"Total matched cards: {matched_count}")

# Print how many cards were not matched
not_matched = len(original_list) - matched_count

print(f"Total not matched cards: {not_matched}")
# Print the unmatched cards
unmatched_cards = [card for card in original_list if not any(card in cards for cards in elixir_cost_arrays.values())]
print(f"Unmatched cards: {unmatched_cards}")
