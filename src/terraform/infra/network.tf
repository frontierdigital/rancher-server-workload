resource "azurerm_subnet" "main" {
  name                 = "${local.identifier}-aks"
  virtual_network_name = local.virtual_network_name
  resource_group_name  = local.virtual_network_resource_group_name
  address_prefixes     = [cidrsubnet(data.azurerm_virtual_network.main.address_space[0], var.cidrsubnet_newbits, var.cidrsubnet_netnum)]
}
