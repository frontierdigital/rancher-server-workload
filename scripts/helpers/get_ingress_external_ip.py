from helpers.exec import exec


def get_ingress_external_ip(kubeconfig_file_path: str) -> str:
    stdout, _ = exec("kubectl get svc \
        --namespace ingress-nginx \
        --output jsonpath='{{.status.loadBalancer.ingress[0].ip}}' \
        --kubeconfig \"{0}\" \
        ingress-nginx-controller".format(kubeconfig_file_path))
    return stdout.decode("utf-8")


def _test():
    raise NotImplementedError


if __name__ == "__main__":
    _test()
