import os
import click

@click.command()
def main():
    partitions = []

    partitions_output = os.popen("lsblk -o MOUNTPOINT").read()
    partitions = partitions_output.strip().split("\n")[1:]

    for partition in partitions:
        if partition == "":
            continue

        partition_path = os.path.join("/", partition)
        permissions = os.stat(partition_path)
        
        click.echo(f"Partition: {partition_path}")
        click.echo(f"  Owner Permissions: {oct(permissions.st_mode & 0o777)}")

        new_permissions = click.prompt("Enter new permissions (e.g., 755):", default="755")
        os.chmod(partition_path, int(new_permissions, 8))

if __name__ == "__main__":
    main()
