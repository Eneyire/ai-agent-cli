import argparse
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from functions.call_function import available_functions
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

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0,
        tools=available_functions,
    )

    if response.usage is None:
        raise RuntimeError("Failed to get usage information from the API")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
        print(f"Total tokens: {response.usage.total_tokens}")
        print(f"Response: \n{response.choices[0].message.content}\n")
    else:
        print(f"Response: \n{response.choices[0].message.content}\n")

    message = response.choices[0].message

    if message.tool_calls:
        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")
            print(f"Calling function: {tool_call.function.name}({function_args})")

    if message.tool_calls is None:
        print(f"There were no function calls.\nContent: \n{message.content}\n")


if __name__ == "__main__":
    main()
