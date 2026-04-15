# ---------------------------------------------------------------------------
# Frontend — private S3 bucket served via CloudFront
#
# webbpulse.com and www.webbpulse.com both point at this distribution.
# A CloudFront Function 301-redirects the bare apex to www.
# 403/404 from S3 → index.html for client-side React Router.
#
# The backend is served independently via App Runner at api.webbpulse.com
# (see backend.tf + route53.tf). The frontend calls api.webbpulse.com
# directly — there is no proxying through CloudFront.
# ---------------------------------------------------------------------------

resource "aws_s3_bucket" "frontend" {
  bucket = "${local.prefix}-frontend"
}

resource "aws_s3_bucket_public_access_block" "frontend" {
  bucket                  = aws_s3_bucket.frontend.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_cloudfront_origin_access_control" "frontend" {
  name                              = "${local.prefix}-frontend"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

# Allow CloudFront (and only CloudFront) to read from the bucket
resource "aws_s3_bucket_policy" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid       = "AllowCloudFrontServicePrincipal"
      Effect    = "Allow"
      Principal = { Service = "cloudfront.amazonaws.com" }
      Action    = "s3:GetObject"
      Resource  = "${aws_s3_bucket.frontend.arn}/*"
      Condition = {
        StringEquals = {
          "AWS:SourceArn" = aws_cloudfront_distribution.frontend.arn
        }
      }
    }]
  })
}

resource "aws_cloudfront_distribution" "frontend" {
  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"
  aliases             = ["www.webbpulse.com", "webbpulse.com"]
  price_class         = "PriceClass_100" # US + Europe + Canada — cheapest tier

  origin {
    domain_name              = aws_s3_bucket.frontend.bucket_regional_domain_name
    origin_id                = "s3-frontend"
    origin_access_control_id = aws_cloudfront_origin_access_control.frontend.id
  }

  default_cache_behavior {
    target_origin_id       = "s3-frontend"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    compress               = true

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    min_ttl     = 0
    default_ttl = 86400
    max_ttl     = 31536000

    function_association {
      event_type   = "viewer-request"
      function_arn = aws_cloudfront_function.apex_redirect.arn
    }
  }

  # Serve index.html for all S3 misses (React Router handles the rest)
  custom_error_response {
    error_code            = 403
    response_code         = 200
    response_page_path    = "/index.html"
    error_caching_min_ttl = 10
  }

  custom_error_response {
    error_code            = 404
    response_code         = 200
    response_page_path    = "/index.html"
    error_caching_min_ttl = 10
  }

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate_validation.www.certificate_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
}

# ---------------------------------------------------------------------------
# CloudFront Function — redirect bare apex (webbpulse.com) to www
# ---------------------------------------------------------------------------

resource "aws_cloudfront_function" "apex_redirect" {
  name    = "${local.prefix}-apex-redirect"
  runtime = "cloudfront-js-2.0"
  publish = true

  code = <<-EOF
    async function handler(event) {
      const host = event.request.headers.host
        ? event.request.headers.host.value
        : "";
      if (host === "webbpulse.com") {
        return {
          statusCode: 301,
          statusDescription: "Moved Permanently",
          headers: {
            location: {
              value: "https://www.webbpulse.com" + event.request.uri,
            },
          },
        };
      }
      return event.request;
    }
  EOF
}

# ---------------------------------------------------------------------------
# App Runner custom domain — api.webbpulse.com → App Runner service
#
# App Runner provisions and manages the TLS certificate automatically.
# After apply, App Runner emits certificate_validation_records that must be
# present in Route53 for the domain to become active (see route53.tf).
# ---------------------------------------------------------------------------

resource "aws_apprunner_custom_domain_association" "api" {
  service_arn          = aws_apprunner_service.backend.arn
  domain_name          = "api.webbpulse.com"
  enable_www_subdomain = false
}
