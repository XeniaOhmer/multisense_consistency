import argparse
import openai
import pickle
import os
import utils.load_task as load_task
from tqdm import tqdm
from utils.language_codes import language_codes
from utils.response_standardization import cut_double_quotes
from utils.task_config import task_config
from utils.eval_metrics import evaluate_translation_quality
from datasets import Dataset

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

openai.organization = ""  # add your organization here
openai.api_key = os.getenv("")  # add your api key here

def get_params():
    """Parse arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--task_collection", type=str, required=True, help="xglue, or individual_tasks")
    parser.add_argument("--subtask", type=str, required=True, help="subtask, e.g. xnli")
    parser.add_argument("--target_languages", required=True, nargs="+", help="target languages")
    parser.add_argument("--source_language", type=str, default="en")
    parser.add_argument("--translation_type", type=str, required=True, help="instruction or task")
    parser.add_argument("--temperature", type=float, default=1.0, help="output sampling temperature (between 0 and 2)")
    parser.add_argument("--top_p", type=float, default=1.0, help="nucleus sampling: the model considers the results of "
                                                                 "the tokens with top_p probability mass")
    parser.add_argument("--output_dir", default="translations_gpt-turbo-0301", help="directory for writing translations")
    parser.add_argument("--max_tokens", default=2048, help="maximum number of tokens to generate in a chat completion")
    return parser.parse_args()


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def completions_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)


def translate_with_gpt_turbo(
        path,
        task_collection,
        subtask,
        source_language,
        target_language,
        translation_type,
        temperature,
        top_p,
        max_tokens,
):

    instruction_set = {
        "en": "Please translate the following text into " + language_codes["en"][target_language] + ": \n",
        "de": "Bitte übersetze den folgenden Text ins " + language_codes["de"][target_language] + ": \n",
        "zh": "请将下面的文字翻译成" + language_codes["zh"][target_language] + ": \n",
        "fr": "Veuillez traduire le texte suivant en " + language_codes["fr"][target_language] + ": \n",
        "es": "Por favor, traduzca el siguiente texto al " + language_codes["es"][target_language] + ": \n"
    }

    # translate instruction
    instruction = instruction_set[source_language]

    if translation_type == "instruction":

        sentence = {
            "en": "Sentence",
            "de": "Satz",
            "fr": "Phrase",
            "es": "Oración",
            "zh": "句子"
        }

        prefix = task_config[task_collection][subtask]["prefix"][source_language]
        suffix = task_config[task_collection][subtask]["suffix"][source_language]

        completions = []
        responses = []
        for text in [prefix, suffix, sentence[source_language]]:

            print(instruction + "\"" + text + "\"")

            completion = completions_with_backoff(
                model="gpt-3.5-turbo-0301",
                messages=
                [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": instruction + "\"" + text + "\""}
                ],
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens
            )
            completions.append(completion)
            responses.append(completion['choices'][0]['message']['content'])

        print("Responses", responses)

        with open(path + "completions.pkl", "wb") as f:
            pickle.dump(completions, f)
        with open(path + "responses.pkl", "wb") as f:
            pickle.dump(responses, f)

    # translate task contents
    elif translation_type == "task":

        test_data = load_task.load_test_split(task_collection, subtask, source_language)

        translated_data = {}
        completions = {}

        for column_name in test_data.column_names:

            if column_name in task_config[task_collection][subtask]["sentence_keys"]:

                print("Translating " + column_name)

                completions_sentence_key = []
                responses_sentence_key = []

                for idx, text in enumerate(tqdm(test_data[column_name])):

                    if idx == 0:
                        print("Example input: ", instruction + text)

                    completion = completions_with_backoff(
                        model="gpt-3.5-turbo-0301",
                        messages=
                        [
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": instruction + text}
                        ],
                        temperature=temperature,
                        top_p=top_p,
                        max_tokens=max_tokens
                    )
                    completions_sentence_key.append(completion)
                    response = completion['choices'][0]['message']['content']
                    response_quotes_removed = cut_double_quotes(response)
                    responses_sentence_key.append(response_quotes_removed)

                completions[column_name] = completions_sentence_key
                translated_data[column_name] = responses_sentence_key

            else:
                print("Keeping " + column_name)
                translated_data[column_name] = test_data[column_name]

        ds_translation = Dataset.from_dict(translated_data)
        with open(path + "completions.pkl", "wb") as f:
            pickle.dump(completions, f)
        with open(path + "dataset.pkl", "wb") as f:
            pickle.dump(ds_translation, f)

        if task_config[task_collection][subtask]["multilingual"]:
            translation_quality_metrics = evaluate_translation_quality(
                task_collection,
                subtask,
                source_language,
                target_language,
                path
            )

            with open(path + "translation_scores.pkl", "wb") as f:
                pickle.dump(translation_quality_metrics, f)


def main():
    args = get_params()

    path = (args.output_dir + "/" + args.translation_type + "/" + args.task_collection + "/" + args.subtask + "/" +
            "temp-" + str(args.temperature) + "_topp-" + str(args.top_p) + "_maxt-" + str(args.max_tokens)) + "/"

    for language in args.target_languages:

        specific_path = path + language + "_from_" + args.source_language + "/"

        if not os.path.exists(specific_path):
            os.makedirs(specific_path)
        else:
            raise Exception("An experiment with these parameters already exists.")

        translate_with_gpt_turbo(
            specific_path,
            args.task_collection,
            args.subtask,
            args.source_language,
            language,
            args.translation_type,
            args.temperature,
            args.top_p,
            args.max_tokens
        )


if __name__ == '__main__':
    main()
