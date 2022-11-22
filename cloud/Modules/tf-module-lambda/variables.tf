variable "region" {
  default     = "eu-west-2"
  type        = string
  description = "AWS region to use"
}

variable lambda_filename {
  default = "../../code/zip/crime-stats.zip"
  type = string
  description = "Path for the lambda function zip file"
}

variable lambda_function_name {
  default     = "Crime_Stats_Lambda"
  type        = string
  description = "Lambda function name"    
}

variable lambda_handler {
  default     = "index.lambda_handler"
  type        = string
  description = "Lambda handler"  
}

variable lambda_runtime {
  default     = "python3.8"
  type        = string
  description = "Lambda runtime"  
}

variable lambda_timeout_create {
  default     = "5m"
  type        = string
  description = "Add custom timeout to lambda function"  
}