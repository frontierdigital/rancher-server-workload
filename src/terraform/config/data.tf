data "azuread_client_config" "main" {}

data "azurerm_client_config" "main" {}

data "azurerm_key_vault" "main" {
  name                = split("/", var.rancher_server_key_vault_id)[8]
  resource_group_name = split("/", var.rancher_server_key_vault_id)[4]
}
