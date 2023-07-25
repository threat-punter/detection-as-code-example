# sumologic_monitor docs: https://registry.terraform.io/providers/SumoLogic/sumologic/latest/docs/resources/monitor

terraform {
  required_providers {
    sumologic = {
      source  = "sumoLogic/sumologic"
      version = "2.24.0"
    }
  }
  required_version = ">= 1.5.2"
}

# Sumo Logic Monitor (alert) resource.
resource "sumologic_monitor" "alert" {
  name                      = var.standard_name
  description               = var.standard_description
  type                      = "MonitorsLibraryMonitor"
  parent_id                 = var.standard_folder
  is_disabled               = false
  notification_group_fields = ["_messageid"]
  content_type              = "Monitor"
  # Monitor type is logs query monitor.
  monitor_type = "Logs"
  queries {
    row_id = "A"
    query  = var.standard_query
  }
  # The "triggers" block is deprecated. Use the trigger_conditions block instead.
  # Trigger conditions docs: https://registry.terraform.io/providers/SumoLogic/sumologic/latest/docs/resources/monitor#the-trigger_conditions-block
  trigger_conditions {
    logs_static_condition {
      critical {
        time_range = "1h"
        alert {
          threshold_type = "GreaterThanOrEqual"
          threshold      = 1
        }
        resolution {
          threshold         = 0
          threshold_type    = "LessThanOrEqual"
          resolution_window = "1h"
        }
      }
    }
  }
  notifications {
    notification {
      connection_type  = "Webhook"
      connection_id    = var.tines_webhook
      payload_override = var.tines_webhook_override
    }
    run_for_trigger_types = [var.standard_trigger_type]
  }
}
