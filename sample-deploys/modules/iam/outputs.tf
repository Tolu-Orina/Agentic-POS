output "codebuild_deploy_role_arn" {
  description = "ARN of the CodeBuild deploy role"
  value       = aws_iam_role.codebuild_deploy.arn
}

output "codebuild_deploy_role_name" {
  description = "Name of the CodeBuild deploy role"
  value       = aws_iam_role.codebuild_deploy.name
}

