import json
import logging
import os
import shutil
import sys
from python_terraform import IsFlagged, Terraform
from tempfile import TemporaryDirectory


def apply_terraform(
        root_dir: str,
        region: str,
        short_region: str,
        environment: str,
        zone: str,
        set: str,
        workload_name: str,
        workload_type: str,
        workload_version: str,
        **kwargs: dict,
) -> dict:
    terraform_state_key = "{0}_{1}".format(set, workload_name)
    terraform_state_storage_account_resource_group_name = "{0}-{1}-{2}-tfstate-rg".format(  # noqa: E501
        zone,
        environment,
        short_region
    )
    terraform_state_storage_account_name = "{0}0{1}0{2}0tfstate0sa".format(
        zone,
        environment,
        short_region
    )

    terraform = Terraform(root_dir)

    return_code, _, _ = terraform.init(
        backend_config={
            "key": terraform_state_key,
            "resource_group_name": terraform_state_storage_account_resource_group_name,  # noqa: E501
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

    # return_code, _, _ = terraform.apply(
    #     dir_or_plan=terraform_plan_file_path,
    #     var=None,
    #     capture_output=False,
    # )
    # if (return_code != 0):
    #     exit(return_code)

    shutil.rmtree(temp_dir_path.name)

    logging.basicConfig(level=logging.DEBUG)
    root_logger = logging.getLogger()
    ch = logging.StreamHandler(sys.stdout)
    root_logger.addHandler(ch)

    # return terraform.output()

    return_code, stdout, stderr = terraform.output_cmd(json=IsFlagged)
    if (return_code != 0):
        print(stderr)
        exit(return_code)

    print(stdout)

    return json.loads(stdout)


def _test():
    raise NotImplementedError


if __name__ == "__main__":
    _test()
