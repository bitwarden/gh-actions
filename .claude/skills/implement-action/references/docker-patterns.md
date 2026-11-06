# Docker/Python Action — Implementation Patterns

Distilled from: `version-bump`

---

## Entry Point Structure

Every Python action follows this shape in `main.py`:

```python
import os
import sys


def main():
    # === Read Inputs ===
    input_name = os.getenv("INPUT_INPUT_NAME", "")
    file_path = os.getenv("INPUT_FILE_PATH", "")

    # === Validate Inputs ===
    if not input_name:
        print("::error::Input 'input_name' is required but was empty.")
        sys.exit(1)

    # === Core Logic ===
    # ... business logic ...

    # === Set Outputs ===
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            print(f"output_name={value}", file=f)


if __name__ == "__main__":
    main()
```

Key rules:
- Single `main()` function as entry point
- Guard with `if __name__ == "__main__"`
- Read inputs from `INPUT_`-prefixed environment variables (GitHub uppercases input names)
- Write outputs to the `GITHUB_OUTPUT` file
- Exit with `sys.exit(1)` on failure

---

## Input Reading

GitHub Actions maps inputs to environment variables with the `INPUT_` prefix and uppercased names.

```python
# Input "version" becomes INPUT_VERSION
version = os.getenv("INPUT_VERSION", "")

# Input "file_path" becomes INPUT_FILE_PATH
file_path = os.getenv("INPUT_FILE_PATH", "")
```

### Multi-word input names

Underscores in input names are preserved. Hyphens are converted to underscores.

```python
# Input "max_threads" becomes INPUT_MAX_THREADS
max_threads = os.getenv("INPUT_MAX_THREADS", "100")
```

---

## Input Validation

Validate immediately after reading, before any business logic.

### Required non-empty

```python
if not version:
    print("::error::Input 'version' is required but was empty.")
    sys.exit(1)
```

### File existence

```python
if not os.path.isfile(file_path):
    print(f"::error::File not found: {file_path}")
    sys.exit(1)
```

### Format validation

```python
import re

if not re.match(r'^\d+\.\d+\.\d+$', version):
    print(f"::error::Invalid version format: expected 'X.Y.Z', got '{version}'")
    sys.exit(1)
```

### Enum validation

```python
VALID_TYPES = {".xml", ".json", ".plist", ".toml"}
file_type = os.path.splitext(file_path)[1]
if file_type not in VALID_TYPES:
    print(f"::error::Unsupported file type: {file_type}")
    sys.exit(1)
```

---

## Output Setting

Write outputs by appending to the `GITHUB_OUTPUT` file:

```python
if "GITHUB_OUTPUT" in os.environ:
    with open(os.environ["GITHUB_OUTPUT"], "a") as f:
        print(f"status=Updated {file_path}", file=f)
```

Always check that `GITHUB_OUTPUT` exists — it won't be set during local testing.

### Multiple outputs

```python
if "GITHUB_OUTPUT" in os.environ:
    with open(os.environ["GITHUB_OUTPUT"], "a") as f:
        print(f"status={status}", file=f)
        print(f"file_count={count}", file=f)
```

---

## Error Handling

### GitHub Actions annotations

```python
print("::error::Description of what went wrong")
print("::warning::Non-fatal issue")
print("::notice::Informational message")
```

### File operation errors

```python
try:
    with open(file_path, "r") as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"::error::File not found: {file_path}")
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"::error::Invalid JSON in {file_path}: {e}")
    sys.exit(1)
```

### Top-level exception guard

```python
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"::error::Unexpected error: {e}")
        sys.exit(1)
```

---

## File Format Dispatch

When an action handles multiple file types, dispatch based on extension:

```python
def get_file_type(file_path):
    return os.path.splitext(file_path)[1]

file_type = get_file_type(file_path)

if file_type in {".xml", ".props", ".csproj"}:
    update_xml(version, file_path)
elif file_type == ".json":
    update_json(version, file_path)
elif file_type == ".plist":
    update_plist(version, file_path)
else:
    print(f"::error::Unsupported file type: {file_type}")
    sys.exit(1)
```

---

## Subprocess Usage

When shell commands are needed, always use argument lists — never `shell=True` with untrusted input:

```python
import subprocess

# GOOD — safe argument list
result = subprocess.run(
    ["git", "tag", "-l", version],
    capture_output=True,
    text=True,
    check=True,
)

# BAD — shell injection risk
# subprocess.run(f"git tag -l {version}", shell=True)
```

### Handling subprocess errors

```python
try:
    result = subprocess.run(
        ["command", "arg1", "arg2"],
        capture_output=True,
        text=True,
        check=True,
    )
except subprocess.CalledProcessError as e:
    print(f"::error::Command failed (exit {e.returncode}): {e.stderr}")
    sys.exit(1)
```

---

## Dockerfile Structure

Use multi-stage builds with a distroless final image:

```dockerfile
FROM python:3-slim AS builder

WORKDIR /app

# Install dependencies to the app directory
RUN pip3 install --no-cache-dir package-name --target=.

ADD ./main.py .

FROM gcr.io/distroless/python3-debian12

WORKDIR /app
COPY --from=builder /app /app
ENV PYTHONPATH=/app

ENTRYPOINT ["/usr/bin/python3", "-u", "/app/main.py"]
```

Key rules:
- Builder stage installs dependencies with `--target=.` so they're co-located
- Final stage uses `gcr.io/distroless/python3-debian12` for minimal attack surface
- `-u` flag on python ensures unbuffered output (logs appear in real time)
- Only add `RUN pip3 install` if the action needs external packages
