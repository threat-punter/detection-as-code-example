# sumologic_connection docs: https://registry.terraform.io/providers/SumoLogic/sumologic/latest/docs/resources/connection

# Read the Tines webhook URL from the environment variable TF_VAR_TINES_WEBHOOK_URL_FOR_SUMOLOGIC_ALERTS.
variable "TINES_WEBHOOK_URL_FOR_SUMOLOGIC_ALERTS" {
  type        = string
  description = "Tines webhook URL to send Sumo Logic alerts to."
  sensitive   = true
}

# Sumo Logic webhook connection to send alerts to Tines.
resource "sumologic_connection" "tines_webhook" {
  type            = "WebhookConnection"
  name            = "Tines Webhook - Create GitHub Issues from Sumo Logic Alerts."
  description     = "Connection to send alert payloads to Tines webhook."
  url             = var.TINES_WEBHOOK_URL_FOR_SUMOLOGIC_ALERTS
  custom_headers  = { "Content-Type" : "application/json" }
  # The default payload (JSON string) from Sumo Logic to send to Tines webhook.
  default_payload = <<JSON
{
  "rule.name": "{{Name}}",
  "rule.description": "{{Description}}",
  "query.url": "{{QueryURL}}",
  "query": "{{Query}}",
  "trigger.range": "{{TriggerTimeRange}}",
  "trigger.name": "{{TriggerTime}}",
  "alert.payload": "{{ResultsJson}}"
}
JSON
  webhook_type    = "Webhook"
}
