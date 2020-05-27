output "rs_endpoint" {
  value = aws_redshift_cluster.rscluster.endpoint
}

output "role_arn" {
  value = aws_iam_role.redshift.arn
}
