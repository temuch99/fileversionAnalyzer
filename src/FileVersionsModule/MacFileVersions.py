from src.FileVersionsModule.FileVersions import FileVersions

from git import Repo
from stat import ST_MTIME
from datetime import datetime

import os
import shutil

class MacFileVersions(FileVersions):
    def __init__(self, path, output_path):
        uid_folders_path = os.path.join(path, "root", ".DocumentRevisions-V100", "PerUID")
        uid_folders = os.listdir(uid_folders_path)
        # TODO для конкретного пользователя желательно сделать
        self.path = os.path.join(uid_folders_path, uid_folders[0])
        self.output_path = output_path
        self.branches = []

        if os.path.exists(self.output_path):
            # TODO throw exception
            print("ERROR")
            return

        if not os.path.exists(self.path):
            # TODO throw exception
            print("ERROR")

    def create(self):
        self.init_repo()

        file_ids = os.listdir(self.path)
        for file_id in file_ids:
            filename = self.get_filename(file_id)
            self.branches.append({
                "filename": filename,
                "branch": self.repo.create_head(filename)
            })

        for file_id in file_ids:
            self.append_file_versions(file_id)
        

    def get_filename(self, file_id):
        # TODO поправить
        return file_id

    def append_file_versions(self, file_id):
        filename = self.get_filename(file_id)

        branch = [branch["branch"] for branch in self.branches if branch["filename"] == filename][0]
        self.repo.head.reference = branch

        dir_path = os.path.join(self.path, file_id, 'com.apple.documentVersions')
        entries  = (os.path.join(dir_path, file) for file in os.listdir(dir_path))
        entries  = ((os.stat(path), path) for path in entries)
        entries  = ((stat[ST_MTIME], path) for stat, path in entries)

        index = 1

        for file_version in entries:
            file = os.path.join(self.output_path, "file")

            if os.path.exists(file):
                os.remove(file)

            shutil.copyfile(file_version[1], file)
            file_date = datetime.fromtimestamp(int(file_version[0]))
            formatted_file_date = file_date.strftime("%Y-%m-%d %H:%M:%S")
            self.repo.index.add(["file"])
            self.repo.index.commit(str(index), commit_date=formatted_file_date, author_date=formatted_file_date)
            index += 1
