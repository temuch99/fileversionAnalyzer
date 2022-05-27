import sys
import click

from src.FileVersionsModule.Win7FileVersions import Win7FileVersions
from src.FileVersionsModule.MacFileVersions import MacFileVersions

@click.command()
@click.option('--path', help='path to mounted system')
@click.option('--output', help='path to extracted files')
@click.option('--os', help='os type (win10/win7/mac)')
def create_fv(path, output, os):
    if os == 'mac':
        versions = MacFileVersions(path, output)
    elif os == 'win7':
        versions = Win7FileVersions(path, output)
    else:
        print("ERROR")
        return

    versions.create()

if __name__ == '__main__':
	create_fv()