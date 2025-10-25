import os.path
import re

class Get_options():
    def __init__(self, option):
        self.__option = option
        __list_option = option.split()
        do = self.create_dict(__list_option)
    def output(self, arg):
        if type(arg) == list:
            for i in arg:
                print(i)
            return
        elif type(arg) == dict:
            for k, v in arg.items():
                print(f"{k} : {v}")
            return
        elif type(arg) == str:
            print(arg)
            return
    def create_dict(self, len_str: list):
        __dict_option = {}
        if len_str[0] == "apk":
            __dict_option["name"] = len_str[0]
        if len_str[0] != "apk":
            print("Error of analyzing")
        if len_str[1].startswith("https://"):
            __dict_option["url"] = len_str[1]
        elif not (len_str[1].startswith("http://")):
            print("Error of url")
        if len_str[2] == "local" or len_str[2] == "remote":
            __dict_option["mode"] = len_str[2]
        elif len_str[2] != "remote" or len_str[2] != "local":
             print("Error of mode")
        if len_str[3] == r"^[^.]*\.[^.]*\.[^.]*$":
            __dict_option["version"] = len_str[3]
        elif len_str[3] == r"^[^.]*\.[^.]*\.[^.]*$":
            print("Error of creating version")
        if len_str[4] == os.path.isfile(len_str[4]):
            __dict_option["name generated file"] = len_str[4]
        elif len_str[4] != os.path.isfile(len_str[4]):
            print("Error of creating file")
        if int(len_str[5]) >= 0:
            __dict_option["max deep"] = len_str[5]
        elif int(len_str[5]) < 0:
            print("Error of max deep")
        if len(len_str[6]) >= 0:
            __dict_option["substring for filter"] = len_str[6]
        elif len(len_str[6]) < 0:
            print("Error of substring for filter")
        else:
            print("Other error")
        return __dict_option