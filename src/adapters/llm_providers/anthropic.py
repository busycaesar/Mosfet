from .base import LLMProvider
from anthropic import Anthropic, BadRequestError, omit
import json
from types import SimpleNamespace

class AnthropicLLM(LLMProvider):
    def __init__(self, api_key, model, max_tokens):
        self.model = model
        self.max_tokens = max_tokens
        self.client = Anthropic(api_key=api_key)

    def infer(self, messages, tools):
        system_message, user_llm_conversations = self._split_system_messages(messages)

        try:
            raw_response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system_message,
                messages=user_llm_conversations,
                tools=self._convert_tools_declaration(tools) or omit
            )
        except BadRequestError as error:
            self._raise_if_tools_not_supported(error)
            raise

        response_object = self._format_generated_response(raw_response)

        return SimpleNamespace(
            **response_object,
            raw_response=raw_response
        )    

    def format_llm_response(self, generated_response):
        return {
            "role": "assistant",
            "content": generated_response.raw_response.content
        }
    
    def format_tool_call_results(self, tool_call_results):
        return [{
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_call_id,
                    "content": result
                }
                for tool_call_id, result in tool_call_results
            ]
        }]


    def _split_system_messages(self, messages):
        
        def _filter_messages_content(messages, filter_logic):
            return [message for message in messages if filter_logic(message)]
        
        _messages = _filter_messages_content(messages, lambda message: message.get("role") == "system")
        system_messages = [message["content"] for message in _messages]
        system_message_text = "\n\n".join(system_messages)

        other_messages = _filter_messages_content(messages, lambda message: message.get("role") != "system")

        return system_message_text or None, other_messages
    
    def _convert_tools_declaration(self, tools_description):
        converted_tools_declaration = []

        for tool in tools_description:

            function = tool["function"]
            
            entry = {
                "name": function["name"],
                "description": function["description"],
                "input_schema": function["parameters"]
            }

            if "strict" in function:
                entry["strict"] = function["strict"]

            converted_tools_declaration.append(entry)

        return converted_tools_declaration
    
    def _format_generated_response(self, raw_response):
        _response = [response.text for response in raw_response.content if response.type == "text"]
        response_text = "".join(_response)

        tool_calls = [
            SimpleNamespace(
                id=block.id,
                function=SimpleNamespace(
                    name=block.name,
                    arguments=json.dumps(block.input)
                )
            )
            for block in raw_response.content
            if block.type == "tool_use"
        ]

        return {
            "content": response_text or None,
            "tool_calls": tool_calls
        }