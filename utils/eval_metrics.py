from utils.task_config import task_config
import evaluate
import pickle
import jieba
import utils.load_task as load_task
from rouge_chinese import Rouge
from comet import download_model, load_from_checkpoint
from utils.response_standardization import standardize_classification_response


def evaluate_performance_metric(task_collection, subtask, instruction_version, labels, responses):
    label_map = task_config[task_collection][subtask]["label_map"][instruction_version]
    print("LABEL MAP", label_map)
    if task_config[task_collection][subtask]["task_type"] == "classification":
        standardized_responses = standardize_classification_response(responses, label_map)
        label_map[-1] = -1  # for responses that cannot be mapped onto one of the targets
        predictions = [label_map[response] for response in standardized_responses]
        accuracy = evaluate.load("accuracy")
        result = accuracy.compute(references=labels, predictions=predictions)
        return standardized_responses, result


def evaluate_translation_quality(
        task_collection,
        subtask,
        source_language,
        target_language,
        path
):
    test_data_source = load_task.load_test_split(task_collection, subtask, source_language)
    test_data_target = load_task.load_test_split(task_collection, subtask, target_language)

    with open(path + "dataset.pkl", "rb") as f:
        test_data_translation = pickle.load(f)

    sentence_keys = task_config[task_collection][subtask]["sentence_keys"]

    sources = []
    machine_translations = []
    references = []

    for key in sentence_keys:
        sources += test_data_source[key]
        machine_translations += test_data_translation[key]
        references += test_data_target[key]

    n = len(sources)

    eval_data = []
    for i in range(n):
        eval_data.append(
            {
                "src": sources[i],
                "mt": machine_translations[i],
                "ref": references[i]
            }
        )

    print("translation eval data: ", eval_data[0])
    print("length translation eval data: ", len(eval_data))

    model_path = download_model("Unbabel/wmt22-comet-da")
    model = load_from_checkpoint(model_path)
    comet_scores = model.predict(eval_data, batch_size=8, gpus=0)

    bleu = evaluate.load("sacrebleu")
    if target_language == "zh":
        tokenize = "zh"
    else:
        tokenize = "13a"
    bleu_scores = bleu.compute(predictions=machine_translations,
                               references=[[ref] for ref in references],
                               tokenize=tokenize)
    print(bleu_scores)

    if target_language == "zh":
        rouge = Rouge()
        machine_translations_jieba = [' '.join(jieba.cut(elem)) for elem in machine_translations]
        references_jieba = [' '.join(jieba.cut(elem)) for elem in references]
        rouge_scores = rouge.get_scores(machine_translations_jieba, references_jieba, avg=True)
        rouge_1 = rouge_scores["rouge-1"]["f"]
        rouge_2 = rouge_scores["rouge-2"]["f"]
        rouge_l = rouge_scores["rouge-l"]["f"]
    else:
        rouge = evaluate.load("rouge")
        rouge_scores = rouge.compute(predictions=machine_translations, references=references)
        rouge_1 = rouge_scores["rouge1"]
        rouge_2 = rouge_scores["rouge2"]
        rouge_l = rouge_scores["rougeL"]

    results = {
        "comet": comet_scores[-1],
        "bleu": bleu_scores["score"],
        "rouge1": rouge_1,
        "rouge2": rouge_2,
        "rouge-l": rouge_l,
        "comet_all": comet_scores,
        "bleu_all": bleu_scores,
        "rouge_all": rouge_scores
    }
    return results

# if __name__ == '__main__':
#     import load_task
#     task_collection = "xglue"
#     subtask = "xnli"
#     language = "en_from_zh-translation"
#     instruction_version = "en"
#
#     path = ("../results_gpt-turbo-0301/" + task_collection + "/" + subtask + "/temp-0.25_topp-1.0_maxt-256_instruction-"
#             + str(instruction_version) + "/" + str(language) + "/")
#     with open(path + "responses.pkl", "rb") as f:
#         responses = pickle.load(f)
#     with open(path + "performance.pkl", "rb") as f:
#         performance_old = pickle.load(f)
#     with open(path + "standardized_responses.pkl", "rb") as f:
#         standardized_responses_old = pickle.load(f)
#
#     if not "translation" in language:
#         test_data = load_task.load_test_split(task_collection, subtask, language)
#     else:
#         data_path = (
#             "../translations_gpt-turbo-0301/task/" + str(task_collection) + "/" + str(subtask) + "/" +
#             "temp-0.25_topp-1.0_maxt-2048/" + language.split("-")[0] + "/"
#         )
#         print("Use translated inputs: ", path)
#         with open(data_path + "dataset.pkl", "rb") as f:
#             test_data = pickle.load(f)
#     model_input, labels = load_task.format_data(test_data, task_collection, subtask, instruction_version)
#     standardized_responses, result = evaluate_performance_metric(task_collection,
#                                                                  subtask,
#                                                                  instruction_version,
#                                                                  labels,
#                                                                  responses)
#     for i in range(len(standardized_responses)):
#         if standardized_responses_old[i] != standardized_responses[i]:
#             print(i, "ALARM")
#             print(responses[i])
#             print(standardized_responses_old[i], standardized_responses[i])
#     print(performance_old, result)
#
#     with open(path + "standardized_responses.pkl", "wb") as f:
#         pickle.dump(standardized_responses, f)
#     with open(path + "performance.pkl", "wb") as f:
#         pickle.dump(result, f)
