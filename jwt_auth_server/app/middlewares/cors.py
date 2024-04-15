from fastapi.middleware.cors import CORSMiddleware


def setup_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://example.com"],  # Specify the origins
        allow_credentials=True,
        allow_methods=["GET", "POST"],  # Specify the methods
        allow_headers=["Authorization"],  # Specify the headers
        expose_headers=["Content-Length", "X-Content-Length"],  # Specify exposed headers
    )
