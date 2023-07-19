locals {
  identifier                          = "rancherserver"
  virtual_network_name                = "${var.zone}-${var.environment}-${var.short_location}-main-vnet"
  virtual_network_resource_group_name = "${var.zone}-${var.environment}-${var.short_location}-network-rg"
}
