# ---------------------------------------------------------------------------
# Apex redirect bucket — webbpulse.com → www.webbpulse.com
# Bucket name must match the domain for S3 website hosting to work.
# ---------------------------------------------------------------------------
resource "aws_s3_bucket" "apex_redirect" {
  bucket = "webbpulse.com"
}

resource "aws_s3_bucket_website_configuration" "apex_redirect" {
  bucket = aws_s3_bucket.apex_redirect.id

  redirect_all_requests_to {
    host_name = "www.webbpulse.com"
    protocol  = "https"
  }
}

resource "aws_s3_bucket_public_access_block" "apex_redirect" {
  bucket = aws_s3_bucket.apex_redirect.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}
