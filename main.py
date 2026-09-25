import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument(
        "user_prompt", type=str, help="This is the prompt to be sent to the LLM"
    )
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY not found in environment variables")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": args.user_prompt,
            }
        ],
    )

    if response.usage is None:
        raise RuntimeError("Failed to get usage information from the API")

    print(f"Prompt tokens: {response.usage.prompt_tokens}")
    print(f"Response tokens: {response.usage.completion_tokens}")
    print(f"Total tokens: {response.usage.total_tokens}")
    print(f"Response: \n{response.choices[0].message.content}")


if __name__ == "__main__":
    main()
