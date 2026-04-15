# ---------------------------------------------------------------------------
# Apex redirect bucket — webbpulse.com → www.webbpulse.com
# Bucket name must match the domain for S3 website hosting to work.
# Created in us-east-1 (existing); new buckets should use var.aws_region.
# ---------------------------------------------------------------------------
resource "aws_s3_bucket" "apex_redirect" {
  provider = aws.us_east_1
  bucket   = "webbpulse.com"
}

resource "aws_s3_bucket_website_configuration" "apex_redirect" {
  provider = aws.us_east_1
  bucket   = aws_s3_bucket.apex_redirect.id

  redirect_all_requests_to {
    host_name = "www.webbpulse.com"
    protocol  = "https"
  }
}

resource "aws_s3_bucket_public_access_block" "apex_redirect" {
  provider = aws.us_east_1
  bucket   = aws_s3_bucket.apex_redirect.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}
