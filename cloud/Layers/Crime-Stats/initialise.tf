provider "aws" {
  region = "eu-west-2"
}

terraform {
  
  required_version = ">= 1.3.0"

  required_providers {
    aws = {
      version = "4.28.0"
      source  = "hashicorp/aws"
    }
  }
}