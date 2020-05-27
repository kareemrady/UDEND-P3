data "aws_iam_policy_document" "redshift" {
    statement {
        actions   = ["sts:AssumeRole"]
        principals {
            type        = "Service"
            identifiers = ["redshift.amazonaws.com"]
    }
  }
}