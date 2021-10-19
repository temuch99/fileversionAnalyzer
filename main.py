import sys
import click
import psutil

# @click.argument('keyword', required=False)

@click.group()
@click.version_option("1.0.0")
def main():
    """Utility for getting saving file versions in OS Windows"""
    pass

@main.command()
def disks_list():
    """Get list disks"""
    click.echo("Discs list:")
    for partition in psutil.disk_partitions():
    	click.echo("Device: {}, Mountpoint: {}, FSType: {}, Opts: {}".format(partition.device, partition.mountpoint, partition.fstype, partition.opts))

if __name__ == '__main__':
    args = sys.argv
    # if "--help" in args or len(args) == 1:
    #     print("Manual")
    main()