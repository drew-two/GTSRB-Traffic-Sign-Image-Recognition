variable "bucket_name" {
    type = string
    description = "S3 bucket name"
}

variable "tags" {
    description = "Tags for S3 bucket"
    default = "mlops-final"
}