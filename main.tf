terraform {
  required_providers {
    # Sumo Logic Provider docs: https://registry.terraform.io/providers/SumoLogic/sumologic/latest/docs
    sumologic = {
      source  = "sumoLogic/sumologic"
      version = "2.24.0"
    }
  }
  # Required Terraform version.
  required_version = ">= 1.5.2"
}

# Setup authentication variables. Docs: https://registry.terraform.io/providers/SumoLogic/sumologic/latest/docs#authentication
variable "SUMOLOGIC_ACCESSID" {
  type        = string
  description = "Sumo Logic Access ID"
}
variable "SUMOLOGIC_ACCESSKEY" {
  type        = string
  description = "Sumo Logic Access Key"
  sensitive   = true
}

# Configure the Sumo Logic Provider
provider "sumologic" {
  access_id   = var.SUMOLOGIC_ACCESSID
  access_key  = var.SUMOLOGIC_ACCESSKEY
  environment = "us1"
}
