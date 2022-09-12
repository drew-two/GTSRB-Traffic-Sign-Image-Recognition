# Create Kinesis Data Stream

resource "aws_kinesis_stream" "stream" {
    name        = var.stream_name
    shard_count = var.shard_count
    retention_period = var.retention_period
}
