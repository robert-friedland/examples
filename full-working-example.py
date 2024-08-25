# ---------------------------------------------------------------------------------------------------
# Below is the full code I was able to run to reliably return the full answer to the user's question.
# ---------------------------------------------------------------------------------------------------

from openai import OpenAI

OPENAI_SECRET_KEY = "your secret key"

client = OpenAI(api_key=OPENAI_SECRET_KEY)

file_path = "dataset.csv"

file = client.files.create(
  file=open(file_path, "rb"),
  purpose='assistants'
)

assistant = client.beta.assistants.create(
  model="gpt-4o-mini",
  tools=[{"type": "code_interpreter"}],
  tool_resources={
    "code_interpreter": {
      "file_ids": [file.id]
    }
  },
  # Give the Assistant explicit instructions to avoid truncating the response.
  description="Answer the user's question thoroughly and completely.",
  instructions="Create and run Python code to answer the user's question. Set the pandas display.max_colwidth to None. Return the answer from code verbatim."
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content="What is Tina's favorite city?"
)

run = client.beta.threads.runs.create_and_poll(
  thread_id=thread.id,
  assistant_id=assistant.id
)

messages = client.beta.threads.messages.list(
  thread_id=thread.id,
  order="asc"
)

run_steps = client.beta.threads.runs.steps.list(
  thread_id=thread.id,
  run_id=run.id,
  order="asc"
)

# Print both the code that Code Interpreter is running and the messages returned by the Assistant.
for step in run_steps:
    if step.type == "message_creation":
        message = next((message for message in messages if message.id == step.step_details.message_creation.message_id))
        print(f"{message.role}: {message.content[0].text.value}")
    if step.type == "tool_calls":
        print(step.step_details.tool_calls[0].code_interpreter.input)
    print("")
