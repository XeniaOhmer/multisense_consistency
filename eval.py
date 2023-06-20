import argparse
import openai
import pickle
import os
import utils.load_task as load_task
from tqdm import tqdm
from utils.eval_metrics import evaluate_performance_metric

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
    parser.add_argument("--languages", nargs="+", default=["en"], help="language to evaluate on, e.g. en for English or"
                                                                       "de_from_en-translation for model's translation"
                                                                       "of the English task data to German")
    parser.add_argument("--temperature", type=float, default=1.0, help="output sampling temperature (between 0 and 2)")
    parser.add_argument("--top_p", type=float, default=1.0, help="nucleus sampling: the model considers the results of "
                                                                 "the tokens with top_p probability mass")
    parser.add_argument("--output_dir", default="results_gpt-turbo-0301",
                        help="directory for writing evaluation results")
    parser.add_argument("--max_tokens", default=256, help="maximum number of tokens to generate in a chat completion")
    parser.add_argument("--instruction_version", default="en", help="which instruction format (language, origin)"
                                                                    "to use")
    return parser.parse_args()


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def completions_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)


def eval_gpt_turbo(
        path,
        task_collection,
        subtask,
        language,
        temperature,
        top_p,
        max_tokens,
        instruction_version
):

    if not "translation" in language:
        test_data = load_task.load_test_split(task_collection, subtask, language)
    else:
        data_path = (
            "translations_gpt-turbo-0301/task/" + str(task_collection) + "/" + str(subtask) + "/" +
            "temp-0.25_topp-1.0_maxt-2048/" + language.split("-")[0] + "/"
        )
        print("Use translated inputs: ", data_path)
        with open(data_path + "dataset.pkl", "rb") as f:
            test_data = pickle.load(f)
    model_input, labels = load_task.format_data(test_data, task_collection, subtask, instruction_version)
    print("Example input: ", model_input[0])

    completions = []
    responses = []

    for datapoint in tqdm(model_input):

        completion = completions_with_backoff(
            model="gpt-3.5-turbo-0301",
            messages=
            [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": datapoint}
            ],
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens
        )

        completions.append(completion)
        responses.append(completion['choices'][0]['message']['content'])

    with open(path + "completions.pkl", "wb") as f:
        pickle.dump(completions, f)
    with open(path + "responses.pkl", "wb") as f:
        pickle.dump(responses, f)

    standardized_responses, performance = evaluate_performance_metric(task_collection,
                                                                      subtask,
                                                                      instruction_version,
                                                                      labels,
                                                                      responses)
    print("performance", performance)

    with open(path + "performance.pkl", "wb") as f:
        pickle.dump(performance, f)
    with open(path + "standardized_responses.pkl", "wb") as f:
        pickle.dump(standardized_responses, f)


def main():

    args = get_params()

    path = (args.output_dir + "/" + args.task_collection + "/" + args.subtask + "/" + "temp-" + str(args.temperature) +
            "_topp-" + str(args.top_p) + "_maxt-" + str(args.max_tokens) + "_instruction-" +
            args.instruction_version + "/")

    for language in args.languages:

        specific_path = path + language + "/"

        if not os.path.exists(specific_path):
            os.makedirs(specific_path)
        else:
            raise Exception("An experiment with these parameters already exists.")

        eval_gpt_turbo(
            specific_path,
            args.task_collection,
            args.subtask,
            language,
            args.temperature,
            args.top_p,
            args.max_tokens,
            args.instruction_version
        )


if __name__ == '__main__':
    main()
