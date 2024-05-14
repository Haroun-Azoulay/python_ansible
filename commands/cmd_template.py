import jinja2
import logging
from utils.cmd_result import CmdResult


def render_and_deploy_template(ssh_client, src, dest, vars, password):
    try:
        template_loader = jinja2.FileSystemLoader(searchpath="./")
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(src)
        rendered_content = template.render(vars)

        remote_tmp_path = "/tmp/temp_rendered_template"
        with ssh_client.open_sftp() as sftp:
            with sftp.file(remote_tmp_path, "w") as remote_file:
                remote_file.write(rendered_content)

        move_command = f"sudo -S -p '' mv {remote_tmp_path} {dest}"
        stdin, stdout, stderr = ssh_client.exec_command(move_command)
        stdin.write(password + "\n")
        stdin.flush()
        cmd_output = stdout.read().decode()
        error_output = stderr.read().decode()
        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            cmd_output = "OK"
        return CmdResult(stdout=cmd_output, stderr=error_output, exit_code=exit_status)

    except Exception as e:
        logging.error(f"An error occurred during execution on '{src}: {str(e)}")
        return CmdResult(stdout="", stderr=str(e), exit_code=1)
