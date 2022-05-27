import os
import re
import shutil

from zipfile import ZipFile
from zipfile import ZIP_DEFLATED
from stat import ST_MTIME
from src.BackupVersionsModule.BackupVersions import BackupVersions

class MacBackupVersions(BackupVersions):
    def get(self, output_path):
        shutil.rmtree("tmp/extracted", ignore_errors=True)
        os.mkdir("tmp/extracted")
        user_folders = os.listdir(self.path + '/root/.DocumentRevisions-V100/PerUID')
        for user_folder in user_folders:
            backup_files = os.listdir(self.path + '/root/.DocumentRevisions-V100/PerUID/' + user_folder)
            for backup_file in backup_files:
                # TODO: подумать как получить название файла
                path = self.path + '/root/.DocumentRevisions-V100/PerUID/' + user_folder + '/' + backup_file
                os.mkdir('tmp/extracted/' + backup_file)
                dir_path = path + '/com.apple.documentVersions/'
                entries  = (os.path.join(dir_path, file) for file in os.listdir(dir_path))
                entries  = ((os.stat(path), path) for path in entries)
                entries  = ((stat[ST_MTIME], path) for stat, path in entries)
                for entry in entries:
                    shutil.copyfile(entry[1], 'tmp/extracted/' + backup_file + '/' + str (entry[0]))

        with ZipFile(output_path + '/backup.zip', mode='w', compression=ZIP_DEFLATED) as zf:
            for folder in os.listdir('tmp/extracted/'):
                for file in os.listdir('tmp/extracted/' + folder):
                    path = folder + '/' + file
                    zf.write('tmp/extracted/' + folder + '/' + file, arcname=path)
        shutil.rmtree("tmp/extracted")