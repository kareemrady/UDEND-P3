locals {
    common_tags = {
        Environment = var.envtag
    }
}


# Create IAM role & attach IAM policy 
resource "aws_iam_role" "redshift" {
    name = "redshift_role"
    description = "Allows Redshift clusters to call AWS services"
    assume_role_policy = data.aws_iam_policy_document.redshift.json
    tags = merge (
        local.common_tags,
        map(
            "Name", "RedShift Role"
        )
    )
}

resource "aws_iam_policy" "s3_read" {
  name        = "s3_Read_Only"
  description = "S3 Read Only Access"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:Get*",
                "s3:List*"
            ],
            "Resource": "*"
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "s3_read_redshift" {
    role       = aws_iam_role.redshift.name
    policy_arn = aws_iam_policy.s3_read.arn

}

# redshift cluster creation

resource "aws_redshift_cluster" "rscluster" {
  cluster_identifier                  = var.redshift_clusterID
  database_name                       = var.redshift_db_name
  master_username                     = var.RSHIFT_USER
  master_password                     = var.RSHIFT_PASS
  node_type                           = var.redshift_node_type
  cluster_type                        = var.redshift_cluster_type
  number_of_nodes                     = var.redshift_num_nodes
  port                                = var.redshift_port
  skip_final_snapshot                 = true
  automated_snapshot_retention_period = 0
  iam_roles                           = [aws_iam_role.redshift.arn]
  tags = merge(
      local.common_tags,
      map(
          "Name", "RedShift_Cluster_Project3"
      )
  )
}

# pull aws default vpc

resource "aws_default_vpc" "default" {}
# enable ingress access to redshift port
resource "aws_default_security_group" "default" {
    vpc_id = aws_default_vpc.default.id
    ingress {
        from_port = var.redshift_port
        to_port = var.redshift_port
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
    tags = {
        Enviornment = "Default_VPC"
        Name = "Redshift SG" 
    }
}
