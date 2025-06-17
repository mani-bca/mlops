module "lambda_iam_role" {
  source = "../modules/iam_role"

  role_name          = var.lambda_role_name
  policy_arns        = var.lambda_policy_arns
  tags               = var.tags
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }]
  })

  inline_policy = jsonencode({
     Version: "2012-10-17",
     Statement: [
      {
        "Effect": "Allow",
        "Action": [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        "Resource": "arn:aws:logs:*:*:*"
      }
    ]
  })
}

module "lambda_docker" {
  source = "../modules/lamdadocker"

  function_name         = var.function_name
  role_arn              = module.lambda_iam_role.iam_role_arn
  image_uri             = var.image_uri
  timeout               = var.timeout
  memory_size           = var.memory_size
  architectures         = var.architectures
  environment_variables = var.environment_variables
  tags                  = var.tags
}

module "apigateway" {
    source = "./modules/api_gateway"
    api_name = "hellowrold-test"
    route_key = "GET /hello"
    lambda_invoke_arn = module.lambda_docker.lambda_invoke_arn
    lambda_arn = module.lambda_docker.lambda_arn

}
