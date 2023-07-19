module "key_vault" {
  source = "git::https://github.com/frontierdigital/key-vault-terraform-module//src?ref=v1.0.0-pre.f2d113d"

  environment                = var.environment
  identifier                 = "ranserv"
  location                   = var.location
  log_analytics_workspace_id = data.azurerm_log_analytics_workspace.main.id
  resource_group_name        = module.resource_group.name
  tags                       = var.tags
  tenant_id                  = data.azurerm_client_config.main.tenant_id
  workload_name              = var.workload_name
  workload_type              = var.workload_type
  workload_version           = var.workload_version
  zone                       = var.zone
}

resource "azurerm_role_assignment" "key_vault_administrator" {
  scope                = module.key_vault.id
  role_definition_name = "Key Vault Administrator"
  principal_id         = data.azurerm_client_config.main.object_id
}
