import logging
from utils.cmd_result import CmdResult


def execute_apt(ssh_client, command, password):
    command_apt_without_sudo = f"{command}"
    command_apt_sudo = "sudo -S -p '' %s" % command_apt_without_sudo

    try:
        stdin, stdout, stderr = ssh_client.exec_command(command_apt_sudo)
        stdin.write(password + "\n")
        stdin.flush()
        cmd_output = stdout.read().decode()
        error_output = stderr.read().decode()
        exit_status = stdout.channel.recv_exit_status()
        return CmdResult(stdout=cmd_output, stderr=error_output, exit_code=exit_status)
    except Exception as e:
        logging.error(
            f"An error occurred during execution on '{command_apt_sudo}': {e}"
        )
        return CmdResult(stdout="", stderr=str(e), exit_code=1)
