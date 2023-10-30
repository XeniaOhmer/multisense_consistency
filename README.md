# multisense_consistency

This repository accompanies the publication:

Xenia Ohmer, Elia Bruni, and Dieuwke Hupkes. "Separating form and meaning: Using self-consistency to quantify task understanding across multiple senses". Proceedings of the 3rd Workshop on Natural Language Generation, Evaluation, and Metrics (GEM). Association for Computational Linguistics.

The different senses (here: translations) of the tasks were generated with *translate.py*. The translations can be found in the folder *translations_gpt-3.5-turbo*.

The model was evaluated on these different senses with *eval.py*. The results can be found in the folder *results_gpt-3.5-turbo*. 

The analyses reported in the paper can be found in the notebooks *consistency_analysis.ipynb*, which analyses the model's consistency across different senses, and *performance_analysis.ipynb*, which analyses the model's accuracy and the quality of the translations. 
