import os
from azure.identity import ClientSecretCredential
from azure.mgmt.containerservice import ContainerServiceClient


def download_kubeconfig(
        dest_dir_path: str,
        client_id: str,
        client_secret: str,
        tenant_id: str,
        cluster_subscription_id: str,
        cluster_resource_group_name: str,
        cluster_name: str,
):
    credential = ClientSecretCredential(tenant_id, client_id, client_secret)
    client = ContainerServiceClient(
        credential=credential,
        subscription_id=cluster_subscription_id,
    )

    user_credentials = client.managed_clusters.list_cluster_user_credentials(
        cluster_resource_group_name,
        cluster_name,
    )

    kubeconfig_file_path = os.path.join(dest_dir_path, "kube.config")
    with open(kubeconfig_file_path, "wb") as kubeconfig_file:
        kubeconfig_file.write(user_credentials.kubeconfigs[0].value)

    return kubeconfig_file_path


def _test():
    raise NotImplementedError


if __name__ == "__main__":
    _test()
