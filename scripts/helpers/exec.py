import subprocess


# def exec(command: str, silent: bool = True) -> tuple[str, str]:
def exec(command: str, opts: dict = {}) -> tuple[str, str]:
    cwd = opts.get("cwd", None)
    silent = opts.get("silent", True)

    process = subprocess.Popen(
        command,
        cwd=cwd,
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


def _test():
    raise NotImplementedError


if __name__ == "__main__":
    _test()
