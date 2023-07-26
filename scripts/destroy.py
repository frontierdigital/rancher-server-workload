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
        os.path.join(os.getcwd(), "src/terraform/infra"),
        region,
        short_region,
        os.getenv("ENVIRONMENT"),
        os.getenv("ZONE"),
        os.getenv("SET"),
        os.getenv("WORKLOAD_NAME"),
        os.getenv("WORKLOAD_TYPE"),
        os.getenv("WORKLOAD_VERSION"),
        True,
    )

    # client = KubernetesConfigurationClient()


if __name__ == "__main__":
    destroy()
