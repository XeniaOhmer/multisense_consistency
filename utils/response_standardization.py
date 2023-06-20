import re


def cut_double_quotes(old_datapoint):
    quotation_start = ["\"", "\'", "`", "“", "‘", "«"]
    quotation_end = ["\"", "\'", "´", "”", "’", "»"]

    new_datapoint = old_datapoint

    start_counts = 0
    end_counts = 0
    for elem in quotation_start:
        start_counts += old_datapoint.count(elem)
    for elem in quotation_end:
        end_counts += old_datapoint.count(elem)

    if end_counts > start_counts:
        if new_datapoint[-2:] == "\'\'" or new_datapoint[-2:] == "\´´":
            new_datapoint = new_datapoint[:-2]
        elif new_datapoint[-1] in quotation_end:
            new_datapoint = new_datapoint[:-1]

    if new_datapoint.count("\"") % 2 != 0 and new_datapoint[-1] == "\"":
        new_datapoint = new_datapoint[:-1]

    for i in range(4):
        if new_datapoint[0] == quotation_start[i] and new_datapoint[-1] == quotation_end[i]:
            new_datapoint = new_datapoint[1:-1]
            if new_datapoint[0] == quotation_start[i] and new_datapoint[-1] == quotation_end[i]:
                new_datapoint = new_datapoint[1:-1]

    return new_datapoint


