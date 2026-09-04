import copy
import CombatCalculation
import EnemySquad
import SheetStorage
import Weapon
import csv


DATA_SOURCE = "ONLINE" # Set the source for experiment and entities data. OFFLINE will take it from Configs file.
                        # ONLINE - will download them from google sheets file you set up in SheetStorage module. It uses
                        # gspread library. So you will need to generate server creds in google console. Link to guide and
                        # documentation - https://docs.gspread.org/en/latest/oauth2.html#for-bots-using-service-account
ENEMY_DATA_LIST = "EnemyStats"
WEAPON_DATA_LIST = "WeaponStats"
EXPERIMENT_INFO_LIST = "ExperimentConfig"


sheet_storage = SheetStorage.OnlineSheetStorageClass() # Used to get data from google sheets

experiments_list = [] # List of experiments we will conduct
weapon_list = [] # List with all the weapons we got from config files
enemy_squad_list = [] # List of all the ehemies we got from config files

class ExperimentInfo:
    def __init__(self, experiment_id, weapon_key, enemy_squad_key, player_squad_size, sl_accuracy, range_of_engagement, cover_level, iterations):
        self.id = experiment_id
        self.weapon_key = weapon_key
        self.enemy_squad_key = enemy_squad_key
        self.player_squad_size = int(player_squad_size)
        self.sl_accuracy = int(sl_accuracy)
        self.range_of_engagement = int(range_of_engagement)
        self.iterations_amount =int(iterations)
        self.cover_level = cover_level

    def get_weapon_stats(self,weapon_data_storage):
        for weapon_ex in weapon_data_storage:
            if weapon_ex.key == self.weapon_key:
                return weapon_ex

    def get_enemy_stats(self,enemy_data_storage):
        for enemy_ex in enemy_data_storage:
            if enemy_ex.key == self.enemy_squad_key:
                return copy.deepcopy(enemy_ex)

if DATA_SOURCE == "ONLINE":
    # Получаем данные об экспериментах, которые хотим провести из таблиц
    experiment_conditions = sheet_storage.get_sheet_from_storage(EXPERIMENT_INFO_LIST)
    for row in experiment_conditions:
        new_experiment = ExperimentInfo(experiment_id = row["ExperimentId"], weapon_key=row["WeaponKey"],enemy_squad_key=row["EnemySquadKey"],
                                        player_squad_size = row["PlayerSquadSize"], range_of_engagement=0,
                                        iterations=row["Iterations"], cover_level=row["TargetCover"], sl_accuracy=row["SquadLeaderAcc"])
        experiments_list.append(new_experiment)
    # for experiment in experiments_list:
    #     print(f"Experiment ID = {experiment.id} and experiment Weapon = {experiment.weapon_key}\n")

    # Получаем данные об оружии из таблиц
    weapon_stats = sheet_storage.get_sheet_from_storage(WEAPON_DATA_LIST)
    for row in weapon_stats:
        if row["Supp"] == "":
            continue
        new_weapon = Weapon.WeaponClass(key = row["Name"],weapon_type = str(row["Type"]),max_range = row["Rng"],ideal_range =row["IdealRng"],
                                        dmg_hp=row["HP Dmg"],dmg_armor=row["Armor Dmg"],armor_pen=row["Armor Pen"],armor_pen_dropoff=row["PenDropoff"],supression = row["Supp"],
                                        elements_hit=row["Elems Hit"],rof=row["RoF"],acc_mod=row["Acc Mod"],acc_dropoff=row["AccDropOff"],
                                        dmg_hp_dropoff=row["DmgDropoff"], dmg_armor_dropfff=row["DmgArmorDropoff"])
        weapon_list.append(new_weapon)
    # for weapon in weapon_list:
    #     print(f"Weapon name = {weapon.key} it's type - {weapon.weapon_type} it does {weapon.dmg_hp} with ideal range of {weapon.ideal_range}\n")

    # Получаем данные об отрядах мобов с которыми можем сражаться
    enemy_stats = sheet_storage.get_sheet_from_storage(ENEMY_DATA_LIST)
    for row in enemy_stats:
        new_enemy = EnemySquad.EnemуSquadClass(key=row["Name"], unit_hp=row["HP per soldier"] ,unit_armor_value=row["Armor"],
                                               unit_armor_dur=row["Armor Durability"],unit_amount=row["Squad Size"], discipline=row["Discipline"])
        enemy_squad_list.append(new_enemy)
    # for enemy in enemy_squad_list:
    #     print(f"Squad name = {enemy.key}")
