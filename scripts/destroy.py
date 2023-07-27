import os
from helpers.apply_terraform import apply_terraform
from helpers.download_kubeconfig import download_kubeconfig
from helpers.get_bootstrap_password import get_bootstrap_password
from helpers.get_ingress_external_ip import get_ingress_external_ip
from helpers.get_short_region import get_short_region
from helpers.get_terraform_state_config import get_terraform_state_config
from python_terraform import Terraform
from tempfile import TemporaryDirectory


def destroy():
    region = os.getenv("REGION")
    short_region = get_short_region(region)

    (
        terraform_state_key,
        terraform_state_storage_account_resource_group_name,
        terraform_state_storage_account_name,
    ) = get_terraform_state_config(
        region=region,
        environment=os.getenv("ENVIRONMENT"),
        zone=os.getenv("ZONE"),
        set=os.getenv("SET"),
        workload_name="{0}-infra".format(os.getenv("WORKLOAD_NAME")),
    )

    terraform = Terraform(
        working_dir=os.path.join(os.getcwd(), "src/terraform/infra"),
    )

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

    terraform_output = terraform.output()
    kubernetes_cluster_id = terraform_output["kubernetes_cluster_id"]["value"]
    key_vault_id = terraform_output["key_vault_id"]["value"]

    kubernetes_cluster_subscription_id = kubernetes_cluster_id.split("/")[2]
    kubernetes_cluster_resource_group_name = kubernetes_cluster_id.split(
        "/")[4]
    kubernetes_cluster_name = kubernetes_cluster_id.split("/")[8]

    temp_dir_path = TemporaryDirectory()
    kubeconfig_file_path = download_kubeconfig(
        dest_dir_path=temp_dir_path.name,
        client_id=os.getenv("ARM_CLIENT_ID"),
        client_secret=os.getenv("ARM_CLIENT_SECRET"),
        tenant_id=os.getenv("ARM_TENANT_ID"),
        cluster_subscription_id=kubernetes_cluster_subscription_id,
        cluster_resource_group_name=kubernetes_cluster_resource_group_name,
        cluster_name=kubernetes_cluster_name,
    )

    ingress_external_ip = get_ingress_external_ip(kubeconfig_file_path)
    external_hostname = "{0}.nip.io".format(ingress_external_ip)

    bootstrap_password = get_bootstrap_password(kubeconfig_file_path)

    apply_terraform(
        working_dir=os.path.join(os.getcwd(), "src/terraform/config"),
        region=region,
        short_region=short_region,
        environment=os.getenv("ENVIRONMENT"),
        zone=os.getenv("ZONE"),
        set=os.getenv("SET"),
        workload_name="{0}-config".format(os.getenv("WORKLOAD_NAME")),
        workload_type=os.getenv("WORKLOAD_TYPE"),
        workload_version=os.getenv("WORKLOAD_VERSION"),
        vars={
            "bootstrap_password": bootstrap_password,
            "rancher_server_api_url": "https://{0}".format(external_hostname),
            "rancher_server_key_vault_id": key_vault_id,
        },
        destroy=True,
    )

    apply_terraform(
        working_dir=os.path.join(os.getcwd(), "src/terraform/infra"),
        region=region,
        short_region=short_region,
        environment=os.getenv("ENVIRONMENT"),
        zone=os.getenv("ZONE"),
        set=os.getenv("SET"),
        workload_name="{0}-infra".format(os.getenv("WORKLOAD_NAME")),
        workload_type=os.getenv("WORKLOAD_TYPE"),
        workload_version=os.getenv("WORKLOAD_VERSION"),
        var_file=os.path.join(os.getcwd(), ".config", "main.tfvars"),
        destroy=True,
    )


if __name__ == "__main__":
    destroy()
