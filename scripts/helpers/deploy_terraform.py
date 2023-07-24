import os
from python_terraform import Terraform


def deploy_terraform(
        root_dir: str,
        region: str,
        short_region: str,
        environment: str,
        zone: str,
        set: str,
        workload_name: str,
        workload_type: str,
        workload_version: str,
):
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

    return_code, _, _ = terraform.apply(
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
        var_file=os.path.join(os.getcwd(), ".config", "main.tfvars"),  # noqa: E501
        skip_plan=True,
        capture_output=False,
    )
    if (return_code != 0):
        exit(return_code)
