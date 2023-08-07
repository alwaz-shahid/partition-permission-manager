import os
import click
import getpass

def permission_string(permissions):
    return "".join([
        "r" if permissions & 0o400 else "-",
        "w" if permissions & 0o200 else "-",
        "x" if permissions & 0o100 else "-",
    ])

@click.command()
def main():
    click.echo("Partition Permission Manager for Linux")
    click.echo("======================================\n")
    
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

            choice = click.prompt("Do you want to change permissions? (yes/no): ").strip().lower()
            if choice == "yes":
                new_permissions = click.prompt("Enter new permissions (e.g., 755):", default="755")
                os.chmod(partition_path, int(new_permissions, 8))
                click.echo("Permissions updated successfully.\n")
            else:
                click.echo("Permissions remain unchanged.\n")

        except OSError as e:
            click.echo(f"Error accessing partition: {mountpoint}")
            click.echo(f"Error details: {e}\n")

if __name__ == "__main__":
    main()
