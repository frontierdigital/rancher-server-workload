resource "random_password" "main" {
  length = 16
}

resource "rancher2_bootstrap" "main" {
  provider = rancher2.bootstrap

  initial_password = var.bootstrap_password
  password         = random_password.main.result
  telemetry        = true
  token_update     = true
}

resource "azurerm_key_vault_secret" "rancher_admin_username" {
  name         = "rancher-admin-username"
  value        = "admin"
  key_vault_id = data.azurerm_key_vault.main.id
}

resource "azurerm_key_vault_secret" "rancher_admin_password" {
  name         = "rancher-admin-password"
  value        = random_password.main.result
  key_vault_id = data.azurerm_key_vault.main.id
}

resource "rancher2_token" "main" {
  description = "Global token used for automated provisioning of clusters"
}

resource "azurerm_key_vault_secret" "rancher_admin_token" {
  name         = "rancher-admin-token"
  value        = rancher2_token.main.token
  key_vault_id = data.azurerm_key_vault.main.id
}

resource "azurerm_key_vault_secret" "rancher_server_api_url" {
  name         = "rancher-server-api-url"
  value        = var.rancher_server_api_url
  key_vault_id = data.azurerm_key_vault.main.id
}
