from auth_service.create_app import create_app
from uvicorn import run as server_run

if __name__ == "__main__":
    app = create_app()

    server_run(app, host="0.0.0.0", port=8000)
