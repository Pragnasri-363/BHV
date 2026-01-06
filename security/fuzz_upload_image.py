"""
Minimal image upload fuzzing harness for BHV to increase security.

This script is intended to increase the robustness of image handling by feeding the malformed or adversarial image inputs and identify any crashes or hangs etc..

The harness is intentionally kept minimal to align with BHV's goals.
- It is not a production fuzzing system
- It does not provide coverage guarantees
- It is designed to fail fast on crashes, hangs, or unexpected exceptions

A failure is defined as:
- An unhandled exception during image processing
- Excessive resource usage or hangs while parsing an image

This script is meant to be run manually by developers when modifying or
reviewing image upload logic.

"""

# Fuzzing flow:
#
# 1. Load a small set of valid seed images
# 2. Apply simple mutations to the image bytes
#    - truncation
#    - random byte flipping
#    - metadata corruption
# 3. Attempt to parse the mutated images
# 4. Observe and record crashes or unexpected behavior
#
# NOTE:
# This script intentionally avoids complex fuzzing infrastructure to align with BHV's goal to have a minimal application with security.
# The goal is early detection of failure modes, not exhaustive testing.

import os
from PIL import Image
import random

def load_and_verify(image_path):
    try:
        with Image.open(image_path) as im:
            im.verify()
        print(f"[+] Verified seed image: {image_path}")
        return image_path
    except (OSError, SyntaxError) as e:
        print(f"[!] Bad seed image {image_path}: {e}")
        return None

def truncate_image(ip_path,op_path):
    with open(ip_path, "rb") as f:
        data = f.read()


    if len(data)<2:
        return False
    
    cut=random.randint(1,len(data)-1)
    truncated=data[:-cut]

    with open(op_path, "wb") as f:
        f.write(truncated)

    return truncated

# Truncation helps us find the cases where program assumes data will alway be a certain length.It can also be used to shrink the input when massive inputs crashes the program.

if __name__ == "__main__":
    seed_dir = "security/seeds"
    output_dir = "security/tmp"

    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(seed_dir):
        seed_path = os.path.join(seed_dir, filename)

        # Step 1: validate seed
        if not load_and_verify(seed_path):
            continue

        # Step 2: truncate
        corrupted_path = os.path.join(output_dir, f"truncated_{filename}")
        truncate_image(seed_path, corrupted_path)

        # Step 3: test corrupted image
        load_and_verify(corrupted_path)

# Truncated images are expected to fail verification.
# This harness ensures such failures are detected safely without crashing the application.
