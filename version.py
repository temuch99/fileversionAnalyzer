import sys
import click
from src.DetectModule.Windows10Detector import Windows10Detector
from src.DetectModule.Windows7Detector import Windows7Detector
from src.DetectModule.MacDetector import MacDetector

@click.command()
@click.option('--path', help='path to mounted system')
@click.option('--os', help='os type (win10/win8/win7/macOS)')
def is_enabled_fv(path, os):
    """Detect file version is enabled"""
    if os == 'win10':
        detector = Windows10Detector(path)
    elif os == 'win7':
        detector = Windows7Detector(path)
    elif os == 'macOS':
        detector = MacDetector(path)
    else:
        print("ERROR")
        return

    print(detector.detect())



if __name__ == '__main__':
	is_enabled_fv()