# multisense_consistency

This repository accompanies the publication:

Xenia Ohmer, Elia Bruni, and Dieuwke Hupkes. "Separating form and meaning: Using self-consistency to quantify task understanding across multiple senses". Proceedings of the 3rd Workshop on Natural Language Generation, Evaluation, and Metrics (GEM). Association for Computational Linguistics.

## Datasets and instructions
We use PAWS-X, XNLI, and BoolQ provided on Huggingface. The tasks are specified with their name and the collection from which they are loaded. 
The (collection, task) pairs are: (individual_tasks, paws-x); (xglue, xnli); and (super_glue, boolq).
The original and translated instructions for each task, together with other details on the datasets, can be found in *utils.task_config*.
For details on how the datasets are loaded and integrated with the corresponding instructions, see *utils/load_task.py*.

## Translation
The different senses (here: translations) of the tasks were generated with *translate.py*. The translations can be found in the folder *translations_gpt-3.5-turbo*.
The required command line arguments for running *translate.py* are the task specifiers (collection and subtask), the target language, and the translation type ("task" or "instruction"). 
Further arguments that can be specified are source language (default: en), temperature, top-p sampling, maximum number of output tokens, and the directory for saving the results (output_dir) 
We used a temperature of 0.25, a top_p probability of 1.0, and 2048 output tokens for all our experiments.
For details on the evaluation of the translation quality, see *utils/eval_metrics.py*.

**Examples**

To generate the German translation of the English instruction for PAWS-X, as in our experiments, run:
```
python translate.py --collection individual_tasks --subtask paws-x --source_language en --target_language de --translation_type instruction --temperature 0.25 --output_dir translations_gpt-turbo-0301
```
In order to be able to use the translated instructions, add them to *utils/task_config.py*.

To generate the English translation of the Chinese input data for XNLI, as in our experiments, run: 
```
python translate.py --collection xglue --subtask xnli --source_language zh --target_language en --translation_type task --temperature 0.25 --output_dir translations_gpt-turbo-0301
```
When evaluating the model on these translations, they will be loaded from *translations_gpt-turbo-0301*. If your input data translations are in a different folder, you will have to change the corresponding code in *eval.py* (lines 58-59).

## Evaluation
The model was evaluated on these different senses with *eval.py*. The results can be found in the folder *results_gpt-3.5-turbo*. 
The required command line arguments for running *eval.py* are the task specifiers (collection and subtask).
In addition, you can specify the input data language (e.g. "en" for English or "de_from_en" for the model's translation from English into German) and the instruction version (e.g. "de" for the original German instruction, or "de_from_en-translation" for the model's translation of the English instruction into German).
Further arguments that can be specified are temperature, top_p sampling, maximum number of output tokens.
We used a temperature of 0.25, a top_p probability of 1.0, and 256 output tokens for all our experiments. 

For details on how the model's responses are standardized, see *utils/response_standardization.py*; for details on the accuracy evaluation, see *utils/eval_metrics.py*.

**Examples**

To evaluate the model on the model's translation of paws-x into German (input data and instruction), as in our experiments, run: 

```
python eval.py --collection individual_tasks --subtask paws-x --languages de_from_en --instruction_version de_from_en-translation --temperature 0.25 --output_dir results_gpt-turbo-0301
```

To evaluate the model on the original English input data for XGLUE paired with the model's translation of the instruction from English to Chinese, as in our experiments, run: 


```
python eval.py --collection xglue --subtask xnli --languages en --instruction_version zh_from_en-translation --temperature 0.25 --output_dir results_gpt-turbo-0301
```

## Analysis
The analyses reported in the paper can be found in the notebooks *consistency_analysis.ipynb*, which analyses the model's consistency across different senses, and *performance_analysis.ipynb*, which analyses the model's accuracy and the quality of the translations. 
Helper functions (mainly for loading the results) can be found in *utils/analysis_helpers.py*.


## Contact

Please do not hesitate to reach out to xenia.ohmer@uni-osnabrueck.de if you have any questions. 