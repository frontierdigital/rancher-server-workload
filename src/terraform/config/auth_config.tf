resource "azuread_application" "authentication" {
  display_name = "Rancher Server authentication"
  owners       = [data.azuread_client_config.main.object_id]

  web {
    redirect_uris = ["${var.rancher_server_api_url}/verify-auth-azure"]
  }

  required_resource_access {
    resource_app_id = "00000003-0000-0000-c000-000000000000" # Microsoft Graph

    resource_access {
      id   = "7ab1d382-f21e-4acd-a863-ba3e13f7da61" # Directory.Read.All
      type = "Role"
    }

    resource_access {
      id   = "5b567255-7703-4780-807c-7be8301ae99b" # Group.Read.All
      type = "Role"
    }

    resource_access {
      id   = "df021288-bdef-4463-88db-98f22de89214" # User.Read.All
      type = "Role"
    }
  }
}

resource "azuread_application_password" "authentication" {
  application_object_id = azuread_application.authentication.object_id
}

resource "rancher2_auth_config_azuread" "main" {
  application_id     = azuread_application.authentication.application_id
  application_secret = azuread_application_password.authentication.value

  auth_endpoint  = "https://login.microsoftonline.com/${data.azuread_client_config.main.tenant_id}/oauth2/v2.0/authorize"
  token_endpoint = "https://login.microsoftonline.com/${data.azuread_client_config.main.tenant_id}/oauth2/v2.0/token"
  graph_endpoint = "https://graph.microsoft.com"

  tenant_id   = data.azuread_client_config.main.tenant_id
  rancher_url = "${var.rancher_server_api_url}/verify-auth-azure"
}
