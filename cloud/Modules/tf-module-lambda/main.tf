resource "aws_lambda_function" "main" {
    filename                       = "${path.module}/${var.lambda_filename}"
    function_name                  = var.lambda_function_name
    role                           = aws_iam_role.lambda_role.arn
    handler                        = var.lambda_handler
    runtime                        = var.lambda_runtime
    depends_on                     = [aws_iam_role_policy_attachment.attach_iam_policy_to_iam_role]

    timeouts {
      create = var.lambda_timeout_create
    }
}
