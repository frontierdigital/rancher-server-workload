locals {
  identifier                          = "rancherserver"
  virtual_network_name                = "${var.zone}-${var.environment}-${var.short_location}-main-vnet"
  virtual_network_resource_group_name = "${var.zone}-${var.environment}-${var.short_location}-network-rg"

  tags = {
    Environment     = var.environment
    Set             = var.set
    WorkloadName    = var.workload_name
    WorkloadType    = var.workload_type
    WorkloadVersion = var.workload_version
  }
}
