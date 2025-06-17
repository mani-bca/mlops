region                  = "us-east-1"
lambda_role_name = "lambda-ML-role"
lambda_policy_arns = [
  "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
]
#####lambda
function_name = "ML-lambda"
image_uri     = "676206899900.dkr.ecr.us-east-1.amazonaws.com/dev/lambda:hello"
timeout       = 30
memory_size   = 128

architectures = ["x86_64"]

environment_variables = {
  BUCKET_NAME = "lambda-code-bucket-ddd"
}

tags = {
  Environment = "production"
  Project     = "ml ops"
  Owner       = "devops-team"
}