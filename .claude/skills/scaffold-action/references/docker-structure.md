# Docker/Python Action — Structural Template

Distilled from: `version-bump`

---

## Files

A Docker action directory contains:

```
{action-name}/
├── action.yml
├── Dockerfile
├── main.py
├── README.md
└── SPEC.md          (internal, removed automatically by the agent at pipeline completion)
```

---

## action.yml Structure

```yaml
name: "{Action Name}"
description: "{One-line description}"
author: "Bitwarden"

inputs:
  required_input:
    description: "What this input controls"
    required: true
  optional_input:
    description: "What this optional input controls"
    required: false
    default: "default_value"

outputs:
  output_name:
    description: "What this output contains"

runs:
  using: "docker"
  image: "Dockerfile"
```

### Key differences from composite

- `runs.using` is `"docker"` (not `"composite"`)
- `runs.image` points to `"Dockerfile"` (relative to action directory)
- Outputs do not have a `value` field — they are set by writing to `GITHUB_OUTPUT` in Python
- Inputs are passed as environment variables with `INPUT_` prefix (handled by GitHub Actions runtime)

---

## Dockerfile Structure

```dockerfile
FROM python:3-slim AS builder

WORKDIR /app

# Install dependencies (only if needed)
# RUN pip3 install --no-cache-dir package-name --target=.

ADD ./main.py .

FROM gcr.io/distroless/python3-debian12

WORKDIR /app
COPY --from=builder /app /app
ENV PYTHONPATH=/app

ENTRYPOINT ["/usr/bin/python3", "-u", "/app/main.py"]
```

### Multi-stage build pattern

- **Builder stage** (`python:3-slim`): Install pip packages with `--target=.` so they land in `/app`
- **Final stage** (`gcr.io/distroless/python3-debian12`): Minimal image, no shell, no package manager
- `ENV PYTHONPATH=/app` ensures pip-installed packages are importable
- `-u` flag ensures unbuffered Python output for real-time log streaming

### When dependencies are needed

Add the `RUN pip3 install` line for any packages beyond the Python standard library:

```dockerfile
RUN pip3 install --no-cache-dir pyyaml tomlkit --target=.
```

### When no dependencies are needed

Remove the `RUN pip3 install` line entirely. The builder stage still handles `ADD ./main.py`.

---

## main.py Skeleton

```python
import os
import sys


def main():
    # TODO: Read inputs from environment variables
    # input_name = os.getenv("INPUT_INPUT_NAME", "")

    # TODO: Validate inputs

    # TODO: Core logic

    # TODO: Set outputs
    # if "GITHUB_OUTPUT" in os.environ:
    #     with open(os.environ["GITHUB_OUTPUT"], "a") as f:
    #         print(f"output_name={value}", file=f)


if __name__ == "__main__":
    main()
```
