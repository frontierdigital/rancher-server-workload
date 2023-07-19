# module "key_vault" {
#   source = "git::https://frontierdigital@dev.azure.com/frontierdigital/Demo/_git/key-vault-terraform-module//src?ref=1.0.4"

#   environment         = var.environment
#   identifier          = "ranserv"
#   location            = var.location
#   resource_group_name = module.resource_group.name
#   tags                = var.tags
#   tenant_id           = data.azurerm_client_config.main.tenant_id
#   workload_name       = var.workload_name
#   workload_type       = var.workload_type
#   workload_version    = var.workload_version
#   zone                = var.zone
# }

# resource "azurerm_role_assignment" "key_vault_administrator" {
#   scope                = module.key_vault.id
#   role_definition_name = "Key Vault Administrator"
#   principal_id         = data.azurerm_client_config.main.object_id
# }
