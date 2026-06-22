"""
client.py
Provides a seamless, OpenAI-compatible interface for the end-user.
"""

from typing import Dict, Any, Optional
from .coordinator import Coordinator

class SakanaFuguClient:
    """
    Main entry point for the Sakana Fugu API.
    Handles user configuration, compliance settings, and executes requests.
    """
    
    def __init__(self, api_key: str, version: str = "standard"):
        # Initialize client with API key and selected version (standard or ultra)
        self.api_key = api_key
        self.version = version
        self.coordinator = Coordinator()
        
        # Max context window depending on the version
        self.max_context = 272000 if version.lower() == "ultra" else 32000
        print(f"Initialized Sakana Fugu Client ({self.version.capitalize()}). Context limit: {self.max_context}")

    def chat_completions_create(self, messages: list, stream: bool = False) -> Dict[str, Any]:
        """
        Simulates an OpenAI-compatible endpoint.
        """
        # Extract user prompt from the messages format
        user_prompt = next((msg['content'] for msg in reversed(messages) if msg['role'] == 'user'), "")
        
        if not user_prompt:
            raise ValueError("No user prompt found in messages.")

        # Trigger the multi-agent orchestration
        orchestration_data = self.coordinator.orchestrate(user_prompt)
        
        # Format the response in a standard API structure
        response = {
            "id": "fugu-chat-12345",
            "object": "chat.completion",
            "model": f"sakana-fugu-{self.version}",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": orchestration_data["content"]
                    },
                    "finish_reason": "stop"
                }
            ],
            # Expose reasoning tree for developers (Advanced Logging)
            "fugu_metadata": {
                "iterations": orchestration_data["iterations"],
                "reasoning_tree": orchestration_data["reasoning_tree"]
            }
        }
        
        return response
