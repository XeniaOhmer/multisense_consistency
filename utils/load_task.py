from datasets import load_dataset
from utils.task_config import task_config


def load_test_split(task_collection, subtask, language):
    """
    Load test split for an xglue subtask in a specific language.
    :param subtask: subtask (e.g. "xnli")
    :param language: langauge (e.g. "en")
    :return: test split in the form of a dataset
    """

    assert task_collection, subtask in [("xglue", "xnli"),
                                        ("individual_tasks", "paws-x"),
                                        ("super_glue", "boolq")]
    assert language in task_config[task_collection][subtask]["languages"]

    if subtask == "xnli":
        dataset = load_dataset(path="xglue", name=subtask, split=f"test.{language}")
    elif subtask == "paws-x":
        dataset = load_dataset(path=subtask, name=language, split="test")
    else:
        dataset = load_dataset(path="super_glue", name=subtask, split="validation")

    return dataset


def format_data(dataset, task_collection, subtask, instruction_version):
    model_inputs = []
    sentence_keys = task_config[task_collection][subtask]["sentence_keys"]
    prefix = task_config[task_collection][subtask]["prefix"][instruction_version]
    suffix = task_config[task_collection][subtask]["suffix"][instruction_version]

    sentence_name = {"en": "Sentence",
                     "de": "Satz",
                     "zh": "句子",
                     "fr": "Phrase",
                     "es": "Oración",
                     "de_test1": "Satz",
                     "de_test2": "Satz",
                     "de_test3": "Satz",
                     "de_test4": "Satz",
                     "de_test5": "Satz",
                     "de_from_en-translation": "Satz",
                     "zh_from_en-translation": "句子",
                     "en_from_de-translation": "Sentence",
                     "en_from_zh-translation": "Sentence",
                     "en_from_es-translation": "Sentence",
                     "en_from_fr-translation": "Sentence"
                     }

    for datapoint in dataset:
        model_input = prefix
        for i, key in enumerate(sentence_keys):
            if subtask == "xnli" or subtask == "paws-x":
                model_input += " " + sentence_name[instruction_version] + f" {i + 1}: \"" + datapoint[key] + "\""
            elif subtask == "boolq":
                if i == 0:
                    model_input += datapoint[key] + " "
                elif i == 1:
                    question = datapoint[key].capitalize()
                    if question[-1] not in ["?", "？"]:
                        if instruction_version[0:2] in ["en", "de", "fr"]:
                            question += "?"
                        elif instruction_version[0:2] in ["zh"]:
                            question += "？"
                        elif instruction_version[0:2] in ["es"]:
                            question = "¿" + question + "?"
                    question += " "
                    model_input += question
        model_input += suffix
        model_inputs.append(model_input)

    labels = dataset["label"]

    return model_inputs, labels
