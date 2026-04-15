resource "aws_route53_zone" "webbpulse_com" {
  name = "webbpulse.com"
}

resource "aws_route53_record" "webbpulse_com_mx" {
  zone_id = aws_route53_zone.webbpulse_com.zone_id
  name    = ""
  type    = "MX"
  ttl     = 3600

  records = [
    "1 smtp.google.com.",
  ]
}

resource "aws_route53_record" "webbpulse_com_spf" {
  zone_id = aws_route53_zone.webbpulse_com.zone_id
  name    = ""
  type    = "TXT"
  ttl     = 3600

  records = [
    "v=spf1 include:_spf.google.com ~all",
  ]
}

resource "aws_route53_record" "webbpulse_com_dmarc" {
  zone_id = aws_route53_zone.webbpulse_com.zone_id
  name    = "_dmarc"
  type    = "TXT"
  ttl     = 3600

  records = [
    "v=DMARC1; p=none; rua=mailto:tyler@webbpulse.com",
  ]
}

# DKIM - add after retrieving the key from Google Admin Console:
# Apps → Google Workspace → Gmail → Authenticate email → Generate new record
# resource "aws_route53_record" "webbpulse_com_dkim" {
#   zone_id = aws_route53_zone.webbpulse_com.zone_id
#   name    = "google._domainkey"
#   type    = "TXT"
#   ttl     = 3600
#   records = ["v=DKIM1; k=rsa; p=<key from Google Admin Console>"]
# }

# Apex redirect: webbpulse.com → www.webbpulse.com via S3 website bucket
resource "aws_route53_record" "webbpulse_com_apex" {
  zone_id = aws_route53_zone.webbpulse_com.zone_id
  name    = ""
  type    = "A"

  alias {
    name                   = aws_s3_bucket_website_configuration.webbpulse_com_apex.website_endpoint
    zone_id                = aws_s3_bucket.webbpulse_com_apex.hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53domains_registered_domain" "webbpulse_com" {
  domain_name   = "webbpulse.com"
  auto_renew    = true
  transfer_lock = true

  name_server {
    name = "ns-580.awsdns-08.net"
  }
  name_server {
    name = "ns-1685.awsdns-18.co.uk"
  }
  name_server {
    name = "ns-112.awsdns-14.com"
  }
  name_server {
    name = "ns-1040.awsdns-02.org"
  }
}
