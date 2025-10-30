import re

class HandlerErrors():

    def chack_url(self, url):
        if not url.startswith("https://"):
            raise ValueError("Error of url")
        return url

    def check_name(self, name):
        if name != "npm":
            raise ValueError("Error of name")
        return name

    def check_mode(self, mode):
        modes = ["remote", "local"]
        if mode not in modes:
            raise ValueError("Error of mode")
        return mode

    def check_version(self, version):
        pattern = r"[1-9]\.[0-9]\.[0-9]"
        if not re.match(pattern, version):
            raise ValueError("Error of version")
        return version

    def check_graph_name(self, name):
        if len(filter.strip()) == 0:
            raise ValueError("Error of filter")
        return name

    def check_max_deep(self, max):
        pattern = r"^(1?\d|2[0-5])$"
        if not re.match(pattern, max):
            raise ValueError("Error of max")
        return max

    def check_substring_filter(self, filter):
        if len(filter.strip()) < 0:
            raise ValueError("Error of filter")
        return filter
