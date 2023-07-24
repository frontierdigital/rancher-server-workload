from python_terraform import Terraform


def handle_error(return_code: int, stdout: str, stderr: str):
    print(stdout)
    print(stderr)
    exit(return_code)


def test(working_dir: str, validate: bool = True):
    print(f"testing terraform resources in '{working_dir}'")

    t = Terraform(working_dir=working_dir)
    return_code, stdout, stderr = t.fmt(check=True, diff=True)
    if (return_code != 0):
        handle_error(return_code, stdout, stderr)

    if (validate):
        return_code, stdout, stderr = t.init(backend=False)
        if (return_code != 0):
            handle_error(return_code, stdout, stderr)

        return_code, stdout, stderr = t.validate()
        if (return_code != 0):
            handle_error(return_code, stdout, stderr)


if __name__ == "__main__":
    test('src/terraform/infra')
