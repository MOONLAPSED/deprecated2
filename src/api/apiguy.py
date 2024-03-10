import httpx
from pydantic import create_model, ValidationError, BaseModel
import toml
import asyncio
import logging

ml = logging.getLogger(__name__)

def load_definitions(path="src/api/static/api_definitions.toml"):
    """
    Loads the API definitions from a TOML file.
    """
    with open(path, "r") as f:
        definitions = toml.load(f)
        return definitions
    
def get_definition(name, path="src/api/static/api_definitions.toml"):
    """
    Loads the API definition from a TOML file.
    """
    definitions = load_definitions(path)
    return definitions[name]


# Define the API endpoints
API_ENDPOINTS = {
  "generate": generate_handler,
  "chat": chat_handler
}

async def api_handler(request):
  if request.method == "POST":
    endpoint = API_ENDPOINTS.get(request.url.parts[-1])
    if endpoint:
      return await endpoint(request)

  return httpx.Response(status_code=405)

async def generate_handler(request):
  # Parse request body
  data = request.json()

  # Call generation function
  response = generate_response(data["prompt"], data["model"], data["options"])
  
  # Return response
  return httpx.Response(
    status_code=200,
    json=response
  )

async def chat_handler(request):
  # Parse request body
  data = request.json()

  # Call chat function 
  response = get_chat_response(data["prompt"], data["model"], data["context"])

  # Return response
  return httpx.Response(
    status_code=200, 
    json=response
  )

async def main():
  async with httpx.AsyncServer(app=api_handler, port=8000) as server:
    await server.serve()

def main():
  ml.info(f'API module initialized\n Logging initialized src: %s', __file__)
  defs=load_definitions()
  for key in defs:
      ml.info(f'{key}')
      for k,v in defs[key].items():
          ml.info(f'{k}={v}')
  if k=='path':
      ml.info(f'path={v}')
  ml.info(f'path={v}')



if __name__ == "__main__":

  asyncio.run(main())
  main()
