provider "azuread" {
}

provider "azurerm" {
  features {}
}

provider "rancher2" {
  alias = "bootstrap"

  api_url   = var.rancher_server_api_url
  bootstrap = true
  insecure  = true
}

provider "rancher2" {
  api_url   = var.rancher_server_api_url
  token_key = rancher2_bootstrap.main.token
  insecure  = true
}
