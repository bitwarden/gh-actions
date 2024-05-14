import sys
import os
import hashlib

def get_file_sha256_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

if __name__ == "__main__":
    packages_dir = os.getenv("INPUT_PACKAGES_DIR")
    file_path = os.getenv("INPUT_FILE_PATH")

    if os.path.isdir(file_path):
        file_path = os.path.join(file_path, "sha256-checksums.txt")

    print(f"Packages directory: {packages_dir}")
    print(f"File which will contain SHA256 checksums will be: {file_path}")

    hashes = ""

    for path in os.listdir(packages_dir):
        package_path = os.path.join(packages_dir, path)
        if not os.path.isfile(package_path):
            continue

        file_hash = get_file_sha256_hash(package_path)

        hashes += f"{file_hash}  {path}{os.linesep}"

    hashes = hashes[:-1]

    with open(file_path, "w") as f:
        f.write(hashes)

    print(hashes)

    print(f"Saved checksums in file: {file_path} >> $GITHUB_OUTPUT")
