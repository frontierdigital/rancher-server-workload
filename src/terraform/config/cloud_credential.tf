resource "azuread_application" "cluster_provisioner" {
  display_name = "Rancher Server cluster provisioner"
  owners       = [data.azuread_client_config.main.object_id]
}

resource "azuread_application_password" "cluster_provisioner" {
  application_object_id = azuread_application.cluster_provisioner.object_id
}

resource "azuread_service_principal" "cluster_provisioner" {
  application_id = azuread_application.cluster_provisioner.application_id
  owners         = [data.azuread_client_config.main.object_id]
}

resource "azurerm_role_assignment" "cluster_provisioner_contributor" {
  scope                = "/subscriptions/${data.azurerm_client_config.main.subscription_id}"
  role_definition_name = "Contributor"
  principal_id         = azuread_service_principal.cluster_provisioner.object_id
}

resource "rancher2_cloud_credential" "cluster_provisioner" {
  name        = azuread_application.cluster_provisioner.display_name
  description = "Service principal to be used for cluster provisioning"

  azure_credential_config {
    client_id       = azuread_application.cluster_provisioner.application_id
    client_secret   = azuread_application_password.cluster_provisioner.value
    subscription_id = data.azurerm_client_config.main.subscription_id
  }
}