elif DATA_SOURCE == "OFFLINE":
    with open("Configs/Menace Balance Shenanigans - EnemyStats.csv", newline='') as enemy_stats:
        reader = csv.DictReader(enemy_stats)
        for row in reader:
            new_enemy = EnemySquad.EnemуSquadClass(key=row["Name"], unit_hp=row["HP per soldier"],
                                                   unit_armor_value=row["Armor"],
                                                   unit_armor_dur=row["Armor Durability"],
                                                   unit_amount=row["Squad Size"], discipline=row["Discipline"])
            enemy_squad_list.append(new_enemy)

    with open("Configs/Menace Balance Shenanigans - ExperimentConfig.csv", newline='') as experiment_config:
        reader = csv.DictReader(experiment_config)
        for row in reader:
            new_experiment = ExperimentInfo(experiment_id = row["ExperimentId"], weapon_key=row["WeaponKey"],enemy_squad_key=row["EnemySquadKey"],
                                        player_squad_size = row["PlayerSquadSize"], range_of_engagement=0,
                                        iterations=row["Iterations"], cover_level=row["TargetCover"], sl_accuracy=row["SquadLeaderAcc"])
            experiments_list.append(new_experiment)

    with open("Configs/Menace Balance Shenanigans - WeaponStats.csv", newline='') as weapon_config:
        reader = csv.DictReader(weapon_config)
        for row in reader:
            new_weapon = Weapon.WeaponClass(key = row["Name"],max_range = row["Rng"],ideal_range =row["IdealRng"],
                                        dmg_hp=row["HP Dmg"],dmg_armor=row["Armor Dmg"],armor_pen=row["Armor Pen"],armor_pen_dropoff=row["PenDropoff"],supression = row["Supp"],
                                        elements_hit=row["Elems Hit"],rof=row["RoF"],acc_mod=row["Acc Mod"],acc_dropoff=row["AccDropOff"],
                                        dmg_hp_dropoff=row["DmgDropoff"], dmg_armor_dropfff=row["DmgArmorDropoff"], weapon_type=row["Type"])
            weapon_list.append(new_weapon)
else:
    print("Setup data source for data on units and experiments")

experiment_results = []

