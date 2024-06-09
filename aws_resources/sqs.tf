resource "aws_sqs_queue" "app_queue" {
  name                      = "app_queue"
  delay_seconds             = 0 # using zero to get little to no delay.
  max_message_size          = 2048
  message_retention_seconds = 86400
  receive_wait_time_seconds = 5

  tags = {
    Environment = "production"
  }
}

output "queue_url" {
    value = aws_sqs_queue.app_queue.url
}