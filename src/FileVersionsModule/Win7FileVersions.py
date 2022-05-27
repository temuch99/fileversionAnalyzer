from src.FileVersionsModule.FileVersions import FileVersions

from git import Repo
from stat import ST_MTIME
from datetime import datetime
from zipfile import ZipFile

import os
import re
import shutil

class Win7FileVersions(FileVersions):
    def __init__(self, path, output_path):
        backup_path = os.path.join(path, 'PC')
        backups_folders = os.listdir(backup_path)

        self.path = os.path.join(backup_path, backups_folders[0])
        self.output_path = output_path
        self.branches = []

        if os.path.exists(self.output_path):
            # TODO throw exception
            print("ERROR")
            return

        if not os.path.exists(self.path):
            # TODO throw exception
            print("ERROR")

    def get_datetime(self, timeformat):
        file_date = datetime.strptime(timeformat, "Backup files %Y-%m-%d %H%M%S")
        return file_date.strftime("%Y-%m-%d %H:%M:%S")

    def create(self):
        self.init_repo()

        self.branches.append({
            "filename": "master",
            "branch": self.repo.create_head("master")
        })

        branch = [branch["branch"] for branch in self.branches if branch["filename"] == "master"][0]
        self.repo.head.reference = branch

        backups = [dir for dir in os.listdir(self.path) if re.match('Backup Files.*', dir)]
        for backup_dir in backups:
            if os.path.exists(os.path.join(self.output_path, 'backups')):
                old_files = os.listdir(os.path.join(self.output_path, 'backups'))
                if len(old_files) != 0:
                    for file in old_files:
                        os.remove(os.path.join(self.output_path, 'backups', file))
                        self.repo.index.remove([os.path.join('backups', file)])

            files = ZipFile(os.path.join(self.path, backup_dir, 'Backup files 1.zip'))
            files.extractall(path=os.path.join(self.output_path, 'backups'))
            extracted_files = [os.path.join('backups', file) for file in os.listdir(os.path.join(self.output_path, 'backups'))]
            self.repo.index.add(extracted_files)
            file_date = self.get_datetime(backup_dir)
            self.repo.index.commit(file_date, commit_date=file_date, author_date=file_date)