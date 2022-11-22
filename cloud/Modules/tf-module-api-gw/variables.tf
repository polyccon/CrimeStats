variable api_gw_name {
    default = "crime-stats-http"
    type = string
    description = "Api gateway name"
}

variable api_gw_protocol_type {
    default = "HTTP"
    type = string
    description = "Api gateway protocol type"    
}

variable api_gw_stage_name {
    default = "serverless_lambda_stage"
    type = string
    description = "Api gateway stage name"       
}

variable api_gw_integration_type {
    default = "AWS_PROXY"
    type = string
    description = "Api gateway integration type"     
}

variable api_gw_integration_method {
    default = "POST"
    type = string
    description = "Api gateway integration method"     
}

variable api_gw_route_key {
    default = "GET /data/{location}"
    type = string
    description = "Api gateway crime stats route key"    
}

variable api_gw_retention_in_days {
    default = 30
    type = number
    description = "Api gateway crime stats retention in days"      
}