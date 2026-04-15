# ---------------------------------------------------------------------------
# Hosted zone
# ---------------------------------------------------------------------------
resource "aws_route53_zone" "webbpulse" {
  name = "webbpulse.com"
}

# ---------------------------------------------------------------------------
# Apex redirect: webbpulse.com → www.webbpulse.com via S3 website bucket
# ---------------------------------------------------------------------------
resource "aws_route53_record" "apex_a" {
  zone_id = aws_route53_zone.webbpulse.zone_id
  name    = "webbpulse.com"
  type    = "A"

  alias {
    name                   = aws_s3_bucket_website_configuration.apex_redirect.website_endpoint
    zone_id                = aws_s3_bucket.apex_redirect.hosted_zone_id
    evaluate_target_health = false
  }
}

# ---------------------------------------------------------------------------
# Google Workspace email records
# ---------------------------------------------------------------------------
resource "aws_route53_record" "mx" {
  zone_id = aws_route53_zone.webbpulse.zone_id
  name    = "webbpulse.com"
  type    = "MX"
  ttl     = 300

  records = [
    "1 smtp.google.com.",
  ]
}

resource "aws_route53_record" "spf" {
  zone_id = aws_route53_zone.webbpulse.zone_id
  name    = "webbpulse.com"
  type    = "TXT"
  ttl     = 300

  records = [
    "v=spf1 include:_spf.google.com ~all",
  ]
}

resource "aws_route53_record" "dmarc" {
  zone_id = aws_route53_zone.webbpulse.zone_id
  name    = "_dmarc.webbpulse.com"
  type    = "TXT"
  ttl     = 300

  records = [
    "v=DMARC1; p=none; rua=mailto:tyler@webbpulse.com",
  ]
}

# DKIM - add after retrieving the key from Google Admin Console:
# Apps → Google Workspace → Gmail → Authenticate email → Generate new record
# resource "aws_route53_record" "dkim" {
#   zone_id = aws_route53_zone.webbpulse.zone_id
#   name    = "google._domainkey.webbpulse.com"
#   type    = "TXT"
#   ttl     = 300
#   records = ["v=DKIM1; k=rsa; p=<key from Google Admin Console>"]
# }

# ---------------------------------------------------------------------------
# Domain registration — nameservers kept in sync with the hosted zone
# ---------------------------------------------------------------------------
resource "aws_route53domains_registered_domain" "webbpulse" {
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
