import logging
from utils.cmd_result import CmdResult


def execute_command(client, command):
    try:
        stdin, stdout, stderr = client.exec_command(command)
        cmd_output = stdout.read().decode()
        error_output = stderr.read().decode()
        exit_status = stdout.channel.recv_exit_status()
        return CmdResult(stdout=cmd_output, stderr=error_output, exit_code=exit_status)
    except Exception as e:
        logging.error(f"An error occurred during execution on '{command}': {e}")
        return CmdResult(stdout="", stderr=str(e), exit_code=1)
