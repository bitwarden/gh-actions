#!/bin/bash

# test-local.sh - Build and test the version-bump Docker action locally
# This script builds the Docker image and runs it against all test fixtures

set -e

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Default version to use for testing
VERSION="${1:-2123.4.5}"

echo -e "${YELLOW}=== Version Bump Docker Action Test ===${NC}"
echo "Testing with version: $VERSION"
echo ""

# Build the Docker image
DOCKER_TAG="version-bump:test"
echo -e "${YELLOW}Building Docker image...${NC}"
docker build -t "$DOCKER_TAG" .
echo -e "${GREEN}✓ Docker image built successfully${NC}"
echo ""

# Create a temporary directory for test files
TEST_DIR="$SCRIPT_DIR/tmp-$(date +%s)"
mkdir -p "$TEST_DIR"
echo "Using temporary directory: $TEST_DIR"

# Copy test fixtures to temp directory
ORIGINAL_TEST_DIR="$SCRIPT_DIR/tests/fixtures"
cp -r "$ORIGINAL_TEST_DIR/"* "$TEST_DIR/"

# Function to run a test
run_test() {
    local file_name="$1"
    local file_path="$TEST_DIR/$file_name"

    echo -e "${YELLOW}Testing: $file_name${NC}"

    # Create a temporary file for GitHub output
    GITHUB_OUTPUT_NAME=".github_output"
    GITHUB_OUTPUT="$TEST_DIR/$GITHUB_OUTPUT_NAME"
    CONTAINER_WORKSPACE="/workspace"

    # Run the Docker container
    docker run --rm \
        -v "$TEST_DIR:$CONTAINER_WORKSPACE" \
        -e INPUT_VERSION="$VERSION" \
        -e INPUT_FILE_PATH="$CONTAINER_WORKSPACE/$file_name" \
        -e GITHUB_OUTPUT="$CONTAINER_WORKSPACE/$GITHUB_OUTPUT_NAME" \
        "$DOCKER_TAG"

    # Check if the file was modified
    if grep -q "$VERSION" "$file_path"; then
        echo -e "${GREEN}✓ $file_name updated successfully${NC}"

        # Show the changes
        echo "  Changes in $file_name:"
        grep -n "$VERSION" "$file_path" | head -3 | sed 's/^/    /'
    else
        echo -e "${RED}✗ $file_name was not updated${NC}"
        exit 1
    fi

    # Clean up
    echo "  GITHUB_OUTPUT:"
    echo "    $(cat "$GITHUB_OUTPUT")"
    rm -f "$GITHUB_OUTPUT"
    echo ""
}

# Run tests for each fixture file
echo -e "${YELLOW}=== Running Tests ===${NC}"
echo ""

run_test "package-lock.json"
run_test "Info.plist"
run_test "AndroidManifest.xml"
run_test "dir.build.props"
run_test "test.csproj"
run_test "Cargo.toml"

# Show git diff style output
echo -e "${YELLOW}=== File Changes Summary ===${NC}"
for file in "$TEST_DIR"/*; do
    if [[ -f "$file" && $(basename "$file") != ".gitignore" ]]; then
        echo -e "${YELLOW}$(basename "$file"):${NC}"
        grep -n "$VERSION" "$file" | head -2 | sed 's/^/  /'
    fi
done

echo ""
echo -e "${GREEN}=== All Tests Passed! ===${NC}"
echo -e "${GREEN}The Docker image works correctly with version: $VERSION${NC}"
