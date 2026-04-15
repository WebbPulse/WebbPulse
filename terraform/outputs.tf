output "webbpulse_zone_id" {
  description = "Route53 hosted zone ID for webbpulse.com"
  value       = aws_route53_zone.webbpulse_com.zone_id
}

output "webbpulse_name_servers" {
  description = "Authoritative name servers for webbpulse.com"
  value       = aws_route53_zone.webbpulse_com.name_servers
}
