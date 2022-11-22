module "lambda" {
    source = ""
}

module "apigw" {
    source = ""
    depends_on = [
        module.lambda
  ]
    aws_lambda_invoke_arn = module.lambda.aws_lambda_invoke_arn_output
    aws_lambda_function_name = module.lambda.aws_lambda_function_name_output
}
