import httpx

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

if __name__ == "__main__":
  import asyncio
  asyncio.run(main())