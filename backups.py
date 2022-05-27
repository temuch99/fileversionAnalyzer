import sys
import click
from src.BackupVersionsModule.Windows7BackupVersions import Windows7BackupVersions
from src.BackupVersionsModule.MacBackupVersions import MacBackupVersions

@click.command()
@click.option('--path', help='path to mounted system')
@click.option('--os', help='os type (win10/win8/win7/macOS)')
@click.option('--output', help='path for output path (backup.zip)')
def get_backups(path, os, output):
    """Detect file version is enabled"""
    if os == 'win7':
        backupVersions = Windows7BackupVersions(path)
    elif os == 'mac':
        backupVersions = MacBackupVersions(path)
    else:
        print("ERROR")
        return

    backupVersions.get(output)



if __name__ == '__main__':
	get_backups()