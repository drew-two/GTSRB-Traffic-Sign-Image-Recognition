# Create S3 bucket for models

resource "aws_s3_bucket" "s3_bucket" {
    bucket  = var.bucket_name
    acl     = "private"
    tags    = {
        CreatedBy = var.tags
    }
}

output "bucket" {
    value = aws_s3_bucket.s3_bucket.bucket
}