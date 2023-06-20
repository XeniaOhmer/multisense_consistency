

task_config = {

    "super_glue": {
        "boolq": {
            "task_type": "classification",
            "column_names": ("question", "passage", "idx", "label"),
            "sentence_keys": ("passage", "question"),
            "n_labels": 2,
            "multilingual": False,
            "metric": "accuracy",
            "languages": ["en"],
            "label_map": {
                "en": {"no": 0, "yes": 1},
                "fr": {"non": 0, "oui": 1},
                "es": {"sí": 1, "no": 0},
                "de_from_en-translation": {"nein": 0, "ja": 1},
                "zh_from_en-translation": {"不是": 0, "是": 1}
            },
            "prefix": {
                "en": "",
                "de": "",
                "zh": "",
                "es": "",
                "fr": "",
                "de_from_en-translation": "",
                "zh_from_en-translation": "",
                "fr_from_en-translation": "",
                "es_from_en-translation": "",
                "en_from_de-translation": "",
                "en_from_zh-translation": "",
                "en_from_es-translation": "",
                "en_from_fr-translation": "",
            },
            "suffix": {
                "en": " Please answer with \"yes\" or \"no\".",
                "de": " Bitte antworte mit \"ja\" oder \"nein\".",
                "zh": " 请用“是”或者“否”回答。",
                "es": " Por favor responda con \"sí\" o \"no\".",
                "fr": " Veuillez répondre par \"oui\" ou \"non\".",
                "de_from_en-translation": " Bitte antworten Sie mit \"Ja\" oder \"Nein\".",
                "zh_from_en-translation": " 请用“是”或“不是”回答。",
                "en_from_de-translation": " Please respond with \'yes\' or \'no\'.",
                "en_from_zh-translation": " Please answer with \'yes\' or \'no\'."
            },
        }
    },

    "xglue": {
        "xnli": {
            "task_type": "classification",
            "column_names": ("premise", "hypothesis", "label"),
            "sentence_keys": ("premise", "hypothesis"),
            "n_labels": 3,
            "multilingual": True,
            "languages": ["ar", "bg", "de", "el", "en", "es", "fr", "hi", "ru", "sw", "th", "tr", "ur", "vi", "zh"],
            "metric": "accuracy",
            "label_map": {"en": {"a": 0, "b": 2, "c": 1},
                          "de": {"a": 0, "b": 2, "c": 1},
                          "zh": {"a": 0, "b": 2, "c": 1},
                          "fr": {"a": 0, "b": 2, "c": 1},
                          "es": {"a": 0, "b": 2, "c": 1},
                          "de_test1": {"a": 0, "b": 2, "c": 1},
                          "de_test2": {"a": 0, "b": 2, "c": 1},
                          "de_test3": {"a": 0, "b": 2, "c": 1},
                          "de_test4": {"a": 0, "b": 2, "c": 1},
                          "de_test5": {"a": 0, "b": 2, "c": 1},
                          "en_from_de-translation": {"a": 0, "b": 2, "c": 1},
                          "en_from_zh-translation": {"a": 0, "b": 2, "c": 1},
                          "en_from_es-translation": {"a": 0, "b": 2, "c": 1},
                          "en_from_fr-translation": {"a": 0, "b": 2, "c": 1},
                          "de_from_en-translation": {"a": 0, "b": 2, "c": 1},
                          "zh_from_en-translation": {"a": 0, "b": 2, "c": 1}},
            "prefix": {"en": "Given the following sentence pair, which one of the following is true: (A) the first "
                             "sentence entails the second sentence, (B) the first sentence contradicts the second "
                             "sentence, or (C) neither of the two?",
                       "de": "Welche dieser Aussagen trifft auf das folgende Satzpaar zu: (A) der erste Satz "
                             "impliziert den zweiten Satz, (B) der erste Satz widerspricht dem zweiten Satz, oder (C) "
                             "keines von beiden?",
                       "es": "Dado el siguiente par de oraciones, ¿cuál de las siguientes afirmaciones es verdadera?: " 
                             "(A) la primera oración implica la segunda oración, (B) la primera oración contradice "
                             "la segunda oración, (C) ninguna de las dos.",
                       "fr": "Étant donné la paire de phrases suivante, laquelle des propositions suivantes est vraie: "
                             "(A) la première phrase implique la seconde phrase, (B) la première phrase contredit la "
                             "seconde phrase, ou (C) aucune des deux?",
                       # Alternative German instructions to test if performance in German is so bad because of
                       # our choice of instruction
                        "de_test1": "Welche dieser Aussagen trifft auf das danach folgende Satzpaar zu: (A) der erste "
                                    "Satz impliziert den zweiten Satz, (B) der erste Satz widerspricht dem zweiten "
                                    "Satz, oder (C) keines von beiden?",
                       "de_test2": "Welche dieser Aussagen ist für das folgende Satzpaar wahr: (A) der erste "
                                   "Satz impliziert den zweiten Satz, (B) der erste Satz widerspricht dem zweiten "
                                   "Satz, oder (C) keines von beiden?",
                       "de_test3": "Gegeben das folgende Satzpaar, welche dieser Aussagen ist wahr: (A) der erste "
                                   "Satz impliziert den zweiten Satz, (B) der erste Satz widerspricht dem zweiten "
                                   "Satz, oder (C) keines von beiden?",
                       "de_test4": "Welche dieser Aussagen trifft auf das folgende Satzpaar zu: (A) Der erste Satz "
                                   "impliziert den zweiten Satz, (B) Der erste Satz widerspricht dem zweiten Satz, "
                                   "oder (C) Keines von beiden?",
                       "de_test5": "Welche dieser Aussagen trifft auf das danach folgende Satzpaar zu: (A) Der zweite "
                                    "Satz folgt aus dem ersten Satz, (B) Der erste Satz widerspricht dem zweiten "
                                    "Satz, oder (C) keines von beiden?",
                       "zh": "对于给出的一对句子，以下哪一个选项是正确的：（A）第一个句子涵盖了第二个句子 "
                             "（B）第一个句子与第二个句子矛盾 （C）两者都不？",
                       "en_from_de-translation": "Which of these statements applies to the following pair of "
                                                 "sentences: (A) the first sentence implies the second sentence, "
                                                 "(B) the first sentence contradicts the second sentence, or (C) "
                                                 "neither of the above?",
                       "en_from_zh-translation": "For a given pair of sentences, which of the following options is "
                                                 "correct: (A) The first sentence covers the second sentence. "
                                                 "(B) The first sentence contradicts the second sentence. (C) "
                                                 "Neither of them?",
                       "en_from_es-translation": "Given the following pair of sentences, which of the following "
                                                 "statements is true?: (A) the first sentence implies the second "
                                                 "sentence, (B) the first sentence contradicts the second sentence, "
                                                 "(C) neither of them.",
                       "en_from_fr-translation": "Given the following pair of sentences, which of the following "
                                                 "propositions is true: (A) the first sentence implies the second "
                                                 "sentence, (B) the first sentence contradicts the second sentence, "
                                                 "or (C) neither of the two?",
                       "de_from_en-translation": "Angesichts des folgenden Satzpaares, welche der folgenden Aussagen "
                                                 "ist wahr: (A) Der erste Satz impliziert den zweiten Satz, (B) Der "
                                                 "erste Satz widerspricht dem zweiten Satz oder (C) Keines von beiden?",
                       "zh_from_en-translation": "给定以下句子对，哪一个是正确的：（A）第一句蕴含第二句，"
                                                 "（B）第一句与第二句相矛盾，还是（C）两者都不是？"
                       },
            "suffix": {"en": " Please answer with \"A\", \"B\", or \"C\".",
                       "de": " Bitte antworte mit \"A\", \"B\" oder \"C\".",
                       "zh": " 请用“A”、“B”或“C”来回答。",
                       "fr": " Veuillez répondre par \"A\", \"B\" ou \"C\".",
                       "es": " Por favor responda con \"A\", \"B\" o \"C\".",
                       "de_test1": " Bitte antworte mit \"A\", \"B\" oder \"C\".",
                       "de_test2": " Bitte antworte mit \"A\", \"B\" oder \"C\".",
                       "de_test3": " Bitte antworte mit \"A\", \"B\" oder \"C\".",
                       "de_test4": " Bitte antworte mit \"A\", \"B\" oder \"C\".",
                       "de_test5": " Bitte antworte mit \"A\", \"B\" oder \"C\".",
                       "en_from_de-translation": " Please reply with \"A\", \"B\", or \"C\".",
                       "en_from_zh-translation": " Please answer with \"A\", \"B\", or \"C\".",
                       "en_from_es-translation": " Please respond with \"A\", \"B\", or \"C\".",
                       "en_from_fr-translation": " Please respond with \"A\", \"B\", or \"C\".",
                       "de_from_en-translation": " Bitte antworten Sie mit \"A\", \"B\" oder \"C\".",
                       "zh_from_en-translation": " 请用\"A\"、\"B\"或\"C\"回答。"}
        },
    },

    "individual_tasks": {

        "paws-x": {
            "task_type": "classification",
            "column_names": ("id", "sentence1", "sentence2", "label"),
            "sentence_keys": ("sentence1", "sentence2"),
            "n_labels": 2,
            "multilingual": True,
            "metric": "accuracy",
            "languages": ["de", "en", "es", "fr", "ja", "ko", "zh"],
            "label_map": {
                "en": {"no": 0, "yes": 1},
                "de": {"nein": 0, "ja": 1},
                "zh": {"否": 0, "是": 1},
                "fr": {"non": 0, "oui": 1},
                "es": {"no": 0, "sí": 1},
                "en_from_de-translation": {"no": 0, "yes": 1},
                "en_from_zh-translation": {"no": 0, "yes": 1},
                "en_from_es-translation": {"no": 0, "yes": 1},
                "en_from_fr-translation": {"no": 0, "yes": 1},
                "de_from_en-translation": {"nein": 0, "ja": 1},
                "zh_from_en-translation": {"不是": 0, "是": 1}
            },
            "prefix": {
                "en": "Do the following sentences have the same meaning?",
                "de": "Haben die folgenden Sätze die gleiche Bedeutung?",
                "zh": "下面的句子有着相同的含义吗？",
                "fr": "Les phrases suivantes ont-elles la même signification?",
                "es": "¿Tienen las siguientes oraciones el mismo significado?",
                "de_from_en-translation": "Haben die folgenden Sätze die gleiche Bedeutung?",
                "zh_from_en-translation": "以下句子的意思相同吗？",
                "en_from_de-translation": "Do the following sentences have the same meaning?",
                "en_from_zh-translation": "Does the following sentence have the same meaning?",
                "en_from_es-translation": "Do the following sentences have the same meaning?",
                "en_from_fr-translation": "Do the following sentences have the same meaning?"
            },
            "suffix": {
                "en": " Please answer with \"yes\" or \"no\".",
                "de": " Bitte antworte mit \"ja\" oder \"nein\".",
                "zh": " 请用“是”或者“否”回答。",
                "fr": " Veuillez répondre par \"oui\" ou \"non\".",
                "es": " Por favor responda con \"sí\" o \"no\".",
                "de_from_en-translation": " Bitte antworten Sie mit \"Ja\" oder \"Nein\".",
                "zh_from_en-translation": " 请用“是”或“不是”回答。",
                "en_from_de-translation": " Please respond with \'yes\' or \'no\'.",
                "en_from_zh-translation": " Please answer with \'yes\' or \'no\'.",
                "en_from_es-translation": " Please respond with \'yes\' or \'no\'.",
                "en_from_fr-translation": " Please respond with \"yes\" or \"no\"."
            },
        }
    }
}
