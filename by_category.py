import re
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
    "MinionHorde Card",
    " FirecrackerCard",
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
<main class="page-container py-1 lg:py-2 xl:py-3">

<nav class="bg-gray-dark mb-5 flex justify-center gap-5 px-page py-3">
    <a href="/card/list" class="disabled">
        List
    </a>
    <a href="/card/by-arena">
        <span class="hidden md:block">By Arena</span>
        <span class="md:hidden">Arena</span>
    </a>
    <a href="/card/damage">
        <span class="hidden md:block">Damage</span>
        <span class="md:hidden">Dmg</span>
    </a>
    <a href="/card/hitpoints">
        <span class="hidden md:block">Hitpoints</span>
        <span class="md:hidden">Hp</span>
    </a>
    <a href="/card/stats">
        <span class="hidden md:block">Other stats</span>
        <span class="md:hidden">Stats</span>
    </a>
    <a href="/card/nerds">
        <span class="hidden md:block">For nerds</span>
        <span class="md:hidden">Nerds</span>
    </a>
</nav>


<article class="px-page xl:px-0">

    <section class="">

        <h3 class="mb-3">With evolutions</h3>

        <div class="mb-4 flex flex-wrap items-center">
                <a href="/card/detail/skeletons?evolution=1"><img src="/img/card_ed_evo/Skellies.png" alt="Skeletons" class="card"></a>
                <a href="/card/detail/ice-spirit?evolution=1"><img src="/img/card_ed_evo/IceSpirit.png" alt="Ice Spirit" class="card"></a>
                <a href="/card/detail/bomber?evolution=1"><img src="/img/card_ed_evo/Bomber.png" alt="Bomber" class="card"></a>
                <a href="/card/detail/bats?evolution=1"><img src="/img/card_ed_evo/Bats.png" alt="Bats" class="card"></a>
                <a href="/card/detail/zap?evolution=1"><img src="/img/card_ed_evo/Zap.png" alt="Zap" class="card"></a>
                <a href="/card/detail/giant-snowball?evolution=1"><img src="/img/card_ed_evo/Snowball.png" alt="Giant Snowball" class="card"></a>
                <a href="/card/detail/archers?evolution=1"><img src="/img/card_ed_evo/Archers.png" alt="Archers" class="card"></a>
                <a href="/card/detail/knight?evolution=1"><img src="/img/card_ed_evo/Knight.png" alt="Knight" class="card"></a>
                <a href="/card/detail/cannon?evolution=1"><img src="/img/card_ed_evo/Cannon.png" alt="Cannon" class="card"></a>
                <a href="/card/detail/firecracker?evolution=1"><img src="/img/card_ed_evo/Firecracker.png" alt="Firecracker" class="card"></a>
                <a href="/card/detail/mortar?evolution=1"><img src="/img/card_ed_evo/Mortar.png" alt="Mortar" class="card"></a>
                <a href="/card/detail/tesla?evolution=1"><img src="/img/card_ed_evo/Tesla.png" alt="Tesla" class="card"></a>
                <a href="/card/detail/barbarians?evolution=1"><img src="/img/card_ed_evo/Barbs.png" alt="Barbarians" class="card"></a>
                <a href="/card/detail/royal-giant?evolution=1"><img src="/img/card_ed_evo/RG.png" alt="Royal Giant" class="card"></a>
                <a href="/card/detail/royal-recruits?evolution=1"><img src="/img/card_ed_evo/RoyalRecruits.png" alt="Royal Recruits" class="card"></a>
                <a href="/card/detail/dart-goblin?evolution=1"><img src="/img/card_ed_evo/DartGob.png" alt="Dart Goblin" class="card"></a>
                <a href="/card/detail/musketeer?evolution=1"><img src="/img/card_ed_evo/Musk.png" alt="Musketeer" class="card"></a>
                <a href="/card/detail/goblin-cage?evolution=1"><img src="/img/card_ed_evo/GoblinCage.png" alt="Goblin Cage" class="card"></a>
                <a href="/card/detail/valkyrie?evolution=1"><img src="/img/card_ed_evo/Valk.png" alt="Valkyrie" class="card"></a>
                <a href="/card/detail/battle-ram?evolution=1"><img src="/img/card_ed_evo/Ram.png" alt="Battle Ram" class="card"></a>
                <a href="/card/detail/wizard?evolution=1"><img src="/img/card_ed_evo/Wiz.png" alt="Wizard" class="card"></a>
                <a href="/card/detail/wall-breakers?evolution=1"><img src="/img/card_ed_evo/WallBreakers.png" alt="Wall Breakers" class="card"></a>
                <a href="/card/detail/goblin-barrel?evolution=1"><img src="/img/card_ed_evo/Barrel.png" alt="Goblin Barrel" class="card"></a>
                <a href="/card/detail/hunter?evolution=1"><img src="/img/card_ed_evo/Hunter.png" alt="Hunter" class="card"></a>
                <a href="/card/detail/goblin-drill?evolution=1"><img src="/img/card_ed_evo/GoblinDrill.png" alt="Goblin Drill" class="card"></a>
                <a href="/card/detail/witch?evolution=1"><img src="/img/card_ed_evo/Witch.png" alt="Witch" class="card"></a>
                <a href="/card/detail/electro-dragon?evolution=1"><img src="/img/card_ed_evo/eDragon.png" alt="Electro Dragon" class="card"></a>
                <a href="/card/detail/executioner?evolution=1"><img src="/img/card_ed_evo/Exe.png" alt="Executioner" class="card"></a>
                <a href="/card/detail/goblin-giant?evolution=1"><img src="/img/card_ed_evo/GobGiant.png" alt="Goblin Giant" class="card"></a>
                <a href="/card/detail/pekka?evolution=1"><img src="/img/card_ed_evo/PEKKA.png" alt="P.E.K.K.A" class="card"></a>
                <a href="/card/detail/inferno-dragon?evolution=1"><img src="/img/card_ed_evo/InfernoD.png" alt="Inferno Dragon" class="card"></a>
                <a href="/card/detail/lumberjack?evolution=1"><img src="/img/card_ed_evo/Lumber.png" alt="Lumberjack" class="card"></a>
                <a href="/card/detail/mega-knight?evolution=1"><img src="/img/card_ed_evo/MegaKnight.png" alt="Mega Knight" class="card"></a>
        </div>

    </section>


    <div class="grid md:grid-cols-2 gap-5">
            <section class="">

                <h3 class="mb-3">By Rarity</h3>


                        <h4 class="text-yellow-300 mb-3">
                            Champion
                        </h4>

                    <div class="mb-4 flex flex-wrap items-center">
                            <a href="/card/detail/little-prince"><img src="/img/card_ed/LittlePrince.png" alt="Little Prince" class="card"></a>
                            <a href="/card/detail/golden-knight"><img src="/img/card_ed/GoldenKnight.png" alt="Golden Knight" class="card"></a>
                            <a href="/card/detail/skeleton-king"><img src="/img/card_ed/SkeletonKing.png" alt="Skeleton King" class="card"></a>
                            <a href="/card/detail/mighty-miner"><img src="/img/card_ed/MightyMiner.png" alt="Mighty Miner" class="card"></a>
                            <a href="/card/detail/archer-queen"><img src="/img/card_ed/ArcherQueen.png" alt="Archer Queen" class="card"></a>
                            <a href="/card/detail/goblinstein"><img src="/img/card_ed/Goblinstein.png" alt="Goblinstein" class="card"></a>
                            <a href="/card/detail/monk"><img src="/img/card_ed/Monk.png" alt="Monk" class="card"></a>
                            <a href="/card/detail/boss-bandit"><img src="/img/card_ed/BossBandit.png" alt="Boss Bandit" class="card"></a>
                    </div>


                        <h4 class="legendary mb-3">
                            Legendary
                        </h4>

                    <div class="mb-4 flex flex-wrap items-center">
                            <a href="/card/detail/the-log"><img src="/img/card_ed/Log.png" alt="The Log" class="card"></a>
                            <a href="/card/detail/miner"><img src="/img/card_ed/Miner.png" alt="Miner" class="card"></a>
                            <a href="/card/detail/princess"><img src="/img/card_ed/Princess.png" alt="Princess" class="card"></a>
                            <a href="/card/detail/ice-wizard"><img src="/img/card_ed/IceWiz.png" alt="Ice Wizard" class="card"></a>
                            <a href="/card/detail/royal-ghost"><img src="/img/card_ed/Ghost.png" alt="Royal Ghost" class="card"></a>
                            <a href="/card/detail/bandit"><img src="/img/card_ed/Bandit.png" alt="Bandit" class="card"></a>
                            <a href="/card/detail/fisherman"><img src="/img/card_ed/Fisherman.png" alt="Fisherman" class="card"></a>
                            <a href="/card/detail/electro-wizard"><img src="/img/card_ed/eWiz.png" alt="Electro Wizard" class="card"></a>
                            <a href="/card/detail/inferno-dragon"><img src="/img/card_ed/InfernoD.png" alt="Inferno Dragon" class="card"></a>
                            <a href="/card/detail/phoenix"><img src="/img/card_ed/Phoenix.png" alt="Phoenix" class="card"></a>
                            <a href="/card/detail/magic-archer"><img src="/img/card_ed/MagicArcher.png" alt="Magic Archer" class="card"></a>
                            <a href="/card/detail/lumberjack"><img src="/img/card_ed/Lumber.png" alt="Lumberjack" class="card"></a>
                            <a href="/card/detail/night-witch"><img src="/img/card_ed/NightWitch.png" alt="Night Witch" class="card"></a>
                            <a href="/card/detail/mother-witch"><img src="/img/card_ed/MotherWitch.png" alt="Mother Witch" class="card"></a>
                            <a href="/card/detail/ram-rider"><img src="/img/card_ed/RamRider.png" alt="Ram Rider" class="card"></a>
                            <a href="/card/detail/graveyard"><img src="/img/card_ed/Graveyard.png" alt="Graveyard" class="card"></a>
                            <a href="/card/detail/goblin-machine"><img src="/img/card_ed/GoblinMachine.png" alt="Goblin Machine" class="card"></a>
                            <a href="/card/detail/sparky"><img src="/img/card_ed/Sparky.png" alt="Sparky" class="card"></a>
                            <a href="/card/detail/mega-knight"><img src="/img/card_ed/MegaKnight.png" alt="Mega Knight" class="card"></a>
                            <a href="/card/detail/lava-hound"><img src="/img/card_ed/Lava.png" alt="Lava Hound" class="card"></a>
                    </div>


                        <h4 class="text-fuchsia-600 mb-3">
                            Epic
                        </h4>

                    <div class="mb-4 flex flex-wrap items-center">
                            <a href="/card/detail/mirror"><img src="/img/card_ed/Mirror.png" alt="Mirror" class="card"></a>
                            <a href="/card/detail/barbarian-barrel"><img src="/img/card_ed/BarbBarrel.png" alt="Barbarian Barrel" class="card"></a>
                            <a href="/card/detail/wall-breakers"><img src="/img/card_ed/WallBreakers.png" alt="Wall Breakers" class="card"></a>
                            <a href="/card/detail/goblin-curse"><img src="/img/card_ed/GoblinCurse.png" alt="Goblin Curse" class="card"></a>
                            <a href="/card/detail/rage"><img src="/img/card_ed/Rage.png" alt="Rage" class="card"></a>
                            <a href="/card/detail/goblin-barrel"><img src="/img/card_ed/Barrel.png" alt="Goblin Barrel" class="card"></a>
                            <a href="/card/detail/guards"><img src="/img/card_ed/Guards.png" alt="Guards" class="card"></a>
                            <a href="/card/detail/skeleton-army"><img src="/img/card_ed/Skarmy.png" alt="Skeleton Army" class="card"></a>
                            <a href="/card/detail/clone"><img src="/img/card_ed/Clone.png" alt="Clone" class="card"></a>
                            <a href="/card/detail/tornado"><img src="/img/card_ed/Tornado.png" alt="Tornado" class="card"></a>
                            <a href="/card/detail/void"><img src="/img/card_ed/Void.png" alt="Void" class="card"></a>
                            <a href="/card/detail/baby-dragon"><img src="/img/card_ed/BabyD.png" alt="Baby Dragon" class="card"></a>
                            <a href="/card/detail/dark-prince"><img src="/img/card_ed/DarkPrince.png" alt="Dark Prince" class="card"></a>
                            <a href="/card/detail/freeze"><img src="/img/card_ed/Freeze.png" alt="Freeze" class="card"></a>
                            <a href="/card/detail/poison"><img src="/img/card_ed/Poison.png" alt="Poison" class="card"></a>
                            <a href="/card/detail/rune-giant"><img src="/img/card_ed/RuneGiant.png" alt="Rune Giant" class="card"></a>
                            <a href="/card/detail/hunter"><img src="/img/card_ed/Hunter.png" alt="Hunter" class="card"></a>
                            <a href="/card/detail/goblin-drill"><img src="/img/card_ed/GoblinDrill.png" alt="Goblin Drill" class="card"></a>
                            <a href="/card/detail/witch"><img src="/img/card_ed/Witch.png" alt="Witch" class="card"></a>
                            <a href="/card/detail/balloon"><img src="/img/card_ed/Balloon.png" alt="Balloon" class="card"></a>
                            <a href="/card/detail/prince"><img src="/img/card_ed/Prince.png" alt="Prince" class="card"></a>
                            <a href="/card/detail/electro-dragon"><img src="/img/card_ed/eDragon.png" alt="Electro Dragon" class="card"></a>
                            <a href="/card/detail/bowler"><img src="/img/card_ed/Bowler.png" alt="Bowler" class="card"></a>
                            <a href="/card/detail/executioner"><img src="/img/card_ed/Exe.png" alt="Executioner" class="card"></a>
                            <a href="/card/detail/cannon-cart"><img src="/img/card_ed/CannonCart.png" alt="Cannon Cart" class="card"></a>
                            <a href="/card/detail/giant-skeleton"><img src="/img/card_ed/GiantSkelly.png" alt="Giant Skeleton" class="card"></a>
                            <a href="/card/detail/lightning"><img src="/img/card_ed/Lightning.png" alt="Lightning" class="card"></a>
                            <a href="/card/detail/goblin-giant"><img src="/img/card_ed/GobGiant.png" alt="Goblin Giant" class="card"></a>
                            <a href="/card/detail/x-bow"><img src="/img/card_ed/XBow.png" alt="X-Bow" class="card"></a>
                            <a href="/card/detail/pekka"><img src="/img/card_ed/PEKKA.png" alt="P.E.K.K.A" class="card"></a>
                            <a href="/card/detail/electro-giant"><img src="/img/card_ed/ElectroGiant.png" alt="Electro Giant" class="card"></a>
                            <a href="/card/detail/golem"><img src="/img/card_ed/Golem.png" alt="Golem" class="card"></a>
                    </div>


                        <h4 class="text-yellow-400 mb-3">
                            Rare
                        </h4>

                    <div class="mb-4 flex flex-wrap items-center">
                            <a href="/card/detail/heal-spirit"><img src="/img/card_ed/HealSpirit.png" alt="Heal Spirit" class="card"></a>
                            <a href="/card/detail/ice-golem"><img src="/img/card_ed/IceGolem.png" alt="Ice Golem" class="card"></a>
                            <a href="/card/detail/suspicious-bush"><img src="/img/card_ed/SuspiciousBush.png" alt="Suspicious Bush" class="card"></a>
                            <a href="/card/detail/tombstone"><img src="/img/card_ed/Tombstone.png" alt="Tombstone" class="card"></a>
                            <a href="/card/detail/mega-minion"><img src="/img/card_ed/MM.png" alt="Mega Minion" class="card"></a>
                            <a href="/card/detail/dart-goblin"><img src="/img/card_ed/DartGob.png" alt="Dart Goblin" class="card"></a>
                            <a href="/card/detail/earthquake"><img src="/img/card_ed/Earthquake.png" alt="Earthquake" class="card"></a>
                            <a href="/card/detail/elixir-golem"><img src="/img/card_ed/ElixirGolem.png" alt="Elixir Golem" class="card"></a>
                            <a href="/card/detail/fireball"><img src="/img/card_ed/Fireball.png" alt="Fireball" class="card"></a>
                            <a href="/card/detail/mini-pekka"><img src="/img/card_ed/MP.png" alt="Mini P.E.K.K.A" class="card"></a>
                            <a href="/card/detail/musketeer"><img src="/img/card_ed/Musk.png" alt="Musketeer" class="card"></a>
                            <a href="/card/detail/goblin-cage"><img src="/img/card_ed/GoblinCage.png" alt="Goblin Cage" class="card"></a>
                            <a href="/card/detail/goblin-hut"><img src="/img/card_ed/GobHut.png" alt="Goblin Hut" class="card"></a>
                            <a href="/card/detail/valkyrie"><img src="/img/card_ed/Valk.png" alt="Valkyrie" class="card"></a>
                            <a href="/card/detail/battle-ram"><img src="/img/card_ed/Ram.png" alt="Battle Ram" class="card"></a>
                            <a href="/card/detail/bomb-tower"><img src="/img/card_ed/BombTower.png" alt="Bomb Tower" class="card"></a>
                            <a href="/card/detail/flying-machine"><img src="/img/card_ed/FlyingMachine.png" alt="Flying Machine" class="card"></a>
                            <a href="/card/detail/hog-rider"><img src="/img/card_ed/Hog.png" alt="Hog Rider" class="card"></a>
                            <a href="/card/detail/battle-healer"><img src="/img/card_ed/BattleHealer.png" alt="Battle Healer" class="card"></a>
                            <a href="/card/detail/furnace"><img src="/img/card_ed/Furnace.png" alt="Furnace" class="card"></a>
                            <a href="/card/detail/zappies"><img src="/img/card_ed/Zappies.png" alt="Zappies" class="card"></a>
                            <a href="/card/detail/goblin-demolisher"><img src="/img/card_ed/GoblinDemolisher.png" alt="Goblin Demolisher" class="card"></a>
                            <a href="/card/detail/giant"><img src="/img/card_ed/Giant.png" alt="Giant" class="card"></a>
                            <a href="/card/detail/inferno-tower"><img src="/img/card_ed/Inferno.png" alt="Inferno Tower" class="card"></a>
                            <a href="/card/detail/wizard"><img src="/img/card_ed/Wiz.png" alt="Wizard" class="card"></a>
                            <a href="/card/detail/royal-hogs"><img src="/img/card_ed/RoyalHogs.png" alt="Royal Hogs" class="card"></a>
                            <a href="/card/detail/rocket"><img src="/img/card_ed/Rocket.png" alt="Rocket" class="card"></a>
                            <a href="/card/detail/barbarian-hut"><img src="/img/card_ed/BarbHut.png" alt="Barbarian Hut" class="card"></a>
                            <a href="/card/detail/elixir-collector"><img src="/img/card_ed/Pump.png" alt="Elixir Collector" class="card"></a>
                            <a href="/card/detail/three-musketeers"><img src="/img/card_ed/3M.png" alt="Three Musketeers" class="card"></a>
                    </div>


                        <h4 class="text-teal-500 mb-3">
                            Common
                        </h4>

                    <div class="mb-4 flex flex-wrap items-center">
                            <a href="/card/detail/skeletons"><img src="/img/card_ed/Skellies.png" alt="Skeletons" class="card"></a>
                            <a href="/card/detail/electro-spirit"><img src="/img/card_ed/ElectroSpirit.png" alt="Electro Spirit" class="card"></a>
                            <a href="/card/detail/fire-spirit"><img src="/img/card_ed/FireSpirit.png" alt="Fire Spirit" class="card"></a>
                            <a href="/card/detail/ice-spirit"><img src="/img/card_ed/IceSpirit.png" alt="Ice Spirit" class="card"></a>
                            <a href="/card/detail/goblins"><img src="/img/card_ed/Gobs.png" alt="Goblins" class="card"></a>
                            <a href="/card/detail/spear-goblins"><img src="/img/card_ed/SpearGobs.png" alt="Spear Goblins" class="card"></a>
                            <a href="/card/detail/bomber"><img src="/img/card_ed/Bomber.png" alt="Bomber" class="card"></a>
                            <a href="/card/detail/bats"><img src="/img/card_ed/Bats.png" alt="Bats" class="card"></a>
                            <a href="/card/detail/zap"><img src="/img/card_ed/Zap.png" alt="Zap" class="card"></a>
                            <a href="/card/detail/giant-snowball"><img src="/img/card_ed/Snowball.png" alt="Giant Snowball" class="card"></a>
                            <a href="/card/detail/berserker"><img src="/img/card_ed/Berserker.png" alt="Berserker" class="card"></a>
                            <a href="/card/detail/archers"><img src="/img/card_ed/Archers.png" alt="Archers" class="card"></a>
                            <a href="/card/detail/arrows"><img src="/img/card_ed/Arrows.png" alt="Arrows" class="card"></a>
                            <a href="/card/detail/knight"><img src="/img/card_ed/Knight.png" alt="Knight" class="card"></a>
                            <a href="/card/detail/minions"><img src="/img/card_ed/Minions.png" alt="Minions" class="card"></a>
                            <a href="/card/detail/cannon"><img src="/img/card_ed/Cannon.png" alt="Cannon" class="card"></a>
                            <a href="/card/detail/goblin-gang"><img src="/img/card_ed/GobGang.png" alt="Goblin Gang" class="card"></a>
                            <a href="/card/detail/skeleton-barrel"><img src="/img/card_ed/SkellyBarrel.png" alt="Skeleton Barrel" class="card"></a>
                            <a href="/card/detail/firecracker"><img src="/img/card_ed/Firecracker.png" alt="Firecracker" class="card"></a>
                            <a href="/card/detail/royal-delivery"><img src="/img/card_ed/RoyalDelivery.png" alt="Royal Delivery" class="card"></a>
                            <a href="/card/detail/skeleton-dragons"><img src="/img/card_ed/SkeletonDragons.png" alt="Skeleton Dragons" class="card"></a>
                            <a href="/card/detail/mortar"><img src="/img/card_ed/Mortar.png" alt="Mortar" class="card"></a>
                            <a href="/card/detail/tesla"><img src="/img/card_ed/Tesla.png" alt="Tesla" class="card"></a>
                            <a href="/card/detail/barbarians"><img src="/img/card_ed/Barbs.png" alt="Barbarians" class="card"></a>
                            <a href="/card/detail/minion-horde"><img src="/img/card_ed/Horde.png" alt="Minion Horde" class="card"></a>
                            <a href="/card/detail/rascals"><img src="/img/card_ed/Rascals.png" alt="Rascals" class="card"></a>
                            <a href="/card/detail/royal-giant"><img src="/img/card_ed/RG.png" alt="Royal Giant" class="card"></a>
                            <a href="/card/detail/elite-barbarians"><img src="/img/card_ed/eBarbs.png" alt="Elite Barbarians" class="card"></a>
                            <a href="/card/detail/royal-recruits"><img src="/img/card_ed/RoyalRecruits.png" alt="Royal Recruits" class="card"></a>
                    </div>


            </section>
            <section class="">

                <h3 class="mb-4 mt-5 md:mt-0">By Elixir</h3>


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


            </section>
        </div>

    <div class="resource-container">


        <div id="resource-long-page-middle">
            <div align="center" data-freestar-ad="__240x400 __970x280" id="deckshop-pro_leaderboard_lpm" name="deckshop-pro_leaderboard_reusable" data-google-query-id="CMWI1smo340DFdZFHQkdRWgeVw">
                
            <div id="google_ads_iframe_/15184186,22289469413/7238_deckshop-pro_leaderboard_reusable_0__container__" style="border: 0pt none;"><iframe id="google_ads_iframe_/15184186,22289469413/7238_deckshop-pro_leaderboard_reusable_0" name="google_ads_iframe_/15184186,22289469413/7238_deckshop-pro_leaderboard_reusable_0" title="3rd party ad content" width="1" height="1" scrolling="no" marginwidth="0" marginheight="0" frameborder="0" aria-label="Advertisement" tabindex="0" allow="private-state-token-redemption;attribution-reporting" style="border: 0px; vertical-align: bottom; width: 728px; height: 90px;" data-google-container-id="5" data-load-complete="true"></iframe></div></div>
        </div>










