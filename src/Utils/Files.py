from __future__ import annotations

import os

class Files:
    @staticmethod
    def get_files(path) -> list:
        files = []
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = "{}/{}".format(dirpath, filename)
                if filepath not in files:
                    files.append(filepath)
        return files