import os
from helpers.apply_terraform import apply_terraform

# from azure.mgmt.kubernetesconfiguration import KubernetesConfigurationClient


def destroy():
    region = os.getenv("REGION")
    short_region = None
    match region:
        case "uksouth":
            short_region = "uks"
        case "ukwest":
            short_region = "ukw"

    apply_terraform(
        root_dir=os.path.join(os.getcwd(), "src/terraform/infra"),
        region=region,
        short_region=short_region,
        environment=os.getenv("ENVIRONMENT"),
        zone=os.getenv("ZONE"),
        set=os.getenv("SET"),
        workload_name=os.getenv("WORKLOAD_NAME"),
        workload_type=os.getenv("WORKLOAD_TYPE"),
        workload_version=os.getenv("WORKLOAD_VERSION"),
        destroy=True,
    )

    # client = KubernetesConfigurationClient()


if __name__ == "__main__":
    destroy()
