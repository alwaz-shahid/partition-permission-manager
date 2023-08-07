import os
import click

@click.command()
def main():
    """Partition Permissions Manager"""
    partitions = get_partitions()

    click.echo("Available Partitions:")
    for idx, partition in enumerate(partitions, start=1):
        click.echo(f"{idx}. {partition}")

    partition_choice = click.prompt("\nEnter the number of the partition to manage permissions:", type=int)
    if 1 <= partition_choice <= len(partitions):
        selected_partition = partitions[partition_choice - 1]
        display_partition_info(selected_partition)
        change_permissions(selected_partition)
    else:
        click.echo("Invalid partition choice.")

def get_partitions():
    partitions_output = os.popen("lsblk -o MOUNTPOINT").read()
    partitions = partitions_output.strip().split("\n")[1:]
    return [partition for partition in partitions if partition]

def display_partition_info(partition):
    click.echo(f"\nPartition: {partition}")
    permissions = os.stat(os.path.join("/", partition))
    click.echo(f"  Owner Permissions: {permission_string(permissions.st_mode & 0o700)}")
    click.echo(f"  Group Permissions: {permission_string(permissions.st_mode & 0o070)}")
    click.echo(f"  Others Permissions: {permission_string(permissions.st_mode & 0o007)}")

def change_permissions(partition):
    new_permissions = click.prompt("\nEnter new permissions (e.g., read write execute = 7):", default="7")
    if new_permissions.lower() == "read write execute" or new_permissions == "7":
        os.chmod(os.path.join("/", partition), 0o777)
        click.echo("Permissions updated successfully.\n")
    elif new_permissions.lower() == "read execute" or new_permissions == "5":
        os.chmod(os.path.join("/", partition), 0o555)
        click.echo("Permissions updated successfully.\n")
    elif new_permissions.lower() == "read" or new_permissions == "4":
        os.chmod(os.path.join("/", partition), 0o444)
        click.echo("Permissions updated successfully.\n")
    else:
        click.echo("Invalid permission input. Permissions remain unchanged.\n")

def permission_string(permissions):
    return "".join([
        "r" if permissions & 0o400 else "-",
        "w" if permissions & 0o200 else "-",
        "x" if permissions & 0o100 else "-",
    ])

if __name__ == "__main__":
    main()
