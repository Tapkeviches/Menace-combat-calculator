This is a tool i made in python to research and deconstruct combat balance in game Menace. It simulates weapons, enemies and then do thousand of shots following ingame rules and formulas. 

To comfortable use it you need to make a copy of this [google sheet file](https://docs.google.com/spreadsheets/d/1fyP3SBn8bYCf5fCMowssKIniw3MKLj7Fy-w3AKteH_A/edit?gid=599662166#gid=599662166). 
Then install [gspread module](https://docs.gspread.org/en/latest/), and setup it with [google cloud authentification](https://docs.gspread.org/en/latest/oauth2.html) of your choosing. Gspread documentation
has and extensive guide on how to do it. Add your copy of google sheet to server_creds file in the root folder. Script launches from ExperimentDataProcessor file. 

**As for google sheet file. It has several lists:**
- **EnemyStats** - contains stats of ingame enemies from wiki or ingame files.

- **WeaponStats** - contains info about weapons player can use in game

- **Experiment config** - file where you setup which experiment to run.
  -**Experiment ID** - unique experiment Id. I use naming convension for Ids. It starts with name of the weapon, then name of a target, then player squad size, squad leader accuracy and size of cover.
  - WeaponKey - choose weapon you want your squad to use\
  - EnemySquadKey - choose squad to shoot at
  - PlayerSquadSuze - set the size of your squad. For special weapon set it to "1" since only one person in squad can carry a special weapon.
  - SquadLeaderAcc - accuracy of your squad
  - Target cover - choose what cover enemy will use when calculating combat.
  - Iterations - since game has alot of random elements, i decided to just brut force this random shenanigans. If you run experiment enough times, then random will become less of a factor and you get average results
    on 10000 iterations i get spread arond +-0.05 for average damage\supression on so on. Good enough i think. Dont launch alot of experiments with dozen of itterations. Since i didn't implement any optimization
    and result compilation happens in the very end you will eat throught your RAM very fast. One time I reached 19GB ram at the end. 
    
- **OneExperimentData** - python script will output data in this list when it finish working.
- **AllExperimentData** - here I dump data from experiment for ruther use.
- **Results** - here you can compare different experiments. There are graphs for HP damage, Armor durablity damage, suppression, AV damage
- **RawDamage** - here you can see weapon damage numbers, for some spherical situation where enemies have infinite HP. May be interesting to compare it to actual results. 
  
