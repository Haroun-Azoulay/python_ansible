import paramiko
import logging


def co_username_password(hostname, port, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    try:
        client.connect(
            hostname=hostname,
            port=port,
            username=username,
            password=password,
            look_for_keys=False,
            allow_agent=False,
        )
        logging.info(
            f"Connected to {hostname} on port {port} with username and password authentification"
        )
        return client
    except paramiko.ssh_exception.NoValidConnectionsError as e:
        logging.error(f"Could not connect to {hostname} on port {port}: {e}")
    except paramiko.AuthenticationException as e:
        logging.error(f"Authentication failed for {hostname}: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
