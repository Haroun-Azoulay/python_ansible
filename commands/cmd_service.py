import logging
from utils.cmd_result import CmdResult


def set_service_param(ssh_client, name, state, password):
    if state == "started":
        action = "start"
    elif state == "stopped":
        action = "stop"
    elif state == "restarted":
        action = "restart"
    elif state == "enabled":
        action = "enable"
    elif state == "disabled":
        action = "disable"
    else:
        error_msg = f"Invalid service state: {state}"
        logging.error(error_msg)
        return CmdResult(stderr=error_msg, exit_code=1)
    command_serv_without_sudo = f"systemctl {action} {name}"
    command_serv_sudo = f"sudo -S -p '' {command_serv_without_sudo}"

    try:
        stdin, stdout, stderr = ssh_client.exec_command(command_serv_sudo)
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
            f"An error occurred during execution on '{command_serv_sudo}': {str(e)}"
        )
        return CmdResult(stderr=str(e), exit_code=1)
