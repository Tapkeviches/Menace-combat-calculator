import copy
import SheetStorage

import ExperimentRunner

class PrintingExperimentResults:
    @staticmethod
    def print_average_dmges(experiment_data):
        sheet = SheetStorage.balance_file
        worksheet = sheet.worksheet("OneExperimentData")
        worksheet.batch_clear(["A2:H"])
        list_to_print = []
        for result in experiment_data:
            experiment_key = result[0]
            result.pop(0)
            average_results = copy.copy(result)
            for avg_result in average_results:
                avg_result.insert(0,experiment_key)
                list_to_print.append(avg_result)
            list_to_print.append([])

        worksheet.update(list_to_print,range_name="A2:H")
data = copy.copy(ExperimentRunner.experiment_results)
# print(data)
compiled_data = []

for experiment in data:
    experiment_compiled_data = []

    experiment_name = experiment[0]
    experiment_compiled_data.append(experiment_name)
    experiment.pop(0)
    shooting_data = copy.copy(experiment)
    # print(f"Shooting data object - {shooting_data}\n")
    # print(f"First - {shooting_data[0]}")
    # print(f"Second - {shooting_data[1]}")
    # print(f"Third - {shooting_data[2]}")

    for shooting in shooting_data:
        current_range = shooting[0]
        shooting.pop(0)
        shooting_result = [current_range]

        total_shots = 0
        total_armor_dmg = 0.0
        total_av_dmg = 0.0
        total_hp_damage = 0.0
        total_suppression = 0.0
        iterations_amount = 0
        iteration_kills = 0
        iterations = copy.copy(shooting)
        # print(f"Iterations object - {iterations}")
        for iteration in iterations:
            total_shots = 0
            iteration.pop(0)
            iteration_kills += iteration.pop(0)
            shots = copy.copy(iteration)

            for each_shot in shots:
                # if current_range == 5:
                #     print(f"Current range = {current_range}")
                #     print(f"Each shot = {each_shot} ")
                total_armor_dmg += each_shot[3]
                total_av_dmg += each_shot[4]
                total_hp_damage += each_shot[5]
                total_suppression += each_shot[6]
                total_shots += 1
            iterations_amount += 1

        shooting_result.append(total_shots)
        # print(f"Total armor damage = {total_armor_dmg} iteration amount = {iterations_amount}")
        shooting_result.append(round(total_armor_dmg/iterations_amount, 1))
        shooting_result.append(round(total_av_dmg/iterations_amount, 1))
        shooting_result.append(round(total_hp_damage/iterations_amount,1))
        shooting_result.append(round(total_suppression/iterations_amount,1))
        shooting_result.append(round(iteration_kills/iterations_amount,1))
        experiment_compiled_data.append(shooting_result)
    compiled_data.append(experiment_compiled_data)
# print(f"\n{data}\n")
print("=====================================================================================================\n\n")
print(compiled_data)

PrintingExperimentResults.print_average_dmges(compiled_data)

        


