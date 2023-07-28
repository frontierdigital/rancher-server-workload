terraform {
  required_version = "~> 1.5"

  backend "azurerm" {
    container_name = "terraform"
  }

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.65"
    }
  }
}
