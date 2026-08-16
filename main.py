import os
import sys
import json
import requests
from dotenv import load_dotenv
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from call_function import call_function


class MockFunctionCall:
    """
    Structural adapter ensuring backward compatibility with the `call_function` utility.
    Simulates the behavior of the FunctionCall object from the official Google SDK,
    mitigating the need to refactor the underlying business logic for the REST layer.
    """
    def __init__(self, name, args):
        self.name = name
        self.args = args


def main():
    # Environment initialization and credential validation
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        print("API key missing!")
        sys.exit(1)

    system_prompt = """
You are an autonomous AI coding agent. Analyze the user's request, formulate a concise step-by-step plan, and execute it using the following tools:

# TOOLS
- `get_files_info`: List files and directories.
- `get_file_content`: Read file contents.
- `write_file`: Create or overwrite a file.
- `run_python_file`: Execute a Python script (arguments optional).

# CONSTRAINTS
- ALWAYS use strictly relative paths.
- NEVER include or specify the working directory with its name or '.' (it is auto-injected).
- Plan your function calls before executing them.
- NEVER call the exact same tool with the exact same arguments twice in a row.
- If you find a directory, your immediate next step MUST BE to inspect its contents using the appropriate tool.
    """

    # Processing CLI input arguments
    if len(sys.argv) < 2:
        print("I need a prompt to provide you with a response!")
        sys.exit(1)

    verbose_flag = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose_flag = True
    prompt = sys.argv[1]

    # Normalization of tool schemas into native dictionary structures.
    # Guards against serialization conflicts when utilizing Pydantic definitions (inherited from the SDK).
    raw_schemas = []
    for schema in [schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file]:
        if hasattr(schema, "model_dump"):
            raw_schemas.append(schema.model_dump(exclude_none=True))
        else:
            raw_schemas.append(schema)

    # Constructing the API payload structure.
    # A temperature of 0.0 enforces deterministic behavior, which is critical for agent reproducibility.
    payload_base = {
        "systemInstruction": {
            "parts": [{"text": system_prompt}]
        },
        "tools": [{"functionDeclarations": raw_schemas}],
        "generationConfig": {
            "temperature": 0.0
        }
    }

    # Initialization of the stateless conversation history.
    # Utilizing strictly raw data types (dict/list) to ensure flawless JSON serialization.
    messages = [{"role": "user", "parts": [{"text": prompt}]}]

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={api_key}"

    # Execution loop with a hard limit to prevent the agent from falling into an infinite tool-calling loop.
    max_iters = 10
    for i in range(max_iters):
        if verbose_flag:
            print(f"\n--- Iteration: {i} ---")

        payload = payload_base.copy()
        payload["contents"] = messages

        # Executing the HTTP POST request. This enables full control over the payload
        # and bypasses the stringent validators imposed by the google-genai package.
        response = requests.post(url, json=payload)
        data = response.json()

        if response.status_code != 200:
            print("\nAPI ERROR:")
            print(json.dumps(data, indent=2))
            return

        candidate = data.get("candidates", [{}])[0]
        content = candidate.get("content", {})
        parts = content.get("parts", [])

        if not parts:
            print("No response from the model.")
            return

        # Persisting the raw model response.
        # Guarantees the retention of hidden internal protocol metadata (e.g., call IDs).
        messages.append({"role": "model", "parts": parts})
        function_calls = [p for p in parts if "functionCall" in p]

        if function_calls:
            tool_responses_parts = []

            for f_part in function_calls:
                f_call = f_part["functionCall"]
                f_name = f_call.get("name")
                f_args = f_call.get("args", {})

                mock_call = MockFunctionCall(name=f_name, args=f_args)

                # Executing the associated tool logic.
                result_data = call_function(mock_call, verbose_flag)

                # Unpacking potential SDK artifacts. Ensures no custom objects (e.g., types.Content)
                # are passed to the requests library, which would raise a TypeError during JSON dumping.
                if hasattr(result_data, "model_dump"):
                    result_data = result_data.model_dump(exclude_none=True)

                if isinstance(result_data, dict) and "parts" in result_data:
                    f_resp_part = result_data["parts"][0]
                elif isinstance(result_data, dict) and "functionResponse" in result_data:
                    f_resp_part = result_data
                else:
                    f_resp_part = {
                        "functionResponse": {
                            "name": f_name,
                            "response": {"result": result_data}
                        }
                    }

                # Critical security assertion for models >= 3.0:
                # Replicating the authentication signature (thought_signature/id) from the request
                # to the response. This prevents a 400 INVALID_ARGUMENT status (logical chain breakage on the backend).
                if "id" in f_call and "functionResponse" in f_resp_part:
                    f_resp_part["functionResponse"]["id"] = f_call["id"]

                tool_responses_parts.append(f_resp_part)

            messages.append({"role": "user", "parts": tool_responses_parts})

        else:
            # Processing and merging all text fragments of the model's final output.
            texts = [p.get("text", "") for p in parts if "text" in p]
            print("\n" + "".join(texts))
            return


if __name__ == "__main__":
    main()