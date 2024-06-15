resource "aws_dynamodb_table" "this" {
  name           = "user_table"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "email"

  attribute {
    name = "email"
    type = "S"
  }

  tags = {
    Name        = "dynamodb-table-1"
    Environment = "production"
  }
}

output "aws_dynamodb_table_arn" {
  value = aws_dynamodb_table.this.arn
}