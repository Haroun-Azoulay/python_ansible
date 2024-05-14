import click
import yaml
import logging
from commands.cmd_command import execute_command
from commands.cmd_apt import execute_apt
from commands.cmd_sysctl import set_sysctl_param
from commands.cmd_service import set_service_param
from commands.cmd_template import render_and_deploy_template
from commands.cmd_copy import set_copy_param
from connections.co_authentification import co_username_password
from connections.co_simple import co_simple_authentification
from connections.co_private_key import co_with_private_key


@click.command()
@click.option(
    "-f", "todos", required=True, help="Path to the todos file to open and read."
)
@click.option(
    "-i",
    "inventory",
    required=True,
    help="Path to the inventory file to open and read.",
)
def execute_tasks(todos, inventory):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    try:
        with open(todos, "r") as f:
            todos_data = yaml.safe_load(f)
        with open(inventory, "r") as f:
            inventory_data = yaml.safe_load(f)
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        return
    except Exception as e:
        logging.error(f"An error occurred while reading file: {e}")
        return

    servers = ["webserver", "bastion"]

    for server in servers:
        hostname = inventory_data["hosts"][server]["ssh_address"]
        port = inventory_data["hosts"][server]["ssh_port"]
        username = inventory_data["hosts"][server].get("identifier", {}).get("ssh_user")
        password = (
            inventory_data["hosts"][server].get("identifier", {}).get("ssh_password")
        )
        key_file = (
            inventory_data["hosts"][server].get("identifier", {}).get("ssh_key_file")
        )
        logging.info(f"processing {len(todos_data)} tasks on hosts:{hostname}.{port}")
        try:
            if username and password:
                client = co_username_password(
                    hostname=hostname, port=port, username=username, password=password
                )
            elif key_file:
                client = co_with_private_key(
                    hostname=hostname, port=port, username=username, key_file=key_file
                )
            else:
                client = co_simple_authentification(
                    hostname=hostname, port=port, username=username
                )

            if client is None:
                raise ValueError(f"Failed to connect to {hostname}")

            for task in todos_data:
                if "module" in task and "params" in task:
                    module = task["module"]
                    params = task["params"]
                    if module == "command":
                        command = params.get("command")
                        result = execute_command(client, command)
                        logging.info(
                            f"[{server}] host={hostname}.{port} - op={module} - {command} - status={result.stdout}"
                        )
                    elif module == "apt":
                        package = params.get("name")
                        state = params.get("state")
                        apt_command = (
                            f"apt-get install -y {package}"
                            if state == "present"
                            else f"apt-get remove -y {package}"
                        )
                        result = execute_apt(client, apt_command, password)
                        logging.info(
                            f"[{server}] host= {hostname}:{port} - op={module} - name={package} state={state}"
                        )
                        logging.info(
                            f"[{server}] host= {hostname}:{port} - status={result.stdout}"
                        )
                    elif module == "sysctl":
                        attribute = params.get("attribute")
                        value = params.get("value")
                        permanent = params.get("permanent")
                        result = set_sysctl_param(
                            client, attribute, value, permanent, password
                        )
                        logging.info(
                            f"[{server}] host={hostname}.{port} - op={module} - permanent={permanent}, sysctl={attribute}, Value={value}, Permanent={permanent}, status={result.stdout}"
                        )
                    elif module == "service":
                        name = params.get("name")
                        state = params.get("state")
                        result = set_service_param(client, name, state, password)
                        logging.info(
                            f"[{server}] host={hostname}.{port} - service={name}, value={state}, status={result.stdout}"
                        )
                    elif module == "template":
                        src = params.get("src")
                        dest = params.get("dest")
                        vars = params.get("vars")
                        result = render_and_deploy_template(
                            client, src, dest, vars, password
                        )
                        logging.info(
                            f"[{server}] host={hostname}.{port} - op={module} - source={src} - destination={dest}, variables={vars}, status={result.stdout}"
                        )
                    elif module == "copy":
                        src = params.get("src")
                        dest = params.get("dest")
                        backup = params.get("backup")
                        result = set_copy_param(client, src, dest, backup, password)
                        logging.info(
                            f"[{server}] host={hostname}.{port} - op={module} - source={src} - destination={dest} - backup={backup} - status={result.stdout}"
                        )

                else:
                    logging.error("Invalid task format.")
        except Exception as e:
            logging.error(f"An error occurred during execution on {hostname}: {e}")
        finally:
            logging.info(
                f"{len(todos_data)} tasks on hosts:{hostname}.{port} is finished"
            )
            client.close()


if __name__ == "__main__":
    execute_tasks()
