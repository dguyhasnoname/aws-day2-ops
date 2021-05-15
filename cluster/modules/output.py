from columnar import columnar
from click import style
from packaging import version
import os, re, time, requests, json
#from .logging import Logger

class Output:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    CYAN = '\033[36m'
    RESET = '\033[0m'
    BOLD = '\033[1;30m'
    # u'\u2717' means values is None or not defined
    # u'\u2714' means value is defined

    global patterns, _logger
    
    patterns = [(u'\u2714', lambda text: style(text, fg='green')), \
                ('True', lambda text: style(text, fg='green')), \
                ('False', lambda text: style(text, fg='yellow'))]

    def time_taken(start_time):
        print(Output.GREEN + "\nTotal time taken: " + Output.RESET + \
        "{}s".format(round((time.time() - start_time), 2)))

    # prints separator line between output
    def separator(color, char, l):
        if l: return
        columns, rows = os.get_terminal_size(0)
        for i in range(columns):
            print (color + char, end="" + Output.RESET)
        print ("\n")

    # sorts data by given field
    def sort_data(data, field):
        try:
            if field:
                data.sort(key=lambda x: x[int(field)])
            else:
                data.sort(key=lambda x: x[0])
        except AttributeError:
            print("Empty data received!")
            exit()
        return data


    # prints table from lists of lists: data
    def print_table(data, headers, verbose):
        try:
            if verbose and len(data) != 0:
                table = columnar(data, headers, no_borders=True, row_sep='-')
                print (table)
        except:
            print("Empty/Incorrect data received!")
            exit()

    def print_tree(data, headers):
        h = sorted(headers[1:], key=len)
        for d in data:
            heading = headers[0] + ": " + d[0]
            Output.separator(Output.YELLOW, '.' , '')
            print(heading)
            for i in range(len(headers)):
                try:
                    #https://www.compart.com/en/unicode/mirrored
                    if not '\n' in d[i+1]:
                        print("".ljust(len(heading)) + u"\u2309\u169B\u22B8" + headers[i+1].ljust(len(h[-1])) + ": " + str(d[i+1]))
                    else:
                        padding = "".ljust(len(heading)) + u"\u2309\u169B\u22B8" + headers[i+1]
                        print(padding)
                        for x in d[i+1].split("\n"):
                            print("".ljust(len(padding)) + u"\u2309\u169B\u22B8" + str(x))                     
                    # print("".ljust(len(heading)) + u"\u2309\u169B\u22B8" + headers[i+1].ljust(len(h[-1])) + ": " + str(d[i+1]))
                except:
                    pass

    # prints analysis in bar format with %age, count and message
    def print_json(i, data, headers):
        # for i in range(len(headers)):
        #     for d in data:
        #         if not '\n' in d[i]:
        #             for x in d[i].split("\n"):
        #                 sub_key_json.append(x)
        #             json_obj.update({headers[i].lower(): sub_key_json})
        #         else:
        #             json_obj.update({headers[i].lower(): d[i]})
        
        json_data = []
        headers = [x.lower() for x in headers]
        for item in data:
            temp_dic = {}
            # storing json data in dict for each list in data
            for i in range(len(headers)):
                for j in range(len(item)):
                    if not '\n' in item[i]:
                        temp_dic.update({headers[i]: item[i]})
                    else:
                        item[i].split("\n")
                        temp_dic.update({headers[i]: item[i].split("\n")})

            # appending all json dicts to form a list
            json_data.append(temp_dic)
     
        print(json.dumps(json_data))
        return json.dumps(json_data)