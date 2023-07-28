variable "bootstrap_password" {
  type = string
}

variable "environment" {
  type = string
}

variable "location" {
  type = string
}

variable "rancher_server_api_url" {
  type = string
}

variable "rancher_server_key_vault_id" {
  type = string
}

variable "set" {
  type = string
}

variable "short_location" {
  type = string
}

variable "tags" {
  type    = map(string)
  default = {}
}

variable "workload_name" {
  type = string
}

variable "workload_type" {
  type = string
}

variable "workload_version" {
  type = string
}

variable "zone" {
  type = string
}
