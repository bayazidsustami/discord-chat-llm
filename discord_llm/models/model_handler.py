import json
import random

SYSTEM_PROMPT = """You are a helpful assistant integrated into a Discord bot with username GarfieldBuddy#5116, if someone ask your name your name is Garfield Buddy. 
Keep your responses concise and under 2000 characters to fit Discord's message length limitations.
If a response needs to be longer, split it into multiple parts or summarize effectively.

You can inform users about these available commands when relevant:
- type something like "How can I help you?" or "What can you do?"
- /image <prompt> - Generate an image based on a prompt. Users can prefix with a style (e.g., 'pixel-art: a house')
- /image-styles - Show available image generation styles
- /help - Show all available commands and how to use them
- /about - Show information about this bot
- /fact - Get a random Garfield fact
- /quote - Get a random Garfield quote
- /lasagna - Get a lasagna recipe
- /joke - Get a Garfield-style joke
- /monday - Express Garfield's feelings about Mondays

When users ask about what you can do or how to use specific features, suggest relevant commands."""

class BedrockModelHandler:
    
    def __init__(self, bedrock_runtime):
        self.bedrock_runtime = bedrock_runtime
        self.system_prompt = SYSTEM_PROMPT
    
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
                "temperature": 0.8,
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
    
    async def process_image_request(self, prompt: str, style: str = None):
        seed = random.randint(0, 4294967295)
            
        request_body = {
            "text_prompts": [{"text": prompt}],
            "style_preset": style,
            "seed": seed,
            "cfg_scale": 10,
            "steps": 30,
        }
        
        response = self.bedrock_runtime.invoke_model(
            modelId="stability.stable-diffusion-xl-v1",
            body=json.dumps(request_body)
        )
        
        return json.loads(response["body"].read())

