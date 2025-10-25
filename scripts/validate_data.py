#!/usr/bin/env python3
# validate_data.py - validate JSON against schema

import sys
import json
from jsonschema import validate, ValidationError, SchemaError

DATA_PATH = sys.argv[1] if len(sys.argv) > 1 else "/workspaces/my_portfolio/root/data.json"
SCHEMA_PATH = sys.argv[2] if len(sys.argv) > 2 else "/workspaces/my_portfolio/root/schemas/data_schema.json"

def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    try:
        data = load(DATA_PATH)
        schema = load(SCHEMA_PATH)
        validate(instance=data, schema=schema)
        print("OK: data.json validates against schema.")
    except FileNotFoundError as e:
        print("ERROR: file not found:", e)
        sys.exit(2)
    except SchemaError as e:
        print("ERROR: invalid schema:", e)
        sys.exit(3)
    except ValidationError as e:
        print("VALIDATION ERROR:", e.message)
        print("Path:", list(e.path))
        sys.exit(4)
    except Exception as e:
        print("ERROR:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()