for experiment in experiments_list:
    experiment_squad = experiment.get_enemy_stats(enemy_squad_list)
    experiment_squad.apply_cover(experiment.cover_level)
    experiment_weapon = experiment.get_weapon_stats(weapon_list)
    experiment_outer_result = [experiment.id]
    if experiment.iterations_amount == 0:
        continue
    shooting_range = 1
    while shooting_range <= 10:
        experiment_inner_result = [shooting_range]
        experiment.range_of_engagement = shooting_range
        iterations_left = experiment.iterations_amount
        iteration_number = 1
        while iterations_left > 0:
            iteration_squad = copy.deepcopy(experiment_squad)
            print("===============================New iteration started ======================================")
            print(f"Weapon = {experiment_weapon.key}")
            print(f"Current shooting range = {experiment.range_of_engagement}")
            print(f"Squad key = {iteration_squad.key}")
            print(f"Squad suppression reduction = {iteration_squad.suppression_reduction}")
            print(f"Squad accuracy = {experiment.sl_accuracy}")
            iteration_result = [iteration_number]
            iteration_kills = 0
            shots_amount = int(experiment.player_squad_size * experiment_weapon.rof)
            shot_number = 1
            while shots_amount >0:
                # print(f"\n\nShots left = {shots_amount}")
                shot_result = [shot_number]  # 0 - Номер выстрела, 1 - Попадание по цели, 2 - Пробитие брони цели, 3 - Урон HP цели, 4 - Урон броне цели, 5 - Урон AV цели

                #Проверяем, что отряд еще существует
                if len(iteration_squad.squad_list) == 0:
                    print(f"Squad is dead")
                    shot_result.append(False)  # Hit confirmation
                    shot_result.append(False)  # Armor penetration confirmation
                    shot_result.append(0.0)  # Shot HP damage
                    shot_result.append(0.0)  # Shot Armor durability damage
                    shot_result.append(0.0)  # Shot armor value damage
                    shot_result.append(0.0)  # Suppression the shot did to target squad
                    shot_result.append("Dead") # Squad status
                    iteration_result.append(shot_result)
                    # print("Target squad died")
                    print(shot_result)
                    break
                # Check for hit happening
                if not CombatCalculation.check_for_hit(weapon=experiment_weapon, enemy_squad=iteration_squad,combat_range=experiment.range_of_engagement,sl_accuracy=experiment.sl_accuracy):
                        if experiment_weapon.max_range < shooting_range:
                            shot_result.append(False)
                            shot_result.append(False)
                            shot_result.append(0.0)
                            shot_result.append(0.0)
                            shot_result.append(0.0)
                            shot_result.append(0.0)
                            shot_result.append("Alive")
                        else:
                            suppression_dmg = CombatCalculation.calculate_suppression_from_shot(hit_confirmed=False,
                                                                                                enemy_squad=iteration_squad,
                                                                                                weapon=experiment_weapon)
                            log_dmg = suppression_dmg * (1 - iteration_squad.suppression_reduction)
                            iteration_squad.apply_suppression_dmg(suppression_dmg)
                            shot_result.append(False)
                            shot_result.append(False)
                            shot_result.append(0.0)
                            shot_result.append(0.0)
                            shot_result.append(0.0)
                            shot_result.append(log_dmg)
                            shot_result.append("Alive")
                            # print("Target didn't get shot")
                else:
                    shot_result.append(True)
                    # Check for armor penetration
                    if not CombatCalculation.check_for_armor_pen(enemy_squad=iteration_squad,weapon=experiment_weapon,combat_range=experiment.range_of_engagement):
                        shot_result.append(False)  # Пробитие брони цели
                        armor_durability_damage = CombatCalculation.calculate_armor_durability_damage(enemy_squad=iteration_squad, weapon=experiment_weapon, combat_range=experiment.range_of_engagement, armor_penetrated=False)
                        armor_av_damage = CombatCalculation.calculate_av_damage(enemy_squad=iteration_squad,armor_durability_damage=armor_durability_damage)
                        iteration_squad.apply_armor_dura_dmg(armor_durability_damage)

                        shot_result.append(armor_durability_damage)  # Урон броне цели
                        shot_result.append(armor_av_damage)  # Урон AV цели
                        shot_result.append(0.0)  # Урон HP цели
                        suppression_dmg = CombatCalculation.calculate_suppression_from_shot(hit_confirmed=True,enemy_squad=iteration_squad,weapon=experiment_weapon)
                        log_dmg = suppression_dmg * (1-iteration_squad.suppression_reduction)
                        iteration_squad.apply_suppression_dmg(suppression_dmg)
                        shot_result.append(log_dmg)  # Количество подавления, которое получила цель

                        shot_result.append("Alive")
                        # print("Bullet didn't pierce armor")
                    else:
                        # print("Bullet pierced armor")
                        shot_result.append(True)  # Пробитие брони цели
                        armor_durability_damage = CombatCalculation.calculate_armor_durability_damage(enemy_squad=iteration_squad, weapon=experiment_weapon,
                                                                                                      combat_range=experiment.range_of_engagement, armor_penetrated=True)
                        armor_av_damage = CombatCalculation.calculate_av_damage(enemy_squad=iteration_squad,armor_durability_damage=armor_durability_damage)
                        iteration_squad.apply_armor_dura_dmg(armor_durability_damage)
                        shot_result.append(armor_durability_damage)  # Урон броне цели
                        shot_result.append(armor_av_damage)  # Урон AV цели

                        # Calculating damage target received
                        raw_hp_dmg = CombatCalculation.calculate_raw_hp_damage(weapon=experiment_weapon,combat_range=experiment.range_of_engagement)
                        current_squad_target = len(iteration_squad.squad_list)-1
                        target_hp = iteration_squad.squad_list[current_squad_target]
                        # print(f"Squad length = {len(iteration_squad.squad_list)}")
                        # print(f"Target hp = {target_hp}")
                        # print(f"Raw dmg = {raw_hp_dmg}")

                        if target_hp <= raw_hp_dmg:
                            print("Target was killed")
                            shot_result.append(target_hp)  # Урон HP цели
                            suppression_dmg = CombatCalculation.calculate_suppression_from_shot(hit_confirmed=True,enemy_squad=iteration_squad,weapon=experiment_weapon)
                            log_dmg = suppression_dmg * (1-iteration_squad.suppression_reduction) + (20 - iteration_squad.discipline*0.17)
                            iteration_squad.apply_suppression_dmg(suppression_dmg)
                            shot_result.append(log_dmg)  # Количество подавления, которое получила цель

                            # print(f"Final shot result = {target_hp}\n")
                            iteration_squad.apply_hp_dmg(raw_hp_dmg)
                            iteration_kills += 1
                            # print(f"Final squad length = {len(iteration_squad.squad_list)}\n")
                            if len(iteration_squad.squad_list)==0:
                                # print("Target squad was killed")
                                shot_result.append("Dead")
                                break
                            else:
                                shot_result.append("Alive")

                        else:
                            shot_result.append(raw_hp_dmg)
                            # print("Target survived")
                            iteration_squad.apply_hp_dmg(raw_hp_dmg)
                            suppression_dmg = CombatCalculation.calculate_suppression_from_shot(hit_confirmed=True,enemy_squad=iteration_squad,weapon=experiment_weapon)
                            log_dmg = suppression_dmg * (1-iteration_squad.suppression_reduction)
                            iteration_squad.apply_suppression_dmg(suppression_dmg)
                            shot_result.append(log_dmg)  # Количество подавления, которое получила цель
                            shot_result.append("Alive")

                iteration_result.append(shot_result)
                shot_number += 1
                shots_amount -= 1
            iteration_result.insert(1,iteration_kills)
            experiment_inner_result.append(iteration_result)
            iterations_left -= 1
            iteration_number += 1

        experiment_outer_result.append(experiment_inner_result)
        shooting_range += 1
    experiment_results.append(experiment_outer_result)


# print(experiment_results)




