resource "aws_s3_bucket" "webbpulse_com_apex" {
  bucket = "webbpulse.com"
}

resource "aws_s3_bucket_website_configuration" "webbpulse_com_apex" {
  bucket = aws_s3_bucket.webbpulse_com_apex.id

  redirect_all_requests_to {
    host_name = "www.webbpulse.com"
    protocol  = "https"
  }
}

resource "aws_s3_bucket_public_access_block" "webbpulse_com_apex" {
  bucket = aws_s3_bucket.webbpulse_com_apex.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}
