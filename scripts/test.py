import os
from python_terraform import Terraform


def test_terraform(working_dir: str, validate: bool = True):
    print(f"testing terraform resources in '{working_dir}'")

    terraform = Terraform(working_dir=working_dir)
    return_code, _, _ = terraform.fmt(
        check=True,
        diff=True,
        capture_output=False,
    )
    if (return_code != 0):
        exit(return_code)

    if (validate):
        return_code, _, _ = terraform.init(backend=False, capture_output=False)
        if (return_code != 0):
            exit(return_code)

        return_code, _, _ = terraform.validate(capture_output=False)
        if (return_code != 0):
            exit(return_code)


if __name__ == "__main__":
    test_terraform(os.path.join(os.getcwd(), "src/terraform/infra"))
    test_terraform(os.path.join(os.getcwd(), "src/terraform/config"))
