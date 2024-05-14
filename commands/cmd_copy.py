import logging
from utils.cmd_result import CmdResult


def set_copy_param(ssh_client, src, dest, backup, password):
    command_copy_whitout_sudo = f"cp -r {src} {dest}"
    command_copy_sudo = "sudo -S -p '' %s" % command_copy_whitout_sudo

    if backup:
        command_copy_whitout_sudo = f"cp -r {dest} {dest}.backup"
        command_copy_sudo = "sudo -S -p '' %s" % command_copy_whitout_sudo

    try:
        stdin, stdout, stderr = ssh_client.exec_command(command_copy_sudo)
        stdin.write(password + "\n")
        stdin.flush()
        cmd_output = stdout.read().decode()
        error_output = stderr.read().decode()
        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            cmd_output = "OK"
        return CmdResult(stdout=cmd_output, stderr=error_output, exit_code=exit_status)
    except Exception as e:
        logging.error(
            f"An error occurred during execution on '{command_copy_sudo}': {e}"
        )
        return CmdResult(stdout="", stderr=str(e), exit_code=1)
