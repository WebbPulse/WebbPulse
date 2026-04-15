output "aws_account_id" {
  description = "AWS account ID Terraform is deploying into"
  value       = data.aws_caller_identity.current.account_id
}

output "aws_region" {
  description = "AWS region being deployed to"
  value       = data.aws_region.current.name
}

output "webbpulse_zone_id" {
  description = "Route53 hosted zone ID for webbpulse.com"
  value       = aws_route53_zone.webbpulse.zone_id
}

output "webbpulse_name_servers" {
  description = "Authoritative name servers for webbpulse.com"
  value       = aws_route53_zone.webbpulse.name_servers
}
