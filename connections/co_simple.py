import paramiko
import logging


def co_simple_authentification(hostname, port, username):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(
            hostname=hostname, port=port, username=username, look_for_keys=False
        )
        logging.info(
            f"Connected to {hostname} on port {port} with simple authentification"
        )
        return client
    except paramiko.AuthenticationException:
        logging.error(f"An error occurred: {e}")
    except paramiko.SSHException as e:
        logging.error(f"An error occurred: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
