/*
name = "Administrator Role Assigned to Non-Admin User Account"
creation_date = "2023/07/22"
updated_date = "2023/07/22"
maturity = "Production"
version = "1.0.0"
rule_id: "97d6c856-93e8-40e3-9af7-f797a5c1435b"
platform: "Sumo Logic"
*/

module "rule_okta_administrator_role_assigned_to_non_admin_user_account" {
  source                 = "./modules/sumo_monitor"
  standard_name          = "Administrator Role Assigned to Non-Admin User Account"
  standard_description   = "Identifies when an administrator role is assigned to a non-admin Okta user account i.e. a standard user account that does not follow our company's admin account naming conventions. Investigate using playbook PB-100."
  standard_query         = <<EOF
_sourceCategory="okta" user.account.privilege.grant
| where eventType="user.account.privilege.grant" AND !(%"target[0].alternateId" matches /^admin\./)
EOF
  standard_folder        = sumologic_monitor_folder.detections.id
  tines_webhook          = sumologic_connection.tines_webhook.id
  tines_webhook_override = <<EOF
{
  "rule.name": "{{Name}}",
  "rule.description": "{{Description}}",
  "query.url": "{{QueryURL}}",
  "query": "{{Query}}",
  "trigger.range": "{{TriggerTimeRange}}",
  "trigger.name": "{{TriggerTime}}",
  "alert.payload": "{{ResultsJson}}"
}
EOF
}
