variable "standard_name" {
  type = string
}

variable "standard_description" {
  type = string
}

variable "standard_query" {
  type = string
}

variable "standard_folder" {
  type = string
}

variable "tines_webhook" {
  type    = string
  default = null
}

variable "standard_trigger_type" {
  type    = string
  default = "Critical"
}

variable "tines_webhook_override" {
  type    = string
  default = null
}
