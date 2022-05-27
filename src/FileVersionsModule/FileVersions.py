from __future__ import annotations
from git import Repo

import os

class FileVersions:
    def create(self):
        pass

    def init_repo(self):
        self.repo = Repo.init(self.output_path)
        keep_dir = os.path.join(self.output_path, 'keep')
        os.mkdir(keep_dir)
        self.repo.index.add(['keep'])
        self.repo.index.commit('init')