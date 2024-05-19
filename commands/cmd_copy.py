import logging
import os
from utils.cmd_result import CmdResult


def set_copy_param(ssh_client, src, dest, backup, password=None):
    try:
        if not os.path.isfile(src):
            raise FileNotFoundError(f"File source {src} doesn't exist")
        sftp_client = ssh_client.open_sftp()
        if backup:
            try:
                sftp_client.stat(dest)
                sftp_client.rename(dest, dest + ".backup")
            except FileNotFoundError:
                logging.error(f"No file exist on {dest} for backup")
        sftp_client.put(src, dest)
        sftp_client.close()
        return CmdResult(stdout="OK", stderr="", exit_code=0)
    except Exception as e:
        logging.error(f"An error occurred during execution on ':{e}")
        return CmdResult(stdout="", stderr=str(e), exit_code=1)
