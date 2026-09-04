import random
from random import randrange
from typing import final
import math

import EnemySquad
import Weapon

def check_for_armor_pen(enemy_squad, weapon, combat_range):
    effective_armor_pen = weapon.get_effective_penetration(combat_range)
    # print(f"Effective armor pen = {effective_armor_pen}")
    effective_av = (enemy_squad.squad_armor_durability_current/enemy_squad.squad_armor_durability_max)*enemy_squad.unit_armor_value
    # print(f"Efective av = {effective_av}")
    chance_to_penetrate = 100 - 3*(effective_av-effective_armor_pen)
    roll = random.randrange(0,100)

    # print(f"Стреляю оружием {weapon.key}")
    # print(f"Эффективное пробитие - {effective_armor_pen}")
    # print(f"Эффективная броня цели - {effective_av}")
    # print(f"Шанс пробития = {chance_to_penetrate}")
    # print(f"Кубик = {roll}")

    if roll < chance_to_penetrate:
        armor_penetrated = True
    else:
        armor_penetrated = False

    # print(f"Броня пробита - {armor_penetrated}")
    return armor_penetrated

def check_for_hit(weapon, enemy_squad, combat_range, sl_accuracy):
    if combat_range > weapon.max_range:
        return False
    chance_to_hit = weapon.get_effective_accuracy(combat_range,sl_accuracy) - enemy_squad.defence
    # print(f"Chance to hit = {chance_to_hit}")
    roll = randrange(1,100)
    # print(f"Roll to hit = {roll}")
    if roll > chance_to_hit:
        # print(f"roll > chance_to_hit\n")
        return False
    else:
        # print(f"roll < chance_to_hit\n")
        return True

def calculate_armor_durability_damage(enemy_squad, weapon, combat_range, armor_penetrated):

    weapon_armor_dmg = weapon.dmg_armor + (weapon.dmg_armor_dropoff*combat_range)

    if armor_penetrated:
        penetration_mod = 0.15
    else:
        penetration_mod = 1

    enemy_squad_armor_durability_mod = pow((enemy_squad.squad_armor_durability_current/enemy_squad.squad_armor_durability_max),2)

    armor_damage = round(weapon_armor_dmg*penetration_mod*enemy_squad_armor_durability_mod,4)
    # print(f"Shot dealt {armor_damage} of armor damage to target")
    # print(f"New squad armor durability value = {enemy_squad.squad_armor_durability_current - armor_damage}")
    return armor_damage

def calculate_av_damage(enemy_squad,armor_durability_damage):
    old_av = enemy_squad.unit_armor_value*pow((enemy_squad.squad_armor_durability_current/enemy_squad.squad_armor_durability_max),2)
    new_av = enemy_squad.unit_armor_value*pow(((enemy_squad.squad_armor_durability_current-armor_durability_damage)/enemy_squad.squad_armor_durability_max),2)
    av_diff = round(old_av-new_av,3)
    return av_diff

def calculate_raw_hp_damage(weapon,combat_range):
    if weapon.max_range < combat_range:
        return 0
    else:
        hit_dmg = math.floor(weapon.dmg_hp + weapon.dmg_hp_dropoff * combat_range)
        print(f" Weapon = {weapon.key} on the range of {combat_range} doing {hit_dmg} damage to target")
        return hit_dmg



def calculate_suppression_from_shot(hit_confirmed,enemy_squad,weapon):
    # print(f"Weapon base suppression = {weapon.supression}")
    # print(f"Enemy suppression reduction = {enemy_squad.suppression_reduction}")
    # print(f"Enemy pinned down - {enemy_squad.pinned_down}")
    raw_suppression = weapon.supression*(100-enemy_squad.discipline)/100
    # print(f"Suppression after discipline mitigation = {raw_suppression} ")
    if hit_confirmed:
        final_suppression = round(raw_suppression*(1-enemy_squad.suppression_reduction),2)
        # print(f"Suppression for succsesfull hit = {final_suppression}")
    else:
        final_suppression = round(raw_suppression*(1-enemy_squad.suppression_reduction)*0.3,2)
        # print(f"Suppression for failed hit = {final_suppression}")
    final_suppression *= 2
    return final_suppression




