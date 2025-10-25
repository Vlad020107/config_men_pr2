import argparse
import sys
from operator import index

import requests
import json

from HandlerErrors import HandlerErrors


class CLI_JS:

    # 1 этап
    def __init__(self):
        self.params = self.command_line()
        self.print_params()

    def print_params(self):
        print(f'Имя пакета: {self.params["package_name"]}')
        print(f'Url: {self.params["repo-url"]}')
        print(f'Режим работы: {self.params["mode"]}')
        print(f'Версия: {self.params["version"]}')
        print(f'Имя файла: {self.params["graph_name"]}')
        print(f'Максимальная глубина: {self.params["max-deep"]}')
        print(f'Подстрока: {self.params["substring_name"]}')

    def create_json(self, url):
        url_content = url.text
        content = json.loads(url_content)
        return (content)

    def info_npm(self, info_package:dict, jv):
        info_package["package_name"] = ("npm")
        info_package["url"] = ("https://registry.npmjs.org/react/18.2.0")
        info_package["mode"] = ("remote")
        info_package["version"] = (jv["version"])
        info_package["max-deep"] = self.search_max_deep(jv)
        print(info_package)

    def search_max_deep(self, jv:dict, current_deep=0):
        for k, v in jv.items():
            if type(v) == dict:
                current_deep+=1
                self.search_max_deep(v, current_deep)
        return current_deep

    def all_info(self, jv:dict):
            print(jv)

    def command_line(self):
        name = "react/18.2.0"
        npm_package = f"https://registry.npmjs.org/{name}"
        url = requests.get(npm_package)
        jv = self.create_json(url)
        info_package = {"package_name":"", "url":"", "mode":"", "version":"", "max-deep":"", "substring_name":""}
        self.info_npm(info_package, jv)
        self.all_info(jv)

        he = HandlerErrors()
        params = {}
        parser = argparse.ArgumentParser(
            description="JavaScript 2.0 CLI",
        )

        argv_list = [argv for argv in sys.argv]
        print(argv_list)

        parser.add_argument("--package_name",
                            "-p",
                            type=he.check_name,
                            required=True,
                            help="JavaScript package name")

        parser.add_argument("--repo_url",
                            "-u",
                            type=he.chack_url,
                            required=True,
                            help="JavaScript package name")

        parser.add_argument("--mode",
                            "-m",
                            type=he.check_mode,
                            default="dev",
                            help="JavaScript package name")

        parser.add_argument("--version",
                            "-v",
                            type=he.check_version,
                            default='1.0.0',
                            help="JavaScript package name")

        parser.add_argument("--graph_name",
                            "-g",
                            type=he.check_graph_name,
                            default="graph.png",
                            help="JavaScript package name")

        parser.add_argument("--max_deep",
                            "-md",
                            type=he.check_max_deep,
                            default=3,
                            help="JavaScript package name")
        parser.add_argument("--substring_name",
                            "-s",
                            type=he.check_substring_filter,
                            default="",
                            help="JavaScript package name")
        args = parser.parse_args()
        params.setdefault("package_name", args.package_name)
        params.setdefault("repo-url", args.repo_url)
        params.setdefault("mode", args.mode)
        params.setdefault("version", args.version)
        params.setdefault("graph_name", args.graph_name)
        params.setdefault("max-deep", args.max_deep)
        params.setdefault("substring_name", args.substring_name)
        return params


if __name__ == '__main__':
    cli = CLI_JS()
