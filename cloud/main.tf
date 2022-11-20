provider "aws" {
  region = var.region
}

terraform {

  required_version = ">= 1.3.0"

  required_providers {
    aws = {
      version = "4.28.0"
      source  = "hashicorp/aws"
    }
  }
}

resource "aws_lambda_function" "crime-stats" {
    filename                       = "${path.module}/code/zip/crime-stats.zip"
    function_name                  = "Crime_Stats_Lambda"
    role                           = aws_iam_role.lambda_role.arn
    handler                        = "index.lambda_handler"
    runtime                        = "python3.8"
    depends_on                     = [aws_iam_role_policy_attachment.attach_iam_policy_to_iam_role]

    timeouts {
      create = "5m"
    }
}

resource "aws_apigatewayv2_api" "lambda" {
  name          = "crime-stats-http"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "lambda" {
  api_id = aws_apigatewayv2_api.lambda.id

  name        = "serverless_lambda_stage"
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gw.arn

    format = jsonencode({
      requestId               = "$context.requestId"
      sourceIp                = "$context.identity.sourceIp"
      requestTime             = "$context.requestTime"
      protocol                = "$context.protocol"
      httpMethod              = "$context.httpMethod"
      resourcePath            = "$context.resourcePath"
      routeKey                = "$context.routeKey"
      status                  = "$context.status"
      responseLength          = "$context.responseLength"
      integrationErrorMessage = "$context.integrationErrorMessage"
      }
    )
  }
}

resource "aws_apigatewayv2_integration" "crime-stats" {
  api_id = aws_apigatewayv2_api.lambda.id

  integration_uri    = aws_lambda_function.crime-stats.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "crime-stats" {
  api_id = aws_apigatewayv2_api.lambda.id

  route_key = "GET /data/{location}"
  target    = "integrations/${aws_apigatewayv2_integration.crime-stats.id}"
}

resource "aws_cloudwatch_log_group" "api_gw" {
  name = "/aws/api_gw/${aws_apigatewayv2_api.lambda.name}"

  retention_in_days = 30
}

resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.crime-stats.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.lambda.execution_arn}/*/*"
}

