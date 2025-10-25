import argparse
import sys

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


    def command_line(self):
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
