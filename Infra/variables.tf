#Secret VARS IN TFVARS FILE
variable "AWS_KEY_ID" {}
variable "AWS_SECRET" {}
variable "RSHIFT_USER" {}
variable "RSHIFT_PASS" {}

# ENV Specific Variables
variable "region" {
  type    = string
  default = "us-west-2"
}

variable "envtag" {
  type    = string
  default = "UDEND_Project3"
}

# REDSHIFT Variables
variable "redshift_clusterID" {
  type    = string
  default = "sparkify-cluster"
}

variable "redshift_node_type" {
  type    = string
  default = "dc2.large"
}

variable "redshift_cluster_type" {
  type    = string
  default = "multi-node"
}

variable "redshift_num_nodes" {
  type    = number
  default = 4
}

variable "redshift_db_name" {
  type    = string
  default = "sparkify"
}

variable "redshift_port" {
  type    = number
  default = 5439
}

