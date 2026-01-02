import hashlib
import os

HASH_FILE = "hash_store.txt"
FOLDER_TO_MONITOR = "test_files"

def calculate_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            sha256.update(chunk)
    return sha256.hexdigest()

def load_previous_hashes():
    hashes = {}
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            for line in f:
                filename, filehash = line.strip().split(",")
                hashes[filename] = filehash
    return hashes

def save_hashes(hashes):
    with open(HASH_FILE, "w") as f:
        for filename, filehash in hashes.items():
            f.write(f"{filename},{filehash}\n")

def check_integrity():
    previous_hashes = load_previous_hashes()
    current_hashes = {}

    print("🔍 Checking file integrity...\n")

    for filename in os.listdir(FOLDER_TO_MONITOR):
        file_path = os.path.join(FOLDER_TO_MONITOR, filename)

        if os.path.isfile(file_path):
            current_hash = calculate_hash(file_path)
            current_hashes[filename] = current_hash

            if filename not in previous_hashes:
                print(f"🆕 New file detected: {filename}")
            elif previous_hashes[filename] != current_hash:
                print(f"⚠ File modified: {filename}")
            else:
                print(f"✅ File unchanged: {filename}")

    save_hashes(current_hashes)
    print("\n✔ Integrity check complete.")

if __name__ == "__main__":
    check_integrity()
