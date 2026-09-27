import argparse
import os
import sys
from typing import cast

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionToolParam

from functions.call_function import available_functions, call_function
from prompts import system_prompt


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument(
        "user_prompt", type=str, help="This is the prompt to be sent to the LLM"
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY not found in environment variables")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            temperature=0,
            tools=cast(list[ChatCompletionToolParam], available_functions),
        )

        if response.usage is None:
            raise RuntimeError("Failed to get usage information from the API")

        message = response.choices[0].message
        messages.append(message)

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
            print(f"Total tokens: {response.usage.total_tokens}")

        if not message.tool_calls:
            print(f"Response: \n{message.content}\n")
            return

        for tool_call in message.tool_calls:
            if tool_call.type != "function":
                raise RuntimeError(f"Unsupported tool call type: {tool_call.type}")
            result_message = call_function(tool_call, args.verbose)
            if not result_message.get("content"):
                raise RuntimeError(
                    f"Function {tool_call.function.name} returned empty content"
                )
            if args.verbose:
                print(f"-> {result_message['content']}")
            messages.append(result_message)

    print(
        "Error: Maximum number of model iterations (20) reached without a final response."
    )
    sys.exit(1)


if __name__ == "__main__":
    main()
