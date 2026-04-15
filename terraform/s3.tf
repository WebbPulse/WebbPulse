# Apex redirect was previously handled by an S3 website bucket aliased from
# Route53. That approach silently broke alias expansion outside us-east-1.
# The apex is now handled by the frontend CloudFront distribution with a
# CloudFront Function that 301-redirects webbpulse.com → www.webbpulse.com.
# The S3 bucket (webbpulse.com) can be deleted manually or via:
#   aws s3 rb s3://webbpulse.com --force
