from helpers.get_short_region import get_short_region


def get_terraform_state_config(
        region: str,
        environment: str,
        zone: str,
        set: str,
        workload_name: str,
) -> tuple[str, str, str]:
    short_region = get_short_region(region=region)

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

    return terraform_state_key, terraform_state_storage_account_resource_group_name, terraform_state_storage_account_name  # noqa: E501


def _test():
    raise NotImplementedError


if __name__ == "__main__":
    _test()
