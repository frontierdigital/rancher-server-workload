import json
import os
import shutil
from helpers.get_short_region import get_short_region
from helpers.get_terraform_state_config import get_terraform_state_config
from python_terraform import IsFlagged, Terraform
from tempfile import TemporaryDirectory


def apply_terraform(
        working_dir: str,
        region: str,
        environment: str,
        zone: str,
        set: str,
        workload_name: str,
        workload_type: str,
        workload_version: str,
        **kwargs: dict,
) -> dict:
    (
        terraform_state_key,
        terraform_state_storage_account_resource_group_name,
        terraform_state_storage_account_name,
    ) = get_terraform_state_config(
        region=region,
        environment=environment,
        zone=zone,
        set=set,
        workload_name=workload_name,
    )
    short_region = get_short_region(region)

    terraform = Terraform(working_dir=working_dir)

    return_code, _, _ = terraform.init(
        backend_config={
            "key": terraform_state_key,
            "resource_group_name": terraform_state_storage_account_resource_group_name,
            "storage_account_name": terraform_state_storage_account_name,
        },
        capture_output=False,
    )
    if (return_code != 0):
        exit(return_code)

    temp_dir_path = TemporaryDirectory()
    terraform_plan_file_path = os.path.join(temp_dir_path.name, "main.tfplan")
    return_code, _, _ = terraform.plan(
        out=terraform_plan_file_path,
        var={
            "environment": environment,
            "location": region,
            "set": set,
            "short_location": short_region,
            "workload_name": workload_name,
            "workload_type": workload_type,
            "workload_version": workload_version,
            "zone": zone,
        },
        capture_output=False,
        **kwargs,
    )
    if (return_code != 0 and return_code != 2):
        exit(return_code)

    return_code, _, _ = terraform.apply(
        dir_or_plan=terraform_plan_file_path,
        var=None,
        capture_output=False,
    )
    if (return_code != 0):
        exit(return_code)

    shutil.rmtree(temp_dir_path.name)

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

    return_code, stdout, stderr = terraform.cmd("output", json=IsFlagged)
    if (return_code != 0):
        print(stderr)
        exit(return_code)

    out = stdout.replace('\n', '')
    print(out)
    return json.loads(out)


def _test():
    raise NotImplementedError


if __name__ == "__main__":
    _test()
