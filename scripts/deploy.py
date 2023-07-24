import os
from python_terraform import Terraform
from tempfile import TemporaryDirectory


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
    terraform_state_key = "{}".format(workload_name)
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

    temp_dir_path = TemporaryDirectory()

    t = Terraform(root_dir)

    return_code, _, _ = t.init(
        backend_config={
            "key": terraform_state_key,
            "resource_group_name": terraform_state_storage_account_resource_group_name,  # noqa: E501
            "storage_account_name": terraform_state_storage_account_name,
        },
        capture_output=False,
    )
    if (return_code != 0):
        exit(return_code)

    tf_plan_file_path = os.path.join(temp_dir_path.name, "main.tfplan")

    return_code, _, _ = t.plan(
        out=tf_plan_file_path,
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
        capture_output=False,
    )
    if (return_code != 0):
        exit(return_code)


def deploy():
    region = os.environ["REGION"]
    short_region = None
    match region:
        case "uksouth":
            short_region = "uks"
        case "ukwest":
            short_region = "ukw"

    deploy_terraform(
        os.path.join(os.getcwd(), "src/terraform/infra"),
        region,
        short_region,
        os.environ["ENVIRONMENT"],
        os.environ["ZONE"],
        os.environ["SET"],
        os.environ["WORKLOAD_NAME"],
        os.environ["WORKLOAD_TYPE"],
        os.environ["WORKLOAD_VERSION"],
    )


if __name__ == "__main__":
    deploy()
