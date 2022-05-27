from zipfile import ZipFile
from zipfile import ZIP_DEFLATED
import shutil
import os
import re
from src.BackupVersionsModule.BackupVersions import BackupVersions
from datetime import datetime

class Windows7BackupVersions(BackupVersions):
	def get(self, output_path):
		shutil.rmtree("tmp/extracted", ignore_errors=True)
		shutil.rmtree("tmp/archive_extracted", ignore_errors=True)
		folders        = os.listdir(self.path + '/PC/')
		folder         = list(filter(lambda x: re.match('Backup*', x), folders))[0]
		folders        = os.listdir(self.path + '/PC/' + folder)
		backup_folders = list(filter(lambda x: re.match('Backup*', x), folders))
		for backup_folder in backup_folders:
			files    = ZipFile(self.path + '/PC/' + folder + '/' + backup_folder + '/Backup files 1.zip')
			tmp_path = 'tmp/extracted/' + re.findall('Backup Files ([0-9-\s]+)', backup_folder)[0]
			files.extractall(path=tmp_path)

		for filenames in os.walk('tmp/extracted'):
			for filename in filenames[2]:
				if re.search('desktop.ini', filename):
					os.remove(filenames[0] + "/" + filename)

		os.mkdir("tmp/archive_extracted")
		folders  = os.listdir("tmp/extracted")
		for folder in folders:
			files = os.listdir("tmp/extracted/" + folder)
			for file in files:
				if os.path.exists("tmp/archive_extracted/" + file):
					continue
				os.mkdir("tmp/archive_extracted/" + file)

		for folder in folders:
			files = os.listdir("tmp/extracted/" + folder)
			for file in files:
				# TODO Нужно будет поменять на timestamp
				shutil.copy("tmp/extracted/" + folder + "/" + file, "tmp/archive_extracted/" + file + "/" + folder)

		with ZipFile(output_path + '/backup.zip', mode='w', compression=ZIP_DEFLATED) as zf:
			for folder in os.listdir('tmp/archive_extracted/'):
				for file in os.listdir('tmp/archive_extracted/' + folder):
					path = folder + '/' + str(int(datetime.strptime(file, "%Y-%m-%d %H%M%S").timestamp()))
					zf.write('tmp/archive_extracted/' + folder + '/' + file, arcname=path)
		shutil.rmtree("tmp/extracted", ignore_errors=True)
		shutil.rmtree("tmp/archive_extracted", ignore_errors=True)
		