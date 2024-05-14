import logging
from utils.cmd_result import CmdResult


def set_sysctl_param(ssh_client, param, value, permanent, password):

    try:
        if permanent:
            permanent_command = (
                f"echo '{param} = {value}' | sudo tee -a /etc/sysctl.conf"
            )
            command = "sudo -S -p '' %s" % permanent_command
            stdin, stdout, stderr = ssh_client.exec_command(command)
            stdin.write(password + "\n")
            stdin.flush()
            cmd_output = stdout.read().decode()
            error_output = stderr.read().decode()
            exit_status = stdout.channel.recv_exit_status()
            return CmdResult(
                stdout=cmd_output, stderr=error_output, exit_code=exit_status
            )
        else:
            temp_command = f"sysctl -w {param}={value}"
            command = "sudo -S -p '' %s" % temp_command
            stdin, stdout, stderr = ssh_client.exec_command(command)
            stdin.write(password + "\n")
            stdin.flush()
            cmd_output = stdout.read().decode()
            error_output = stderr.read().decode()
            exit_status = stdout.channel.recv_exit_status()
            return CmdResult(
                stdout=cmd_output, stderr=error_output, exit_code=exit_status
            )

    except Exception as e:
        logging.error(f"An error occurred during execution on '{param}: {e}")
        return CmdResult(stdout="", stderr=str(e), exit_code=1)