<div class="friendlyReminder w-full bg-gray-darker border border-gray-dark rounded py-2 px-4" style="display: none;">
    <p class="text-gray-muted">
        Did you know?
    </p>
    <p class="mb-1">
        Deck Shop has lots of visitors, and servers cost money each month.
    </p>
</div>

    </div>

    <div class="grid md:grid-cols-2 gap-5" id="byType">
        <section class="">
            <h3 class="mb-3">Spells</h3>

            <div class="mb-4 flex flex-wrap items-center">
                <a href="/card/detail/zap"><img src="/img/card_ed/Zap.png" alt="Zap" class="card"></a>
                <a href="/card/detail/giant-snowball"><img src="/img/card_ed/Snowball.png" alt="Giant Snowball" class="card"></a>
                <a href="/card/detail/arrows"><img src="/img/card_ed/Arrows.png" alt="Arrows" class="card"></a>
                <a href="/card/detail/royal-delivery"><img src="/img/card_ed/RoyalDelivery.png" alt="Royal Delivery" class="card"></a>
                <a href="/card/detail/earthquake"><img src="/img/card_ed/Earthquake.png" alt="Earthquake" class="card"></a>
                <a href="/card/detail/fireball"><img src="/img/card_ed/Fireball.png" alt="Fireball" class="card"></a>
                <a href="/card/detail/rocket"><img src="/img/card_ed/Rocket.png" alt="Rocket" class="card"></a>
                <a href="/card/detail/mirror"><img src="/img/card_ed/Mirror.png" alt="Mirror" class="card"></a>
                <a href="/card/detail/barbarian-barrel"><img src="/img/card_ed/BarbBarrel.png" alt="Barbarian Barrel" class="card"></a>
                <a href="/card/detail/goblin-curse"><img src="/img/card_ed/GoblinCurse.png" alt="Goblin Curse" class="card"></a>
                <a href="/card/detail/rage"><img src="/img/card_ed/Rage.png" alt="Rage" class="card"></a>
                <a href="/card/detail/goblin-barrel"><img src="/img/card_ed/Barrel.png" alt="Goblin Barrel" class="card"></a>
                <a href="/card/detail/clone"><img src="/img/card_ed/Clone.png" alt="Clone" class="card"></a>
                <a href="/card/detail/tornado"><img src="/img/card_ed/Tornado.png" alt="Tornado" class="card"></a>
                <a href="/card/detail/void"><img src="/img/card_ed/Void.png" alt="Void" class="card"></a>
                <a href="/card/detail/freeze"><img src="/img/card_ed/Freeze.png" alt="Freeze" class="card"></a>
                <a href="/card/detail/poison"><img src="/img/card_ed/Poison.png" alt="Poison" class="card"></a>
                <a href="/card/detail/lightning"><img src="/img/card_ed/Lightning.png" alt="Lightning" class="card"></a>
                <a href="/card/detail/the-log"><img src="/img/card_ed/Log.png" alt="The Log" class="card"></a>
                <a href="/card/detail/graveyard"><img src="/img/card_ed/Graveyard.png" alt="Graveyard" class="card"></a>
            </div>

            <h3 class="mb-3 mt-5">Direct damage</h3>

            <div class="mb-4 flex flex-wrap items-center">
                    <a href="/card/detail/zap"><img src="/img/card_ed/Zap.png" alt="Zap" class="card"></a>
                    <a href="/card/detail/giant-snowball"><img src="/img/card_ed/Snowball.png" alt="Giant Snowball" class="card"></a>
                    <a href="/card/detail/arrows"><img src="/img/card_ed/Arrows.png" alt="Arrows" class="card"></a>
                    <a href="/card/detail/royal-delivery"><img src="/img/card_ed/RoyalDelivery.png" alt="Royal Delivery" class="card"></a>
                    <a href="/card/detail/earthquake"><img src="/img/card_ed/Earthquake.png" alt="Earthquake" class="card"></a>
                    <a href="/card/detail/fireball"><img src="/img/card_ed/Fireball.png" alt="Fireball" class="card"></a>
                    <a href="/card/detail/rocket"><img src="/img/card_ed/Rocket.png" alt="Rocket" class="card"></a>
                    <a href="/card/detail/barbarian-barrel"><img src="/img/card_ed/BarbBarrel.png" alt="Barbarian Barrel" class="card"></a>
                    <a href="/card/detail/goblin-curse"><img src="/img/card_ed/GoblinCurse.png" alt="Goblin Curse" class="card"></a>
                    <a href="/card/detail/rage"><img src="/img/card_ed/Rage.png" alt="Rage" class="card"></a>
                    <a href="/card/detail/tornado"><img src="/img/card_ed/Tornado.png" alt="Tornado" class="card"></a>
                    <a href="/card/detail/void"><img src="/img/card_ed/Void.png" alt="Void" class="card"></a>
                    <a href="/card/detail/freeze"><img src="/img/card_ed/Freeze.png" alt="Freeze" class="card"></a>
                    <a href="/card/detail/poison"><img src="/img/card_ed/Poison.png" alt="Poison" class="card"></a>
                    <a href="/card/detail/lightning"><img src="/img/card_ed/Lightning.png" alt="Lightning" class="card"></a>
                    <a href="/card/detail/the-log"><img src="/img/card_ed/Log.png" alt="The Log" class="card"></a>
            </div>

            <h3 class="mb-3 mt-5">Buildings</h3>

            <div class="mb-4 flex flex-wrap items-center">
                <a href="/card/detail/cannon"><img src="/img/card_ed/Cannon.png" alt="Cannon" class="card"></a>
                <a href="/card/detail/mortar"><img src="/img/card_ed/Mortar.png" alt="Mortar" class="card"></a>
                <a href="/card/detail/tesla"><img src="/img/card_ed/Tesla.png" alt="Tesla" class="card"></a>
                <a href="/card/detail/tombstone"><img src="/img/card_ed/Tombstone.png" alt="Tombstone" class="card"></a>
                <a href="/card/detail/goblin-cage"><img src="/img/card_ed/GoblinCage.png" alt="Goblin Cage" class="card"></a>
                <a href="/card/detail/goblin-hut"><img src="/img/card_ed/GobHut.png" alt="Goblin Hut" class="card"></a>
                <a href="/card/detail/bomb-tower"><img src="/img/card_ed/BombTower.png" alt="Bomb Tower" class="card"></a>
                <a href="/card/detail/furnace"><img src="/img/card_ed/Furnace.png" alt="Furnace" class="card"></a>
                <a href="/card/detail/inferno-tower"><img src="/img/card_ed/Inferno.png" alt="Inferno Tower" class="card"></a>
                <a href="/card/detail/barbarian-hut"><img src="/img/card_ed/BarbHut.png" alt="Barbarian Hut" class="card"></a>
                <a href="/card/detail/elixir-collector"><img src="/img/card_ed/Pump.png" alt="Elixir Collector" class="card"></a>
                <a href="/card/detail/goblin-drill"><img src="/img/card_ed/GoblinDrill.png" alt="Goblin Drill" class="card"></a>
                <a href="/card/detail/x-bow"><img src="/img/card_ed/XBow.png" alt="X-Bow" class="card"></a>
            </div>

            <h3 class="mb-3 mt-5">Defensive towers</h3>

            <div class="mb-4 flex flex-wrap items-center">
                    <a href="/card/detail/cannon"><img src="/img/card_ed/Cannon.png" alt="Cannon" class="card"></a>
                    <a href="/card/detail/tesla"><img src="/img/card_ed/Tesla.png" alt="Tesla" class="card"></a>
                    <a href="/card/detail/bomb-tower"><img src="/img/card_ed/BombTower.png" alt="Bomb Tower" class="card"></a>
                    <a href="/card/detail/inferno-tower"><img src="/img/card_ed/Inferno.png" alt="Inferno Tower" class="card"></a>
            </div>

            <h3 class="mb-3 mt-5">Siege buildings</h3>

            <div class="mb-4 flex flex-wrap items-center">
                    <a href="/card/detail/mortar"><img src="/img/card_ed/Mortar.png" alt="Mortar" class="card"></a>
                    <a href="/card/detail/x-bow"><img src="/img/card_ed/XBow.png" alt="X-Bow" class="card"></a>
            </div>

            <h3 class="mb-3 mt-5">Spawners</h3>

            <div class="mb-4 flex flex-wrap items-center">
                <a href="/card/detail/tombstone"><img src="/img/card_ed/Tombstone.png" alt="Tombstone" class="card"></a>
                <a href="/card/detail/goblin-hut"><img src="/img/card_ed/GobHut.png" alt="Goblin Hut" class="card"></a>
                <a href="/card/detail/furnace"><img src="/img/card_ed/Furnace.png" alt="Furnace" class="card"></a>
                <a href="/card/detail/barbarian-hut"><img src="/img/card_ed/BarbHut.png" alt="Barbarian Hut" class="card"></a>
                <a href="/card/detail/goblin-drill"><img src="/img/card_ed/GoblinDrill.png" alt="Goblin Drill" class="card"></a>
            </div>
        </section>
        <section class="">

            <h3 class="mb-3 mt-5 md:mt-0">Melee</h3>

            <p class="text-gray-muted text-responsive-lead mb-1">Melee: Short</p>
            <div class="mb-4 flex flex-wrap items-center">
                <a href="/card/detail/skeletons"><img src="/img/card_ed/Skellies.png" alt="Skeletons" class="card"></a>
                <a href="/card/detail/goblins"><img src="/img/card_ed/Gobs.png" alt="Goblins" class="card"></a>
                <a href="/card/detail/berserker"><img src="/img/card_ed/Berserker.png" alt="Berserker" class="card"></a>
                <a href="/card/detail/goblin-gang"><img src="/img/card_ed/GobGang.png" alt="Goblin Gang" class="card"></a>
                <a href="/card/detail/barbarians"><img src="/img/card_ed/Barbs.png" alt="Barbarians" class="card"></a>
                <a href="/card/detail/rascals"><img src="/img/card_ed/Rascals.png" alt="Rascals" class="card"></a>
                <a href="/card/detail/elixir-golem"><img src="/img/card_ed/ElixirGolem.png" alt="Elixir Golem" class="card"></a>
                <a href="/card/detail/mini-pekka"><img src="/img/card_ed/MP.png" alt="Mini P.E.K.K.A" class="card"></a>
                <a href="/card/detail/goblin-cage"><img src="/img/card_ed/GoblinCage.png" alt="Goblin Cage" class="card"></a>
                <a href="/card/detail/barbarian-barrel"><img src="/img/card_ed/BarbBarrel.png" alt="Barbarian Barrel" class="card"></a>
                <a href="/card/detail/goblin-barrel"><img src="/img/card_ed/Barrel.png" alt="Goblin Barrel" class="card"></a>
                <a href="/card/detail/skeleton-army"><img src="/img/card_ed/Skarmy.png" alt="Skeleton Army" class="card"></a>
                <a href="/card/detail/giant-skeleton"><img src="/img/card_ed/GiantSkelly.png" alt="Giant Skeleton" class="card"></a>
                <a href="/card/detail/bandit"><img src="/img/card_ed/Bandit.png" alt="Bandit" class="card"></a>
                <a href="/card/detail/lumberjack"><img src="/img/card_ed/Lumber.png" alt="Lumberjack" class="card"></a>
                <a href="/card/detail/graveyard"><img src="/img/card_ed/Graveyard.png" alt="Graveyard" class="card"></a>
                <a href="/card/detail/boss-bandit"><img src="/img/card_ed/BossBandit.png" alt="Boss Bandit" class="card"></a>
            </div>
            <p class="text-gray-muted text-responsive-lead mb-1">Melee: Medium</p>
            <div class="mb-4 flex flex-wrap items-center">
                <a href="/card/detail/bats"><img src="/img/card_ed/Bats.png" alt="Bats" class="card"></a>
                <a href="/card/detail/knight"><img src="/img/card_ed/Knight.png" alt="Knight" class="card"></a>
                <a href="/card/detail/elite-barbarians"><img src="/img/card_ed/eBarbs.png" alt="Elite Barbarians" class="card"></a>
                <a href="/card/detail/valkyrie"><img src="/img/card_ed/Valk.png" alt="Valkyrie" class="card"></a>
                <a href="/card/detail/dark-prince"><img src="/img/card_ed/DarkPrince.png" alt="Dark Prince" class="card"></a>
                <a href="/card/detail/rune-giant"><img src="/img/card_ed/RuneGiant.png" alt="Rune Giant" class="card"></a>
                <a href="/card/detail/goblin-giant"><img src="/img/card_ed/GobGiant.png" alt="Goblin Giant" class="card"></a>
                <a href="/card/detail/pekka"><img src="/img/card_ed/PEKKA.png" alt="P.E.K.K.A" class="card"></a>
                <a href="/card/detail/electro-giant"><img src="/img/card_ed/ElectroGiant.png" alt="Electro Giant" class="card"></a>
                <a href="/card/detail/miner"><img src="/img/card_ed/Miner.png" alt="Miner" class="card"></a>
                <a href="/card/detail/royal-ghost"><img src="/img/card_ed/Ghost.png" alt="Royal Ghost" class="card"></a>
                <a href="/card/detail/fisherman"><img src="/img/card_ed/Fisherman.png" alt="Fisherman" class="card"></a>
                <a href="/card/detail/goblin-machine"><img src="/img/card_ed/GoblinMachine.png" alt="Goblin Machine" class="card"></a>
                <a href="/card/detail/mega-knight"><img src="/img/card_ed/MegaKnight.png" alt="Mega Knight" class="card"></a>
                <a href="/card/detail/golden-knight"><img src="/img/card_ed/GoldenKnight.png" alt="Golden Knight" class="card"></a>
                <a href="/card/detail/skeleton-king"><img src="/img/card_ed/SkeletonKing.png" alt="Skeleton King" class="card"></a>
                <a href="/card/detail/goblinstein"><img src="/img/card_ed/Goblinstein.png" alt="Goblinstein" class="card"></a>
                <a href="/card/detail/monk"><img src="/img/card_ed/Monk.png" alt="Monk" class="card"></a>
            </div>
            <p class="text-gray-muted text-responsive-lead mb-1">Melee: Long</p>
            <div class="mb-4 flex flex-wrap items-center">
                <a href="/card/detail/minions"><img src="/img/card_ed/Minions.png" alt="Minions" class="card"></a>
                <a href="/card/detail/royal-delivery"><img src="/img/card_ed/RoyalDelivery.png" alt="Royal Delivery" class="card"></a>
                <a href="/card/detail/minion-horde"><img src="/img/card_ed/Horde.png" alt="Minion Horde" class="card"></a>
                <a href="/card/detail/royal-recruits"><img src="/img/card_ed/RoyalRecruits.png" alt="Royal Recruits" class="card"></a>
                <a href="/card/detail/mega-minion"><img src="/img/card_ed/MM.png" alt="Mega Minion" class="card"></a>
                <a href="/card/detail/battle-healer"><img src="/img/card_ed/BattleHealer.png" alt="Battle Healer" class="card"></a>
                <a href="/card/detail/guards"><img src="/img/card_ed/Guards.png" alt="Guards" class="card"></a>
                <a href="/card/detail/prince"><img src="/img/card_ed/Prince.png" alt="Prince" class="card"></a>
                <a href="/card/detail/phoenix"><img src="/img/card_ed/Phoenix.png" alt="Phoenix" class="card"></a>
                <a href="/card/detail/night-witch"><img src="/img/card_ed/NightWitch.png" alt="Night Witch" class="card"></a>
                <a href="/card/detail/mighty-miner"><img src="/img/card_ed/MightyMiner.png" alt="Mighty Miner" class="card"></a>
            </div>

            <h3 class="mb-3 mt-5">Ranged</h3>

            <div class="mb-4 flex flex-wrap items-center">
                <a href="/card/detail/spear-goblins"><img src="/img/card_ed/SpearGobs.png" alt="Spear Goblins" class="card"></a>
                <a href="/card/detail/bomber"><img src="/img/card_ed/Bomber.png" alt="Bomber" class="card"></a>
                <a href="/card/detail/archers"><img src="/img/card_ed/Archers.png" alt="Archers" class="card"></a>
                <a href="/card/detail/cannon"><img src="/img/card_ed/Cannon.png" alt="Cannon" class="card"></a>
                <a href="/card/detail/goblin-gang"><img src="/img/card_ed/GobGang.png" alt="Goblin Gang" class="card"></a>
                <a href="/card/detail/firecracker"><img src="/img/card_ed/Firecracker.png" alt="Firecracker" class="card"></a>
                <a href="/card/detail/skeleton-dragons"><img src="/img/card_ed/SkeletonDragons.png" alt="Skeleton Dragons" class="card"></a>
                <a href="/card/detail/rascals"><img src="/img/card_ed/Rascals.png" alt="Rascals" class="card"></a>
                <a href="/card/detail/dart-goblin"><img src="/img/card_ed/DartGob.png" alt="Dart Goblin" class="card"></a>
                <a href="/card/detail/musketeer"><img src="/img/card_ed/Musk.png" alt="Musketeer" class="card"></a>
                <a href="/card/detail/goblin-hut"><img src="/img/card_ed/GobHut.png" alt="Goblin Hut" class="card"></a>
                <a href="/card/detail/flying-machine"><img src="/img/card_ed/FlyingMachine.png" alt="Flying Machine" class="card"></a>
                <a href="/card/detail/zappies"><img src="/img/card_ed/Zappies.png" alt="Zappies" class="card"></a>
                <a href="/card/detail/goblin-demolisher"><img src="/img/card_ed/GoblinDemolisher.png" alt="Goblin Demolisher" class="card"></a>
                <a href="/card/detail/wizard"><img src="/img/card_ed/Wiz.png" alt="Wizard" class="card"></a>
                <a href="/card/detail/three-musketeers"><img src="/img/card_ed/3M.png" alt="Three Musketeers" class="card"></a>
                <a href="/card/detail/baby-dragon"><img src="/img/card_ed/BabyD.png" alt="Baby Dragon" class="card"></a>
                <a href="/card/detail/hunter"><img src="/img/card_ed/Hunter.png" alt="Hunter" class="card"></a>
                <a href="/card/detail/witch"><img src="/img/card_ed/Witch.png" alt="Witch" class="card"></a>
                <a href="/card/detail/electro-dragon"><img src="/img/card_ed/eDragon.png" alt="Electro Dragon" class="card"></a>
                <a href="/card/detail/bowler"><img src="/img/card_ed/Bowler.png" alt="Bowler" class="card"></a>
                <a href="/card/detail/executioner"><img src="/img/card_ed/Exe.png" alt="Executioner" class="card"></a>
                <a href="/card/detail/cannon-cart"><img src="/img/card_ed/CannonCart.png" alt="Cannon Cart" class="card"></a>
                <a href="/card/detail/goblin-giant"><img src="/img/card_ed/GobGiant.png" alt="Goblin Giant" class="card"></a>
                <a href="/card/detail/x-bow"><img src="/img/card_ed/XBow.png" alt="X-Bow" class="card"></a>
                <a href="/card/detail/princess"><img src="/img/card_ed/Princess.png" alt="Princess" class="card"></a>
                <a href="/card/detail/ice-wizard"><img src="/img/card_ed/IceWiz.png" alt="Ice Wizard" class="card"></a>
                <a href="/card/detail/fisherman"><img src="/img/card_ed/Fisherman.png" alt="Fisherman" class="card"></a>
                <a href="/card/detail/electro-wizard"><img src="/img/card_ed/eWiz.png" alt="Electro Wizard" class="card"></a>
                <a href="/card/detail/inferno-dragon"><img src="/img/card_ed/InfernoD.png" alt="Inferno Dragon" class="card"></a>
                <a href="/card/detail/magic-archer"><img src="/img/card_ed/MagicArcher.png" alt="Magic Archer" class="card"></a>
                <a href="/card/detail/mother-witch"><img src="/img/card_ed/MotherWitch.png" alt="Mother Witch" class="card"></a>
                <a href="/card/detail/ram-rider"><img src="/img/card_ed/RamRider.png" alt="Ram Rider" class="card"></a>
                <a href="/card/detail/sparky"><img src="/img/card_ed/Sparky.png" alt="Sparky" class="card"></a>
                <a href="/card/detail/little-prince"><img src="/img/card_ed/LittlePrince.png" alt="Little Prince" class="card"></a>
                <a href="/card/detail/archer-queen"><img src="/img/card_ed/ArcherQueen.png" alt="Archer Queen" class="card"></a>
                <a href="/card/detail/goblinstein"><img src="/img/card_ed/Goblinstein.png" alt="Goblinstein" class="card"></a>
            </div>

            <h3 class="mb-3 mt-5">Air units</h3>

            <div class="mb-4 flex flex-wrap items-center">
                    <a href="/card/detail/bats"><img src="/img/card_ed/Bats.png" alt="Bats" class="card"></a>
                    <a href="/card/detail/minions"><img src="/img/card_ed/Minions.png" alt="Minions" class="card"></a>
                    <a href="/card/detail/skeleton-barrel"><img src="/img/card_ed/SkellyBarrel.png" alt="Skeleton Barrel" class="card"></a>
                    <a href="/card/detail/skeleton-dragons"><img src="/img/card_ed/SkeletonDragons.png" alt="Skeleton Dragons" class="card"></a>
                    <a href="/card/detail/minion-horde"><img src="/img/card_ed/Horde.png" alt="Minion Horde" class="card"></a>
                    <a href="/card/detail/mega-minion"><img src="/img/card_ed/MM.png" alt="Mega Minion" class="card"></a>
                    <a href="/card/detail/flying-machine"><img src="/img/card_ed/FlyingMachine.png" alt="Flying Machine" class="card"></a>
                    <a href="/card/detail/baby-dragon"><img src="/img/card_ed/BabyD.png" alt="Baby Dragon" class="card"></a>
                    <a href="/card/detail/balloon"><img src="/img/card_ed/Balloon.png" alt="Balloon" class="card"></a>
                    <a href="/card/detail/electro-dragon"><img src="/img/card_ed/eDragon.png" alt="Electro Dragon" class="card"></a>
                    <a href="/card/detail/inferno-dragon"><img src="/img/card_ed/InfernoD.png" alt="Inferno Dragon" class="card"></a>
                    <a href="/card/detail/phoenix"><img src="/img/card_ed/Phoenix.png" alt="Phoenix" class="card"></a>
                    <a href="/card/detail/lava-hound"><img src="/img/card_ed/Lava.png" alt="Lava Hound" class="card"></a>
            </div>


            <h3 class="mb-3 mt-5">Ground units</h3>

            <div class="mb-4 flex flex-wrap items-center">
                    <a href="/card/detail/skeletons"><img src="/img/card_ed/Skellies.png" alt="Skeletons" class="card"></a>
                    <a href="/card/detail/electro-spirit"><img src="/img/card_ed/ElectroSpirit.png" alt="Electro Spirit" class="card"></a>
                    <a href="/card/detail/fire-spirit"><img src="/img/card_ed/FireSpirit.png" alt="Fire Spirit" class="card"></a>
                    <a href="/card/detail/ice-spirit"><img src="/img/card_ed/IceSpirit.png" alt="Ice Spirit" class="card"></a>
                    <a href="/card/detail/goblins"><img src="/img/card_ed/Gobs.png" alt="Goblins" class="card"></a>
                    <a href="/card/detail/spear-goblins"><img src="/img/card_ed/SpearGobs.png" alt="Spear Goblins" class="card"></a>
                    <a href="/card/detail/bomber"><img src="/img/card_ed/Bomber.png" alt="Bomber" class="card"></a>
                    <a href="/card/detail/berserker"><img src="/img/card_ed/Berserker.png" alt="Berserker" class="card"></a>
                    <a href="/card/detail/archers"><img src="/img/card_ed/Archers.png" alt="Archers" class="card"></a>
                    <a href="/card/detail/knight"><img src="/img/card_ed/Knight.png" alt="Knight" class="card"></a>
                    <a href="/card/detail/goblin-gang"><img src="/img/card_ed/GobGang.png" alt="Goblin Gang" class="card"></a>
                    <a href="/card/detail/firecracker"><img src="/img/card_ed/Firecracker.png" alt="Firecracker" class="card"></a>
                    <a href="/card/detail/royal-delivery"><img src="/img/card_ed/RoyalDelivery.png" alt="Royal Delivery" class="card"></a>
                    <a href="/card/detail/barbarians"><img src="/img/card_ed/Barbs.png" alt="Barbarians" class="card"></a>
                    <a href="/card/detail/rascals"><img src="/img/card_ed/Rascals.png" alt="Rascals" class="card"></a>
                    <a href="/card/detail/royal-giant"><img src="/img/card_ed/RG.png" alt="Royal Giant" class="card"></a>
                    <a href="/card/detail/elite-barbarians"><img src="/img/card_ed/eBarbs.png" alt="Elite Barbarians" class="card"></a>
                    <a href="/card/detail/royal-recruits"><img src="/img/card_ed/RoyalRecruits.png" alt="Royal Recruits" class="card"></a>
                    <a href="/card/detail/heal-spirit"><img src="/img/card_ed/HealSpirit.png" alt="Heal Spirit" class="card"></a>
                    <a href="/card/detail/ice-golem"><img src="/img/card_ed/IceGolem.png" alt="Ice Golem" class="card"></a>
                    <a href="/card/detail/suspicious-bush"><img src="/img/card_ed/SuspiciousBush.png" alt="Suspicious Bush" class="card"></a>
                    <a href="/card/detail/dart-goblin"><img src="/img/card_ed/DartGob.png" alt="Dart Goblin" class="card"></a>
                    <a href="/card/detail/elixir-golem"><img src="/img/card_ed/ElixirGolem.png" alt="Elixir Golem" class="card"></a>
                    <a href="/card/detail/mini-pekka"><img src="/img/card_ed/MP.png" alt="Mini P.E.K.K.A" class="card"></a>
                    <a href="/card/detail/musketeer"><img src="/img/card_ed/Musk.png" alt="Musketeer" class="card"></a>
                    <a href="/card/detail/goblin-cage"><img src="/img/card_ed/GoblinCage.png" alt="Goblin Cage" class="card"></a>
                    <a href="/card/detail/valkyrie"><img src="/img/card_ed/Valk.png" alt="Valkyrie" class="card"></a>
                    <a href="/card/detail/battle-ram"><img src="/img/card_ed/Ram.png" alt="Battle Ram" class="card"></a>
                    <a href="/card/detail/hog-rider"><img src="/img/card_ed/Hog.png" alt="Hog Rider" class="card"></a>
                    <a href="/card/detail/battle-healer"><img src="/img/card_ed/BattleHealer.png" alt="Battle Healer" class="card"></a>
                    <a href="/card/detail/zappies"><img src="/img/card_ed/Zappies.png" alt="Zappies" class="card"></a>
                    <a href="/card/detail/goblin-demolisher"><img src="/img/card_ed/GoblinDemolisher.png" alt="Goblin Demolisher" class="card"></a>
                    <a href="/card/detail/giant"><img src="/img/card_ed/Giant.png" alt="Giant" class="card"></a>
                    <a href="/card/detail/wizard"><img src="/img/card_ed/Wiz.png" alt="Wizard" class="card"></a>
                    <a href="/card/detail/royal-hogs"><img src="/img/card_ed/RoyalHogs.png" alt="Royal Hogs" class="card"></a>
                    <a href="/card/detail/three-musketeers"><img src="/img/card_ed/3M.png" alt="Three Musketeers" class="card"></a>
                    <a href="/card/detail/barbarian-barrel"><img src="/img/card_ed/BarbBarrel.png" alt="Barbarian Barrel" class="card"></a>
                    <a href="/card/detail/wall-breakers"><img src="/img/card_ed/WallBreakers.png" alt="Wall Breakers" class="card"></a>
                    <a href="/card/detail/goblin-barrel"><img src="/img/card_ed/Barrel.png" alt="Goblin Barrel" class="card"></a>
                    <a href="/card/detail/guards"><img src="/img/card_ed/Guards.png" alt="Guards" class="card"></a>
                    <a href="/card/detail/skeleton-army"><img src="/img/card_ed/Skarmy.png" alt="Skeleton Army" class="card"></a>
                    <a href="/card/detail/dark-prince"><img src="/img/card_ed/DarkPrince.png" alt="Dark Prince" class="card"></a>
                    <a href="/card/detail/rune-giant"><img src="/img/card_ed/RuneGiant.png" alt="Rune Giant" class="card"></a>
                    <a href="/card/detail/hunter"><img src="/img/card_ed/Hunter.png" alt="Hunter" class="card"></a>
                    <a href="/card/detail/witch"><img src="/img/card_ed/Witch.png" alt="Witch" class="card"></a>
                    <a href="/card/detail/prince"><img src="/img/card_ed/Prince.png" alt="Prince" class="card"></a>
                    <a href="/card/detail/bowler"><img src="/img/card_ed/Bowler.png" alt="Bowler" class="card"></a>
                    <a href="/card/detail/executioner"><img src="/img/card_ed/Exe.png" alt="Executioner" class="card"></a>
                    <a href="/card/detail/cannon-cart"><img src="/img/card_ed/CannonCart.png" alt="Cannon Cart" class="card"></a>
                    <a href="/card/detail/giant-skeleton"><img src="/img/card_ed/GiantSkelly.png" alt="Giant Skeleton" class="card"></a>
                    <a href="/card/detail/goblin-giant"><img src="/img/card_ed/GobGiant.png" alt="Goblin Giant" class="card"></a>
                    <a href="/card/detail/pekka"><img src="/img/card_ed/PEKKA.png" alt="P.E.K.K.A" class="card"></a>
                    <a href="/card/detail/electro-giant"><img src="/img/card_ed/ElectroGiant.png" alt="Electro Giant" class="card"></a>
                    <a href="/card/detail/golem"><img src="/img/card_ed/Golem.png" alt="Golem" class="card"></a>
                    <a href="/card/detail/miner"><img src="/img/card_ed/Miner.png" alt="Miner" class="card"></a>
                    <a href="/card/detail/princess"><img src="/img/card_ed/Princess.png" alt="Princess" class="card"></a>
                    <a href="/card/detail/ice-wizard"><img src="/img/card_ed/IceWiz.png" alt="Ice Wizard" class="card"></a>
                    <a href="/card/detail/royal-ghost"><img src="/img/card_ed/Ghost.png" alt="Royal Ghost" class="card"></a>
                    <a href="/card/detail/bandit"><img src="/img/card_ed/Bandit.png" alt="Bandit" class="card"></a>
                    <a href="/card/detail/fisherman"><img src="/img/card_ed/Fisherman.png" alt="Fisherman" class="card"></a>
                    <a href="/card/detail/electro-wizard"><img src="/img/card_ed/eWiz.png" alt="Electro Wizard" class="card"></a>
                    <a href="/card/detail/magic-archer"><img src="/img/card_ed/MagicArcher.png" alt="Magic Archer" class="card"></a>
                    <a href="/card/detail/lumberjack"><img src="/img/card_ed/Lumber.png" alt="Lumberjack" class="card"></a>
                    <a href="/card/detail/night-witch"><img src="/img/card_ed/NightWitch.png" alt="Night Witch" class="card"></a>
                    <a href="/card/detail/mother-witch"><img src="/img/card_ed/MotherWitch.png" alt="Mother Witch" class="card"></a>
                    <a href="/card/detail/ram-rider"><img src="/img/card_ed/RamRider.png" alt="Ram Rider" class="card"></a>
                    <a href="/card/detail/goblin-machine"><img src="/img/card_ed/GoblinMachine.png" alt="Goblin Machine" class="card"></a>
                    <a href="/card/detail/sparky"><img src="/img/card_ed/Sparky.png" alt="Sparky" class="card"></a>
                    <a href="/card/detail/mega-knight"><img src="/img/card_ed/MegaKnight.png" alt="Mega Knight" class="card"></a>
                    <a href="/card/detail/little-prince"><img src="/img/card_ed/LittlePrince.png" alt="Little Prince" class="card"></a>
                    <a href="/card/detail/golden-knight"><img src="/img/card_ed/GoldenKnight.png" alt="Golden Knight" class="card"></a>
                    <a href="/card/detail/skeleton-king"><img src="/img/card_ed/SkeletonKing.png" alt="Skeleton King" class="card"></a>
                    <a href="/card/detail/mighty-miner"><img src="/img/card_ed/MightyMiner.png" alt="Mighty Miner" class="card"></a>
                    <a href="/card/detail/archer-queen"><img src="/img/card_ed/ArcherQueen.png" alt="Archer Queen" class="card"></a>
                    <a href="/card/detail/goblinstein"><img src="/img/card_ed/Goblinstein.png" alt="Goblinstein" class="card"></a>
                    <a href="/card/detail/monk"><img src="/img/card_ed/Monk.png" alt="Monk" class="card"></a>
                    <a href="/card/detail/boss-bandit"><img src="/img/card_ed/BossBandit.png" alt="Boss Bandit" class="card"></a>
            </div>


        </section>
    </div>


