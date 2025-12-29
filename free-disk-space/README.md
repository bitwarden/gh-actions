# Free Disk Space

A reusable GitHub Action that removes pre-installed tools from Linux runners to free disk space for workflows that do not need to use them.

## Features

- **Configurable cleanup**: Choose which tools to remove via inputs
- **Linux-only**: Automatically skips on macOS and Windows runners
- **Verbose output**: Shows disk space before and after cleanup

## Usage

### Basic Example (Remove Everything)

```yaml
- name: Free disk space
  uses: bitwarden/gh-actions/free-disk-space@main
```

This removes defined pre-installed tools with default settings.

### Selective Removal Example

```yaml
- name: Free disk space
  uses: bitwarden/gh-actions/free-disk-space@main
  with:
    remove-dotnet: false    # Keep .NET tools (needed for C# builds)
    # you do not have to set true for the ones to remove as they will default to true
```

## When to Use This Action

Use this action when your workflow encounters disk space issues on GitHub-hosted runners, particularly for:

- **Large projects**: Compilation artifacts can be 10-20GB+
- **Code coverage tools**: Tools like `cargo-llvm-cov` generate large intermediate files
- **Multi-language builds**: Projects with multiple toolchains
- **Docker builds**: Large image layers and build caches

### Common Error Signs

You may need this action if you see errors like:
```
No space left on device
error: linking with `cc` failed: exit status: 1
fatal error: ld terminated with signal 7 [Bus error]
```

## Platform Compatibility

- ✅ **Linux**: Fully supported (ubuntu-22.04, ubuntu-24.04, etc.)
- ⚠️ **macOS**: Action runs but skips cleanup (not needed on macOS runners)
- ⚠️ **Windows**: Action runs but skips cleanup (paths don't exist on Windows)

## Notes

- The action automatically detects the OS and only runs cleanup on Linux runners
- Cleanup is performed with `sudo rm -rf`, so there's no interactive prompts
- Disk space measurements are shown in the workflow logs
- This action does not affect the runner's cache or any checked-out code
