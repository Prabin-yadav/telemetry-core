terraform {
  required_version = ">= 1.0"
}

resource "local_file" "fleet_env" {
  content  = "BROKER=localhost:30095\n"
  filename = "${path.module}/fleet.env"
}

output "broker_config" {
  description = "The generated broker configuration"
  value       = "BROKER=localhost:30095"
}
