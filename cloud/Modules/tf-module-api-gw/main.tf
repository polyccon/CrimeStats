resource "aws_apigatewayv2_api" "main" {
  name          = var.api_gw_name
  protocol_type = var.api_gw_protocol_type
}

resource "aws_apigatewayv2_stage" "main" {
  api_id = aws_apigatewayv2_api.main.id

  name        = var.api_gw_stage_name
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.main.arn

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

resource "aws_apigatewayv2_integration" "main" {
  api_id = aws_apigatewayv2_api.main.id

  integration_uri    = var.aws_lambda_invoke_arn
  integration_type   = var.api_gw_integration_type
  integration_method = var.api_gw_integration_method
}

resource "aws_apigatewayv2_route" "main" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = var.api_gw_route_key
  target    = "integrations/${aws_apigatewayv2_integration.main.id}"
}

resource "aws_cloudwatch_log_group" "main" {
  name = "/aws/api_gw/${aws_apigatewayv2_api.main.name}"

  retention_in_days = var.api_gw_retention_in_days
}

resource "aws_lambda_permission" "main" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = var.aws_lambda_function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}


