from pickle import FALSE


class WeaponClass:
    def __init__(self,key,max_range,ideal_range,dmg_hp,dmg_armor,armor_pen,armor_pen_dropoff, supression, elements_hit,
                 rof,acc_mod,acc_dropoff,dmg_hp_dropoff, dmg_armor_dropfff,weapon_type="None"):


        self.key = key
        self.weapon_type = weapon_type
        self.max_range = int(max_range)
        self.ideal_range = int(ideal_range)
        self.rof = int(rof)

        self.accuracy_bonus = int(acc_mod)
        self.accuracy_dropoff = float(acc_dropoff)

        self.dmg_hp = int(dmg_hp)
        self.dmg_hp_dropoff = float(dmg_hp_dropoff)

        self.dmg_armor = int(dmg_armor)
        self.dmg_armor_dropoff = float(dmg_armor_dropfff)
        self.armor_pen = int(armor_pen)
        self.armor_pen_dropoff = float(armor_pen_dropoff)

        self.supression = float(supression)

    def get_effective_penetration(self,shot_range):
        effective_penetration = self.armor_pen + self.armor_pen_dropoff*(shot_range-1)
        return effective_penetration

    def get_effective_hp_dmg(self,shot_range):
        effective_dmg_hp = self.dmg_hp + (self.dmg_hp_dropoff*(shot_range-1))
        return effective_dmg_hp
    
    def get_effective_armor_dmg(self,shot_range):
        effective_dmg_armor = self.dmg_armor + (self.dmg_armor_dropoff*(shot_range-1))
        return effective_dmg_armor

    def get_effective_accuracy(self, shot_range, sl_accuracy):
        effective_acc = (self.accuracy_bonus + sl_accuracy) + abs(shot_range-self.ideal_range)*self.accuracy_dropoff

        # print(f"Shoot range = {shot_range}, drop_off_per_miss_range = {self.accuracy_dropoff}, effective accuracy = {effective_acc}")
        return effective_acc