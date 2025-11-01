import re
import os


class HandlerErrors:


    def check_url(self, url):

        if not isinstance(url, str):
            raise ValueError("Error: URL must be a string")
        if not url.startswith("https://"):
            raise ValueError("Error: URL must start with 'https://'")
        return url

    def check_name(self, name):

        if not isinstance(name, str):
            raise ValueError("Error: Package name must be a string")
        if len(name.strip()) == 0:
            raise ValueError("Error: Package name cannot be empty")
        return name

    def check_mode(self, mode):

        modes = ["remote", "local"]
        if mode not in modes:
            raise ValueError(f"Error: Mode must be one of {modes}")
        return mode

    def check_version(self, version):

        if not isinstance(version, str):
            raise ValueError("Error: Version must be a string")
        # Разрешаем любой формат версии или пустую строку
        if len(version.strip()) > 0:
            # Проверяем базовый формат версии
            pattern = r"^[\d\.\-\w]+$"
            if not re.match(pattern, version):
                raise ValueError("Error: Invalid version format")
        return version

    def check_graph_name(self, name):

        if not isinstance(name, str):
            raise ValueError("Error: Graph name must be a string")
        if len(name.strip()) == 0:
            raise ValueError("Error: Graph name cannot be empty")
        return name

    def check_max_deep(self, max_deep):

        try:
            max_deep_int = int(max_deep)
            if max_deep_int < 1 or max_deep_int > 25:
                raise ValueError("Error: Max depth must be between 1 and 25")
            return max_deep_int
        except (ValueError, TypeError):
            raise ValueError("Error: Max depth must be a valid integer")

    def check_substring_filter(self, substring):

        if not isinstance(substring, str):
            raise ValueError("Error: Substring filter must be a string")
        return substring

    def check_file_path(self, file_path):
        """Проверка пути к файлу для local режима"""
        if not isinstance(file_path, str):
            raise ValueError("Error: File path must be a string")
        if len(file_path.strip()) == 0:
            raise ValueError("Error: File path cannot be empty")
        # Проверяем, что файл существует
        import os
        if not os.path.isfile(file_path):
            raise ValueError(f"Error: File not found: {file_path}")
        return file_path
