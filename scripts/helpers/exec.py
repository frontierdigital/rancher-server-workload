import subprocess


def exec(command: str, silent: bool = True):
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        raise Exception(stderr.decode("utf-8"))

    if silent is False:
        print(stdout.decode("utf-8"))

    return stdout, stderr
