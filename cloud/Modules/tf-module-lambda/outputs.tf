output "aws_lambda_invoke_arn_output" {
  description = "Crime stats lambda invoke arn"
  value       = aws_lambda_function.main.invoke_arn
}

output "aws_lambda_function_name_output" {
  description = "Crime stats lambda function name"
  value       = var.lambda_function_name
}