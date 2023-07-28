data "azurerm_client_config" "main" {}

data "azurerm_log_analytics_workspace" "main" {
  name                = "${var.zone}-${var.environment}-${var.short_location}-main-law"
  resource_group_name = "${var.zone}-${var.environment}-${var.short_location}-loganalytics-rg"
}

data "azurerm_virtual_network" "main" {
  name                = local.virtual_network_name
  resource_group_name = local.virtual_network_resource_group_name
}
