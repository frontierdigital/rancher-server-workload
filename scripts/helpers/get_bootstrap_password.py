from helpers.exec import exec


def get_bootstrap_password(kubeconfig_file_path: str):
    stdout, _ = exec("kubectl get secret bootstrap-secret \
        --namespace cattle-system \
        --kubeconfig \"{0}\" \
        -o go-template='{{{{.data.bootstrapPassword|base64decode}}}}'".format(kubeconfig_file_path))  # noqa: E501
    return stdout.decode("utf-8")
