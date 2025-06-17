output "role_arn" {
  value = module.lambda_iam_role.iam_role_arn
}
output "api_endpoint" {
  value = module.api_gateway.api_endpoint
}
