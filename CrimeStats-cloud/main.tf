provider "aws" {
  region = var.region
}

resource "aws_lambda_function" "terraform_lambda_func" {
    filename                       = "${path.module}/package/crime-stats.zip"
    function_name                  = "Crime_Stats_Lambda"
    role                           = aws_iam_role.lambda_role.arn
    handler                        = "index.lambda_handler"
    runtime                        = "python3.8"
    depends_on                     = [aws_iam_role_policy_attachment.attach_iam_policy_to_iam_role]
}