import os
from uvicorn import run

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    run("server:app", host="0.0.0.0", port=port)
