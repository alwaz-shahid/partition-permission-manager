import os
import click
import getpass

def permission_string(permissions):
    return "".join([
        "read" if permissions & 0o400 else "-",
        "write" if permissions & 0o200 else "-",
        "execute" if permissions & 0o100 else "-",
    ])

def display_manual():
    click.echo("Welcome to the Partition and Disk Permission Manager for Linux!")
    click.echo("===============================================================\n")
    click.echo("This tool allows you to view and modify permissions for partitions and disks.")
    click.echo("You can use natural language like 'r' for read, 'w' for write, and 'e' for execute when setting permissions.")
    click.echo("Here are some usage examples:")
    click.echo("  - 'r w e' or '7': Give read, write, and execute permissions.")
    click.echo("  - 'r e' or '5': Give read and execute permissions.")
    click.echo("  - 'r' or '4': Give read-only permissions.\n")

@click.command()
def main():
    display_manual()

    current_user = getpass.getuser()
    click.echo(f"Current User: {current_user}\n")

    partitions_output = os.popen("lsblk -o NAME,MOUNTPOINT,SIZE,FSTYPE --noheadings").read()
    partitions = partitions_output.strip().split("\n")

    for partition_info in partitions:
        partition_info = partition_info.split()
        if len(partition_info) < 4:
            continue

        name, mountpoint, size, fstype = partition_info

        if mountpoint == "":
            continue

        partition_path = os.path.join("/", mountpoint)
        try:
            permissions = os.stat(partition_path)
            
            click.echo(f"Partition: {name}")
            click.echo(f"  Mount Point: {mountpoint}")
            click.echo(f"  Size: {size}")
            click.echo(f"  File System Type: {fstype}")
            click.echo(f"  Owner Permissions: {permission_string(permissions.st_mode & 0o700)}")
            click.echo(f"  Group Permissions: {permission_string(permissions.st_mode & 0o070)}")
            click.echo(f"  Others Permissions: {permission_string(permissions.st_mode & 0o007)}\n")

            choice = click.confirm("Do you want to change permissions?", default=False)
            if choice:
                new_permissions = click.prompt("Enter new permissions (e.g., r w e = 7):", default="7")
                permission_value = 0
                if "r" in new_permissions:
                    permission_value |= 0o400
                if "w" in new_permissions:
                    permission_value |= 0o200
                if "e" in new_permissions:
                    permission_value |= 0o100

                os.chmod(partition_path, permission_value)
                click.echo("Permissions updated successfully.\n")
            else:
                click.echo("Permissions remain unchanged.\n")

        except OSError as e:
            click.echo(f"Error accessing partition: {mountpoint}")
            click.echo(f"Error details: {e}\n")

if __name__ == "__main__":
    main()
