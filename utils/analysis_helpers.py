import pickle
import evaluate
from utils.task_config import task_config
import pandas as pd


def get_table(df_orig):
    df = df_orig[df_orig.consistency != -1]
    idx = sorted(set(df['task/prompt_1']).union(df['task/prompt_2']))

    return (df.pivot(index='task/prompt_1', columns='task/prompt_2', values='consistency')
            .reindex(index=idx, columns=idx)
            .fillna(0, downcast='infer')
            .pipe(lambda x: (x + x.values.T) / 2))


def load_standardized_response(task_collection, subtask, language, instruction_version, temperature=0.25):
    path = ("results_gpt-turbo-0301/" + task_collection + "/" + subtask + "/" + "temp-" +
            str(temperature) + "_topp-1.0_maxt-256_instruction-" + instruction_version + "/" +
            language + "/standardized_responses.pkl")

    with open(path, "rb") as f:
        standardized_responses = pickle.load(f)

    return standardized_responses


def get_consistency_matrix(task_instruction, task_collection, subtask, temperature=0.25):
    consistencies = {
        "task/prompt_1": [],
        "task/prompt_2": [],
        "consistency": []
    }
    max_invalid = 0

    for tl1, il1 in task_instruction:

        label_map = task_config[task_collection][subtask]["label_map"][il1]
        label_map[-1] = -1

        responses1 = load_standardized_response(task_collection, subtask, tl1, il1, temperature=temperature)
        if responses1:
            predictions1 = [label_map[response] for response in responses1]

        for tl2, il2 in task_instruction:

            label_map = task_config[task_collection][subtask]["label_map"][il2]
            label_map[-1] = -1

            responses2 = load_standardized_response(task_collection, subtask, tl2, il2, temperature=temperature)

            consistencies["task/prompt_1"].append(tl1 + " / " + il1)
            consistencies["task/prompt_2"].append(tl2 + " / " + il2)

            if responses2:
                predictions2 = [label_map[response] for response in responses2]

            if responses1 and responses2:
                accuracy = evaluate.load("accuracy")
                result = accuracy.compute(references=predictions1, predictions=predictions2)
                consistencies["consistency"].append(result["accuracy"])
                counter1 = len([r for r in responses1 if r == -1]) / len(responses1)
                counter2 = len([r for r in responses2 if r == -1]) / len(responses2)
                if counter1 > max_invalid or counter2 > max_invalid:
                    max_invalid = max(counter1, counter2)
            else:
                consistencies["consistency"].append(-1)
    print("maximum % of invalid responses", max_invalid * 100)
    return consistencies


def load_performances(task_instruction, subtasks=("paws-x", "xnli")):
    results_dict = {
        "subtask": [],
        "task_language": [],
        "prompt_language": [],
        "performance": []
    }

    for subtask in subtasks:

        for idx, (task_language, instruction_language) in enumerate(task_instruction):

            if subtask == "paws-x":
                path = "results_gpt-turbo-0301/individual_tasks/paws-x/"
            elif subtask == "xnli":
                path = "results_gpt-turbo-0301/xglue/xnli/"
            elif subtask == "boolq":
                path = "results_gpt-turbo-0301/super_glue/boolq/"

            specific_path = (path + "temp-0.25_topp-1.0_maxt-256_instruction-" +
                             str(instruction_language) + "/" + str(task_language) + "/")

            try:
                with open(specific_path + "performance.pkl", "rb") as f:
                    performance = pickle.load(f)
                results_dict["subtask"].append(subtask)
                results_dict["task_language"].append(task_language)
                results_dict["prompt_language"].append(instruction_language)
                results_dict["performance"].append(performance["accuracy"])
            except:
                print("skip", subtask, task_language, instruction_language)
                continue

    return pd.DataFrame(data=results_dict)
