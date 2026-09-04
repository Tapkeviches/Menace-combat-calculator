class EnemуSquadClass:
    def __init__(self, key, unit_hp,unit_armor_value,unit_armor_dur,unit_amount, discipline, enemy_type="infantry",morale=0):
        self.key = key
        self.type = enemy_type
        self.unit_hp = int(unit_hp)
        self.unit_amount = int(unit_amount)

        self.squad_morale = int(morale)
        self.discipline = int(discipline)

        self.defence = 0.0
        self.damage_reduction = 0.0

        self.suppressed = False
        self.pinned_down = False
        self.suppression = 0.0
        self.suppression_reduction = 0.0

        self.unit_armor_value = int(unit_armor_value)
        self.unit_armor_durability= int(unit_armor_dur)

        self.squad_armor_durability_max = self.unit_armor_durability*self.unit_amount
        self.squad_armor_durability_current = self.squad_armor_durability_max

        self.squad_list = []

        squaddies = int(unit_amount)
        while squaddies >0:
             self.squad_list.append(self.unit_hp)
             squaddies -= 1


    def apply_suppressed_status(self):
        self.defence += 0.15
        self.damage_reduction += 0.15
        return

    def remove_suppressed_status(self):
        self.defence -= 0.15
        self.damage_reduction -= 0.15

    def apply_pinned_down_status(self):
        self.defence += 0.3
        self.damage_reduction += 0.3
        self.suppression_reduction += 0.5

    def apply_cover(self,cover_size):
        if cover_size == "Light":
            self.defence += 20
            self.damage_reduction += 0.2
            self.suppression_reduction += 0.1
        elif cover_size == "Medium":
            self.defence += 40
            self.damage_reduction += 0.4
            self.suppression_reduction += 0.2
        elif cover_size == "Heavy":
            self.defence += 60
            self.damage_reduction += 0.6
            self.suppression_reduction += 0.4
        else:
            return

    def apply_armor_dura_dmg(self,armor_dura_dmg):
        self.squad_armor_durability_current -= armor_dura_dmg

    def apply_hp_dmg(self, hp_dmg_received):
        target_index = len(self.squad_list)-1
        target = self.squad_list[target_index]
        if hp_dmg_received >= target:
            self.squad_list.pop(target_index)
            return
        else:

            new_target_hp = target - hp_dmg_received
            self.squad_list[target_index] = new_target_hp
            return

    def apply_suppression_dmg(self,sup_dmg):
        # print(f"Old suppression = {self.suppression}")
        # print(f"Squad supression reduction = {self.suppression_reduction}")
        raw_suppression = sup_dmg * (1-self.suppression_reduction)
        self.suppression += round(raw_suppression,1)
        # print(f"New suppression = {self.suppression}")


        if self.suppression > 100:
            self.suppression = 100
            # print(f"New suppression after check = {self.suppression}")

        if self.suppression >= 66 and self.pinned_down != True:
            self.suppressed = False
            self.remove_suppressed_status()
            self.pinned_down = True
            self.apply_pinned_down_status()
            # print("Squad was pinned down should not be pinned again")
            # print(f"Suppression after pin {self.suppression}")

        if self.suppression >= 33 and self.suppressed!=True and self.pinned_down!=True:
            self.suppressed = True
            self.apply_suppressed_status()
            # print("Squad was suppressed should not be suppressed again")
            # print(f"Suppression after supression status {self.suppression}")


