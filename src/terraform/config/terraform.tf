terraform {
  required_version = "~> 1.5"

  backend "azurerm" {
    container_name = "terraform"
  }

  required_providers {
    azuread = {
      source  = "hashicorp/azuread"
      version = "~> 2.40"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.65"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
    rancher2 = {
      source  = "rancher/rancher2"
      version = "~> 3.1"
    }
  }
}
