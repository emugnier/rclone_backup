from datetime import datetime
import subprocess
import sys
import logging
import argparse
from time import sleep

# # get_date_first archive
# def get_date_first_archive():
#     # rclone ls first date
#     date_time_obj = datetime.strptime(extracted_date, "%d_%m_%y_%H_%M_%S")

# if new_month:
# copy and create new backup

# if new_week:
# sync incrementaly

# dt=date +%Y%m%d.%I%M%S
# rclone sync /path/to/local/folder remote:backup --backup-dir=remote:archive/$dt
# TODO add log with time
stream_handler = None


def setup_logging(log_file, log_level):

    formatter = logging.Formatter("[ %(levelname)s ] %(message)s")
    handlerFile = logging.FileHandler(log_file)
    handlerOut = logging.StreamHandler(sys.stdout)
    global stream_handler
    stream_handler = handlerOut

    logging.basicConfig(level=log_level, handlers=[handlerFile, handlerOut])


def execute_command(command):
    logging.info("EXECUTE %s" % command)

    res = subprocess.Popen(
        command.split(),
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        encoding="utf-8",
    )
    while True:
        line_stdout = res.stdout.readline()
        if line_stdout == "" and res.poll() is not None:
            break
        if line_stdout != "":
            logging.info("RESULT %s", line_stdout)

    line_stderr = res.stderr.readline()
    if line_stderr != "":
        logging.error(line_stderr)


def sync(remote, path):
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")

    command = "rclone sync -P {path} {remote}:backup --backup-dir={remote}:archive/{dt_string}".format(
        remote=remote, dt_string=dt_string, path=path
    )
    execute_command(command)


# restore data
def restore():
    return True


def mount(remote, mounted_path):
    command = "rclone mount {remote}:backup {mounted_path}".format(
        remote=remote, mounted_path=mounted_path
    )
    execute_command(command)


if __name__ == "__main__":
    main_parser = argparse.ArgumentParser(prog="rclone backup tool")
    subparsers = main_parser.add_subparsers(dest="command", required=True)
    parser_sync = subparsers.add_parser("sync")
    parser_sync.add_argument("remote", type=str, help="remote")
    parser_sync.add_argument("path", type=str, help="path to the content to backup")
    parser_mount = subparsers.add_parser("mount")
    parser_mount.add_argument("remote", type=str, help="remote")
    parser_mount.add_argument("path", type=str, help="mount location")

    args = main_parser.parse_args()
    setup_logging("log.info", 0)

    if args.command == "sync":
        sync(args.remote, args.path)

    if args.command == "mount":
        mount(args.remote, args.path)
