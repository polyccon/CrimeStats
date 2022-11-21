data "aws_iam_policy_document" "lambda_assume_role" {

    version = "2012-10-17"

    statement {
        sid = ""

        actions = [
            "sts:AssumeRole",
        ]

        principals {
            type = "Service"
            identifiers = [
                "lambda.amazonaws.com",
            ]
        }

        effect = "Allow"
    }

}

resource "aws_iam_role" "lambda_role" {
    name   = "crime_stats_lambda_function_role"
    assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

data "aws_iam_policy_document" "iam_policy_for_lambda_logs" {

    version = "2012-10-17"

    statement {
        sid = ""

        actions = [
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents"
        ]

        resources = ["arn:aws:logs:*:*:*"]

        effect = "Allow"
    }

}

resource "aws_iam_policy" "iam_policy_for_lambda" {
    name         = "aws_iam_policy_for_terraform_aws_lambda_role"
    path         = "/"
    description  = "AWS IAM Policy for managing aws lambda role"
    policy = data.aws_iam_policy_document.iam_policy_for_lambda_logs.json

}

resource "aws_iam_role_policy_attachment" "attach_iam_policy_to_iam_role" {
    role        = aws_iam_role.lambda_role.name
    policy_arn  = aws_iam_policy.iam_policy_for_lambda.arn
}