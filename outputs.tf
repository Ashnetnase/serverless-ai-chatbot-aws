output "api_url" {
  description = "API Gateway endpoint URL"
  value       = aws_apigatewayv2_api.chatbot_api.api_endpoint
}

output "chatbot_endpoint" {
  description = "Full chatbot POST endpoint"
  value       = "${aws_apigatewayv2_api.chatbot_api.api_endpoint}/chat"
}

output "dynamodb_table_name" {
  description = "DynamoDB chat messages table"
  value       = aws_dynamodb_table.chat_messages.name
}

output "lambda_function_name" {
  description = "Lambda function name"
  value       = aws_lambda_function.chatbot.function_name
}