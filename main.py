import os
from app import create_app

# @app.route("/")
# def hello_world():
#   """Example Hello World route."""
#   name = os.environ.get("NAME", "World")
#   return f"Hello {name}!"

app = create_app()

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
