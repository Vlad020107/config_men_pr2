import argparse
import sys
import requests
import json
from HandlerErrors import HandlerErrors


class CLI_JS:


    def __init__(self):
        self.params = self.command_line()
        self.print_params()


        if self.params["mode"] == "remote":
            self.process_remote_mode()
        elif self.params["mode"] == "local":
            self.process_local_mode()

    def print_params(self):

        print("\n=== Параметры конфигурации ===")
        print(f'Имя пакета: {self.params["package_name"]}')
        print(f'URL: {self.params["repo_url"]}')
        print(f'Режим работы: {self.params["mode"]}')
        print(f'Версия: {self.params["version"]}')
        print(f'Имя файла: {self.params["graph_name"]}')
        print(f'Максимальная глубина: {self.params["max_deep"]}')
        print(f'Подстрока фильтра: {self.params["substring_name"]}')
        print("=" * 32)

    def command_line(self):

        he = HandlerErrors()
        parser = argparse.ArgumentParser(
            description="Инструмент визуализации графа зависимостей npm пакетов",
        )

        parser.add_argument("--package_name",
                           "-p",
                           type=he.check_name,
                           required=True,
                           help="Имя анализируемого пакета")

        parser.add_argument("--mode",
                           "-m",
                           type=he.check_mode,
                           default="remote",
                           help="Режим работы: 'remote' или 'local'")

        parser.add_argument("--repo_url",
                           "-u",
                           required=True,
                           help="URL репозитория или путь к файлу тестового репозитория")

        parser.add_argument("--version",
                           "-v",
                           type=he.check_version,
                           default="latest",
                           help="Версия пакета")

        parser.add_argument("--graph_name",
                           "-g",
                           type=he.check_graph_name,
                           default="graph.png",
                           help="Имя сгенерированного файла с изображением графа")

        parser.add_argument("--max_deep",
                           "-md",
                           type=he.check_max_deep,
                           default=3,
                           help="Максимальная глубина анализа зависимостей (1-25)")

        parser.add_argument("--substring_name",
                           "-s",
                           type=he.check_substring_filter,
                           default="",
                           help="Подстрока для фильтрации пакетов")

        args = parser.parse_args()


        if args.mode == "local":

            he.check_file_path(args.repo_url)
        else:

            he.check_url(args.repo_url)
        
        params = {
            "package_name": args.package_name,
            "repo_url": args.repo_url,
            "mode": args.mode,
            "version": args.version,
            "graph_name": args.graph_name,
            "max_deep": args.max_deep,
            "substring_name": args.substring_name
        }
        
        return params

    def get_npm_package_info(self, package_name, version):

        url = f"https://registry.npmjs.org/{package_name}"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error: Failed to fetch package info: {e}")

    def extract_direct_dependencies(self, package_info, version=None):

        version_data = None


        target_version = version
        if not target_version or target_version == "latest":

            target_version = package_info.get("dist-tags", {}).get("latest")
        
        if not target_version:
            return {}


        if "versions" not in package_info:
            return {}
        
        versions_dict = package_info["versions"]


        if target_version in versions_dict:
            version_data = versions_dict[target_version]
        else:

            for v in versions_dict.keys():

                v_clean = v.lstrip('v').strip()
                target_clean = str(target_version).lstrip('v').strip()
                if v_clean == target_clean:
                    version_data = versions_dict[v]
                    break


            if not version_data:
                latest_version = package_info.get("dist-tags", {}).get("latest")
                if latest_version and latest_version in versions_dict:
                    version_data = versions_dict[latest_version]
        
        if not version_data:
            return {}


        dependencies = {}
        if "dependencies" in version_data:
            dependencies.update(version_data["dependencies"])
        if "peerDependencies" in version_data:
            dependencies.update(version_data["peerDependencies"])
        if "optionalDependencies" in version_data:
            dependencies.update(version_data["optionalDependencies"])

        return dependencies

    def process_remote_mode(self):

        package_name = self.params["package_name"]
        version = self.params["version"]
        repo_url = self.params["repo_url"]


        base_url = repo_url.rstrip('/')
        
        print(f"\n=== Получение информации о пакете {package_name} версии {version} ===")
        
        package_info = self.get_npm_package_info(package_name, version)
        direct_deps = self.extract_direct_dependencies(package_info, version)
        
        print(f"\nПрямые зависимости пакета {package_name}:")
        if direct_deps:
            for dep_name, dep_version in direct_deps.items():
                print(f"  - {dep_name}: {dep_version}")
        else:
            print("  Зависимостей не найдено")


        print(f"\n=== Построение графа зависимостей ===")
        graph = self.dfs_build_graph(
            package=package_name,
            version=version,
            max_depth=self.params["max_deep"],
            substring_filter=self.params["substring_name"],
            mode="remote",
            base_url=base_url
        )
        
        print(f"\nГраф зависимостей (пакеты: {len(graph)}):")
        for pkg, deps in graph.items():
            if deps:
                print(f"  {pkg} -> {', '.join(deps)}")

    def parse_test_repo(self, repo_path):

        try:
            with open(repo_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            deps_dict = {}
            lines = content.split('\n')
            
            for line in lines:
                line = line.strip()
                if not line or ':' not in line:
                    continue
                
                parts = line.split(':', 1)
                if len(parts) == 2:
                    package = parts[0].strip()
                    deps_str = parts[1].strip()
                    
                    if deps_str:
                        deps = [d.strip() for d in deps_str.split(',')]
                        deps_dict[package] = deps
                    else:
                        deps_dict[package] = []
            
            return deps_dict
        except FileNotFoundError:
            raise ValueError(f"Error: Test repository file not found: {repo_path}")
        except Exception as e:
            raise ValueError(f"Error: Failed to parse test repository: {e}")

    def process_local_mode(self):

        repo_path = self.params["repo_url"]
        package_name = self.params["package_name"]
        
        print(f"\n=== Загрузка тестового репозитория из {repo_path} ===")
        
        deps_dict = self.parse_test_repo(repo_path)
        
        print(f"\nЗагруженные пакеты из тестового репозитория:")
        for pkg, deps in deps_dict.items():
            if deps:
                print(f"  {pkg}: {', '.join(deps)}")
            else:
                print(f"  {pkg}: (нет зависимостей)")
        
        if package_name not in deps_dict:
            print(f"\nWarning: Пакет {package_name} не найден в тестовом репозитории")
            print(f"Доступные пакеты: {', '.join(deps_dict.keys())}")


        print(f"\n=== Построение графа зависимостей ===")
        graph = self.dfs_build_graph(
            package=package_name,
            version=None,
            max_depth=self.params["max_deep"],
            substring_filter=self.params["substring_name"],
            mode="local",
            deps_dict=deps_dict
        )
        
        print(f"\nГраф зависимостей (пакеты: {len(graph)}):")
        for pkg, deps in graph.items():
            if deps:
                print(f"  {pkg} -> {', '.join(deps)}")

    def get_package_dependencies(self, package_name, package_version, mode, base_url=None, deps_dict=None):

        if mode == "local":
            if deps_dict and package_name in deps_dict:
                return deps_dict[package_name]
            return []
        else:  # remote
            try:

                version_to_use = package_version if package_version and package_version != "latest" else "latest"
                package_info = self.get_npm_package_info(package_name, version_to_use)
                direct_deps = self.extract_direct_dependencies(package_info, version_to_use)
                return list(direct_deps.keys())
            except Exception as e:
                print(f"Warning: Не удалось получить зависимости для {package_name}: {e}")
                return []

    def dfs_build_graph(self, package, version=None, max_depth=3, substring_filter="", mode="remote", base_url=None, deps_dict=None):
        graph = {}
        visited = set()
        processing = set()
        stack = [(package, version, 0)]
        
        while stack:
            current_pkg, current_version, depth = stack.pop()


            if depth > max_depth:
                continue


            if substring_filter and substring_filter in current_pkg:
                continue


            if current_pkg in processing:
                print(f"Warning: Обнаружена циклическая зависимость для {current_pkg}")
                if current_pkg not in graph:
                    graph[current_pkg] = []
                continue


            if current_pkg in visited:

                if current_pkg not in graph:
                    graph[current_pkg] = []
                continue


            deps = self.get_package_dependencies(
                current_pkg, 
                current_version, 
                mode, 
                base_url, 
                deps_dict
            )


            filtered_deps = [dep for dep in deps if not (substring_filter and substring_filter in dep)]


            graph[current_pkg] = filtered_deps


            processing.add(current_pkg)
            visited.add(current_pkg)


            for dep in reversed(filtered_deps):
                if dep not in visited or depth + 1 <= max_depth:
                    stack.append((dep, None, depth + 1))


            processing.discard(current_pkg)
        
        return graph


if __name__ == '__main__':
    try:
        cli = CLI_JS()
    except ValueError as e:
        print(f"\nОшибка валидации: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nПрервано пользователем", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nНеожиданная ошибка: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
