import json
import os

from src.api.main import app

"""
Utility script to regenerate the static OpenAPI specification.

Usage:
- Run `python -m src.api.generate_openapi` from the carpool_backend root.
- This will write interfaces/openapi.json so the frontend can consume a stable spec file.
"""

# Get the OpenAPI schema
openapi_schema = app.openapi()

# Write to file
output_dir = "interfaces"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "openapi.json")

with open(output_path, "w") as f:
    json.dump(openapi_schema, f, indent=2)
