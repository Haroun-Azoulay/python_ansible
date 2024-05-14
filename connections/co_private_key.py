import paramiko
import logging
import os


def co_with_private_key(hostname, port, username, key_file):
    private_key_path = os.path.expanduser(key_file)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(
            hostname=hostname,
            port=port,
            username=username,
            key_filename=private_key_path,
            look_for_keys=False,
        )
        logging.info(
            f"Connected to {hostname} on port {port} with private authentification"
        )
        return client

    except paramiko.AuthenticationException:
        logging.error(f"An error occurred: {e}")
    except paramiko.SSHException as e:
        logging.error(f"An error occurred: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
