import hashlib


def calculate_hash(filepath, algorithm="sha256"):
    hash_obj = hashlib.new(algorithm)

    with open(filepath, "rb") as f:
        while chunk := f.read(4096):
            hash_obj.update(chunk)

    return hash_obj.hexdigest()
