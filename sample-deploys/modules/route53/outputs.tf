output "zone_id" {
  description = "Route53 hosted zone ID"
  value       = local.zone_id
}

output "name_servers" {
  description = "Route53 name servers"
  value       = var.domain_name != "" && length(data.aws_route53_zone.main) > 0 ? data.aws_route53_zone.main[0].name_servers : []
}

