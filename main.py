from fastapi import FastAPI
from fastapi.responses import JSONResponse
import socketio

# Create FastAPI instance
app = FastAPI()

# Create a Socket.IO server with CORS enabled
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*"  # Allow all origins, or replace with a specific origin
)
socket_app = socketio.ASGIApp(sio, other_asgi_app=app)

# Define Socket.IO events
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    await sio.emit("message", {"message": "Welcome!"}, to=sid)

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.event
async def message(sid, data):
    print(f"Message from {sid}: {data}")
    await sio.emit("response", {"message": "Message received!"}, to=sid)

# FastAPI route
@app.get("/")
def root():
    """
    Root endpoint for basic testing.
    
    Returns:
        dict: Welcome message.
    """
    return {"message": "Welcome to the FastAPI File Upload Service!"}
