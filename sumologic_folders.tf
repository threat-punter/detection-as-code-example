# sumologic_monitor_folder docs: https://registry.terraform.io/providers/SumoLogic/sumologic/latest/docs/resources/monitor_folder

# Sumo Logic "Monitors" folder for detection rules.
resource "sumologic_monitor_folder" "detections" {
  name        = "Detections"
  description = "A folder for our detection rules."
}
