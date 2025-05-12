import json

class BedrockModelHandler:
    
    def __init__(self, bedrock_runtime, system_prompt):
        self.bedrock_runtime = bedrock_runtime
        self.system_prompt = system_prompt
    
    def get_payload(self, content, model_id):
        model_id_lower = model_id.lower()
        
        if "anthropic" in model_id_lower or "claude" in model_id_lower:
            return {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "system": self.system_prompt,
                "messages": [
                    {"role": "user", "content": content}
                ]
            }
        elif "llama" in model_id_lower:
            return {
                "prompt": f"{self.system_prompt}\n\nUser: {content}\nAssistant:",
                "max_gen_len": 1000,
                "temperature": 0.7,
            }
        elif "titan" in model_id_lower:
            return {
                "inputText": f"{self.system_prompt}\n\nUser: {content}",
                "textGenerationConfig": {
                    "maxTokenCount": 1000,
                    "temperature": 0.7,
                    "topP": 0.9,
                }
            }
        else:  # Default fallback format
            return {
                "prompt": content,
                "max_tokens": 1000,
                "temperature": 0.7,
                "system_prompt": self.system_prompt,
            }
    
    def parse_response(self, response, model_id):
        response_body = json.loads(response.get("body").read())
        model_id_lower = model_id.lower()
        
        if "anthropic" in model_id_lower or "claude" in model_id_lower:
            if "completion" in response_body:
                return response_body.get("completion")
            elif "content" in response_body:
                if isinstance(response_body.get("content"), list):
                    return response_body.get("content")[0].get("text")
                return response_body.get("content")
        elif "llama" in model_id_lower:
            return response_body.get("generation", "")
        elif "titan" in model_id_lower:
            return response_body.get("results", [{}])[0].get("outputText", "")
        else:
            for key in ["text", "generated_text", "answer", "response", "output"]:
                if key in response_body:
                    return response_body[key]
                    
        return str(response_body)
    
    async def process_request(self, content, model_id):
        payload = self.get_payload(content, model_id)
        
        response = self.bedrock_runtime.invoke_model(
            modelId=model_id,
            body=json.dumps(payload)
        )
        
        return self.parse_response(response, model_id)