</article>


    </main>
"""


def extract_categories_and_cards(html):
    # This pattern finds h3 or h4 headings and the following div with class "mb-4 flex flex-wrap items-center"
    pattern = re.compile(
        r'<(h3|h4)\b[^>]*>([^<]*)</\1>\s*<div\b[^>]*class="[^"]*mb-4 flex flex-wrap items-center[^"]*"[^>]*?>(.*?)</div>',
        re.DOTALL,
    )
    categories = {}
    for match in pattern.finditer(html):
        category_name = match.group(2).strip()
        div_content = match.group(3)
        alt_texts = re.findall(r'alt="([^"]+)"', div_content)
        categories[category_name] = alt_texts
    return categories


# Extract categories and their cards from HTML
categories_dict = extract_categories_and_cards(html_content)

# Process each category: convert to the matching card name from original_list
category_arrays = {}
for category, cards in categories_dict.items():
    matched_cards = []
    for card in cards:
        closest_match = find_closest_match(card, original_list)
        if closest_match:
            matched_cards.append(closest_match)
    category_arrays[category] = matched_cards

# Print the arrays for each category
for category, cards in category_arrays.items():
    print(f"Category '{category}': {cards}")
    print(f"Count: {len(cards)}")
    print()

# Total cards in the original list
print(f"Total cards in original list: {len(original_list)}")

# Count and display unmatched cards
matched_set = set()
for cards in category_arrays.values():
    matched_set.update(cards)
matched_count = len(matched_set)
print(f"Total matched cards: {matched_count}")

not_matched = len(original_list) - matched_count
unmatched_cards = [card for card in original_list if card not in matched_set]
print(f"Total not matched cards: {not_matched}")
print(f"Unmatched cards: {unmatched_cards}")
