# Registry DS records without Route53 hosted-zone DNSSEC signing cause
# validating resolvers to SERVFAIL (breaking TXT, e.g. DKIM). Enable signing
# in the zone before associating delegation signers at the registrar.

# ---------------------------------------------------------------------------
# Hosted zone
# ---------------------------------------------------------------------------
resource "aws_route53_zone" "webbpulse" {
  name = "webbpulse.com"
}

# ---------------------------------------------------------------------------
# www — CloudFront distribution
# ---------------------------------------------------------------------------

resource "aws_route53_record" "www" {
  zone_id = aws_route53_zone.webbpulse.zone_id
  name    = "www.webbpulse.com"
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.frontend.domain_name
    zone_id                = aws_cloudfront_distribution.frontend.hosted_zone_id
    evaluate_target_health = false
  }
}

# ---------------------------------------------------------------------------
# api.webbpulse.com — App Runner custom domain
#
# App Runner issues its own TLS cert; these CNAMEs prove domain ownership.
# The second record (api) routes traffic to the App Runner service endpoint.
# ---------------------------------------------------------------------------

locals {
  apprunner_cert_validation_records = tolist(aws_apprunner_custom_domain_association.api.certificate_validation_records)
}

resource "aws_route53_record" "apprunner_cert_validation_0" {
  zone_id = aws_route53_zone.webbpulse.zone_id
  name    = local.apprunner_cert_validation_records[0].name
  type    = local.apprunner_cert_validation_records[0].type
  ttl     = 300
  records = [local.apprunner_cert_validation_records[0].value]
}

resource "aws_route53_record" "apprunner_cert_validation_1" {
  zone_id = aws_route53_zone.webbpulse.zone_id
  name    = local.apprunner_cert_validation_records[1].name
  type    = local.apprunner_cert_validation_records[1].type
  ttl     = 300
  records = [local.apprunner_cert_validation_records[1].value]
}

resource "aws_route53_record" "api" {
  zone_id = aws_route53_zone.webbpulse.zone_id
  name    = "api.webbpulse.com"
  type    = "CNAME"
  ttl     = 300
  records = [aws_apprunner_custom_domain_association.api.dns_target]
}

# ---------------------------------------------------------------------------
# Apex: webbpulse.com → same CloudFront distribution as www
# A CloudFront Function on the distribution redirects to www.webbpulse.com.
# ---------------------------------------------------------------------------
resource "aws_route53_record" "apex_a" {
  zone_id = aws_route53_zone.webbpulse.zone_id
  name    = "webbpulse.com"
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.frontend.domain_name
    zone_id                = aws_cloudfront_distribution.frontend.hosted_zone_id
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

resource "aws_route53_record" "dkim" {
  zone_id = aws_route53_zone.webbpulse.zone_id
  name    = "google._domainkey.webbpulse.com"
  type    = "TXT"
  ttl     = 300
  # Each list element is a separate TXT character-string (max 255 octets each).
  records = [
    "v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA21lP0OGD3iNqzHSvnhkzVjdLcgbSG7Is6YZUKCe8GCw5sqCoAWjGpZbYZlwkxVhrxmkoaI02j9MgxIX0sHBzDI2Lsp5MK3mHJ442ED67zbKDQRX42DMzIRdGYOLo35QK9R/BGK9D3uKvy8CWYStaPpFMqrclMiGWsgvbY8ym9EoZHEjUDG7hDuRNkjR1NSam",
    "gZe8sPI/9pb5gr243DfCtfqVvrweWGby8i96STkKYZlCERC6zYD4knjmvnKejmzgc4QDDIEqpOxEIaw9785RTAHDhEnxfSR84QVw1e/t3sFAs17Enz3MPTGKHVGFrRNxHH7+qFcJC/Xqj+K9FgzPpwIDAQAB",
  ]
}

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
