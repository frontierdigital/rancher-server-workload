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

variable "node_count" {
  type = number
}

variable "short_location" {
  type = string
}

variable "tags" {
  type    = map(string)
  default = {}
}

variable "vm_size" {
  type = string
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