def standardize_classification_response(responses, label_map):

    standardized = []
    possible_answers = list(label_map.keys())

    for r_idx, r in enumerate(responses):

        if r:
            r_stand = r.lower()
            r_stand = r_stand.strip(" ")
            r_stand = r_stand.strip("。")  # all Chinese answers are followed by this sign
            if "i cannot answer" in r_stand:
                print(r_idx, "Not the right format: ", r_stand)
                r_stand = -1
                print("1) Set to: -1")
            if r_stand != -1:
                r_stand = r_stand.replace("the correct answer is", "")
                r_stand = r_stand.replace("the answer is", "")
                r_stand = r_stand.replace("answer", "")
                r_stand = r_stand.replace("option", "")
                r_stand = r_stand.strip(" ")
                r_stand = r_stand.strip(":")
                r_stand = r_stand.strip(" ")
                r_stand = r_stand.strip(".")
                r_stand = r_stand.strip(" ")

            for answer in possible_answers:
                if r_stand and r_stand != -1:
                    if (
                            "\"" + answer + "\"" == r_stand or
                            "\'" + answer + "\'" == r_stand or
                            "(" + answer + ")" == r_stand or
                            "[" + answer + "]" == r_stand or
                            "“" + answer + "”" == r_stand or
                            "\"" + answer + ".\"" == r_stand or
                            "\'" + answer + ".\'" == r_stand or
                            "(" + answer + ".)" == r_stand or
                            "[" + answer + ".]" == r_stand or
                            "“" + answer + ".”" == r_stand or
                            answer + "。" == r_stand[0:len(answer) + 1] or
                            answer + "," == r_stand[0:len(answer) + 1] or
                            " " + answer + "。" == r_stand[0:len(answer) + 2] or
                            " " + answer + "." == r_stand[0:len(answer) + 2] or
                            answer + " " == r_stand[0:len(answer) + 1] or
                            answer + "-" == r_stand[0:len(answer) + 1]
                    ):
                        print(r_idx, "Not the right format: ", r_stand)
                        r_stand = answer
                        print("2) Set to: ", answer)
        else:
            print(r_idx, "empty string 1: ", r)
            r_stand = -1
            print("Set to: ", -1)

        if r_stand and r_stand != -1:

            if r_stand not in possible_answers:
                print(r_idx, "Not the right format: ", r_stand)
                flag = False  # mark whether mapping could be corrected

                counter = 0
                for answer in possible_answers:
                    if (
                            "\"" + answer + "\"" in r_stand or
                            "\'" + answer + "\'" in r_stand or
                            "(" + answer + ")" in r_stand or
                            "[" + answer + "]" in r_stand or
                            "“" + answer + "”" in r_stand or
                            "\"" + answer + ".\"" in r_stand or
                            "\'" + answer + ".\'" in r_stand or
                            "(" + answer + ".)" in r_stand or
                            "[" + answer + ".]" in r_stand or
                            "“" + answer + ".”" in r_stand or
                            ", " + answer + ".," in r_stand or
                            ",  " + answer + ".," in r_stand or
                            "\" " + answer + " \"" in r_stand or
                            "\' " + answer + " \'" in r_stand or
                            "( " + answer + " )" in r_stand or
                            "[ " + answer + " ]" in r_stand or
                            "“ " + answer + " ”" in r_stand or
                            ", " + answer + " ," in r_stand or
                            ",  " + answer + " ," in r_stand
                    ):
                        answer_temp = answer
                        counter += 1
                if counter == 1:
                    r_stand = answer_temp
                    print("3) Set to: ", answer_temp)
                    flag = True

                if not flag:
                    for answer in possible_answers:
                        if (
                                answer + "." == r_stand[0:len(answer)+1] or
                                answer + "," == r_stand[0:len(answer)+1] or
                                answer + ")" == r_stand[0:len(answer)+1] or
                                answer + "。" == r_stand[0:len(answer)+1] or
                                answer + ":" == r_stand[0:len(answer)+1] or
                                answer + "：" == r_stand[0:len(answer)+1] or
                                "\"" + answer + "\"" == r_stand[0:len(answer)+2] or
                                "\'" + answer + "\'" == r_stand[0:len(answer)+2]
                        ):
                            r_stand = answer
                            print("4) Set to: ", answer)
                            flag = True

                counter = 0
                if not flag:
                    for answer in possible_answers:
                        if (
                                ": " + answer in r_stand or
                                " " + answer + "." in r_stand or
                                " " + answer + " " in r_stand or
                                " " + answer + ":" in r_stand or
                                " " + answer + "," in r_stand
                        ):
                            answer_temp = answer
                            counter += 1
                    if counter == 1:
                        r_stand = answer_temp
                        print("5) Set to: ", answer_temp)
                        flag = True

                if not flag:
                    for answer in possible_answers:
                        if answer == r_stand[0:len(answer)]:
                            r_stand = answer
                            print("6) Set to: ", answer)
                            flag = True

                if not flag:
                    for answer in possible_answers:
                        if (
                                " " + answer == r_stand[-(len(answer) + 1):] or
                                " " + answer + "." == r_stand[-(len(answer) + 2):]
                        ):
                            r_stand = answer
                            print("7) Set to: ", answer)
                            flag = True

                if not flag:
                    if r_stand[0:2] == "不是" and "不是" not in possible_answers:
                        r_stand = "否"
                        flag = True
                        print("Chinese exception: wrong sign for \"no\"; set to 否")

                if not flag:
                    counter = 0
                    for answer in possible_answers:
                        if (
                                re.search("[\u4e00-\u9FFF]" + answer, r_stand) or
                                re.search("[\u4e00-\u9FFF] " + answer, r_stand)
                        ):
                            if r_stand[-1] == r_stand:
                                r_stand = answer
                                print("8) Set to: ", answer)
                                flag = True
                            if (
                                    answer + "，" in r_stand or
                                    answer + "," in r_stand or
                                    answer + "." in r_stand or
                                    answer + "。" in r_stand or
                                    answer + ":" in r_stand or
                                    answer + "：" in r_stand

                            ):
                                r_stand = answer
                                print("9) Set to: ", answer)
                                flag = True
                            elif answer == r_stand[-1]:
                                r_stand = answer
                                print("10) Set to: ", answer)
                                flag = True
                            else:
                                candidate = answer
                                counter += 1
                    if not flag and counter == 1:
                        if not re.search("[\u4e00-\u9FFF]", candidate):
                            r_stand = candidate
                            flag = True
                            print("11) Set to: ", candidate)

                if not flag:
                    r_stand = -1
                    print("Set to: -1")
        else:
            if not r_stand:
                print(r_idx, "empty string 2: ", r)
                r_stand = -1

        standardized.append(r_stand)
    return standardized
