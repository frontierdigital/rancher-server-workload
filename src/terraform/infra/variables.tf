variable "cidrsubnet_netnum" {
  type = number
}

variable "cidrsubnet_newbits" {
  type = number
}

variable "environment" {
  type = string
}

variable "kubernetes_version" {
  type = string
}

variable "location" {
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
