import json
from python_terraform import Terraform
from helpers.exec import exec


def get_terraform_output(terraform: Terraform) -> dict:
    # return terraform.output()
    #
    # For some reason, terraform.output() doesn't work here:
    #
    # Traceback (most recent call last):
    # File "/home/runner/work/rancher-cluster-workload/rancher-cluster-workload/scripts/deploy.py", line 22, in <module>
    #     deploy()
    # File "/home/runner/work/rancher-cluster-workload/rancher-cluster-workload/scripts/deploy.py", line 8, in deploy
    #     apply_terraform(
    # File "/home/runner/work/rancher-cluster-workload/rancher-cluster-workload/scripts/helpers/apply_terraform.py", line 76, in apply_terraform
    #     return terraform.output()
    #         ^^^^^^^^^^^^^^^^^^
    # File "/home/runner/.local/share/virtualenvs/rancher-cluster-workload-fE1wvjYY/lib/python3.11/site-packages/python_terraform/__init__.py", line 360, in output
    #     value = json.loads(out)
    #             ^^^^^^^^^^^^^^^
    # File "/opt/hostedtoolcache/Python/3.11.4/x64/lib/python3.11/json/__init__.py", line 346, in loads
    #     return _default_decoder.decode(s)
    #         ^^^^^^^^^^^^^^^^^^^^^^^^^^
    # File "/opt/hostedtoolcache/Python/3.11.4/x64/lib/python3.11/json/decoder.py", line 337, in decode
    #     obj, end = self.raw_decode(s, idx=_w(s, 0).end())
    #             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # File "/opt/hostedtoolcache/Python/3.11.4/x64/lib/python3.11/json/decoder.py", line 355, in raw_decode
    #     raise JSONDecodeError("Expecting value", s, err.value) from None
    # json.decoder.JSONDecodeError: Expecting value: line 1 column 2 (char 1)

    stdout = exec(
        command="terraform output -json",
        opts={"cwd": terraform.working_dir},
    )

    json_str = stdout[0].decode("utf-8")

    front_idx = json_str.find("terraform-bin output -json")
    if front_idx != -1:
        json_str = json_str[front_idx + len("terraform-bin output -json"):]

    back_idx = json_str.find("::debug::")
    if back_idx != -1:
        json_str = json_str[:back_idx]

    return json.loads(json_str)
