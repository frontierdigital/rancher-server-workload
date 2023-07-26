provider "azurerm" {
  features {}
}

module "resource_group" {
  source = "git::https://github.com/frontierdigital/resource-group-terraform-module//src?ref=v1.0.0-pre.a1c4ef6"

  environment      = var.environment
  identifier       = local.identifier
  location         = var.location
  set              = var.set
  tags             = var.tags
  workload_name    = var.workload_name
  workload_type    = var.workload_type
  workload_version = var.workload_version
  zone             = var.zone
}
