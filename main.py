import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    system_prompt = """
    You are a helpful AI coding agent.
    
    When a user aks a question or makes a request, make a function call plan. You can perform the following operations:
    
    - List files and directories
    - Read the content of a file
    - Write to a file (create or update)
    - Run a Python file with optional arguments
    
    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons. 
    """

    client = genai.Client(api_key=api_key)

    if len(sys.argv) < 2:
        print("I need a prompt to provide you with a response!")
        sys.exit(1)
    prompt = sys.argv[1]

    verbose_flag = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose_flag = True
    prompt = sys.argv[1]

    messages = [
        types.Content(role='user', parts=[types.Part(text=prompt)])
        ]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )

    config = types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
    )


    response = client.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=prompt,
        config=config
    )

    if response is None or response.usage_metadata is None:
        print("Response is malformed")
        return
    if verbose_flag:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    if response.function_calls:
        for function_call_part in response.function_calls:
            print(f'Calling function: {function_call_part.name} ({function_call_part.args})')
    else:
        print(response.text)




# print(get_files_info("calculator"))
main()