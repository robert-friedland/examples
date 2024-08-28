import os
from openai import OpenAI

OPENAI_SECRET_KEY = os.environ.get('OPENAI_SECRET_KEY')
client = OpenAI(api_key=OPENAI_SECRET_KEY)

assistant = client.beta.assistants.create(
  name="My Assistant",
  model="gpt-4o",
  tools=[{"type": "file_search"}],
)

# Create a vector store caled "Financial Statements"
vector_store = client.beta.vector_stores.create(name="My Vector Store")
 
# Ready the files for upload to OpenAI
file_paths = [r"C:\Users\rober\Downloads\top_50_bundle_logs.json"]
file_streams = [open(path, "rb") for path in file_paths]
 
# Use the upload and poll SDK helper to upload the files, add them to the vector store,
# and poll the status of the file batch for completion.
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
  vector_store_id=vector_store.id, files=file_streams
)

vector_store_files = client.beta.vector_stores.files.list(vector_store_id=vector_store.id)
for file in vector_store_files:
    print(file.last_error.message)

# Prints "The file could not be parsed because it is too large."
