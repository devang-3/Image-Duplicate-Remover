import os
from PIL import Image
import imagehash

def get_rotation_flip_hashes(img):
    """Generate perceptual hashes for rotations (0°–350° with 10° steps) 
       and both horizontal & vertical flips"""
    hashes = []

    # ✅ Normal rotations
    for angle in range(0, 360, 10):  
        rotated = img.rotate(angle, expand=True)
        hashes.append(imagehash.phash(rotated))

        # ✅ Horizontal flip of rotated image
        flipped_h = rotated.transpose(Image.FLIP_LEFT_RIGHT)
        hashes.append(imagehash.phash(flipped_h))

        # ✅ Vertical flip of rotated image
        flipped_v = rotated.transpose(Image.FLIP_TOP_BOTTOM)
        hashes.append(imagehash.phash(flipped_v))

    return hashes

def remove_duplicates(folder, threshold=5):
    hashes = {}
    duplicates = []

    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)

        if os.path.isdir(filepath):
            continue  

        try:
            img = Image.open(filepath).convert("RGB")

            # Get rotation + flip invariant hash set
            hash_list = get_rotation_flip_hashes(img)

            duplicate_found = False
            for existing_h, kept_file in hashes.items():
                if any(abs(h - existing_h) <= threshold for h in hash_list):
                    duplicates.append(filepath)
                    duplicate_found = True
                    print(f"🔁 Duplicate found (rot/flip): {filename} ~ {os.path.basename(kept_file)}")

                    # ❌ Delete duplicate
                    os.remove(filepath)
                    break

            if not duplicate_found:
                # store one representative hash
                hashes[hash_list[0]] = filepath

        except Exception as e:
            print(f"Error processing {filename}: {e}")

    print(f"\n✅ Total duplicates removed: {len(duplicates)}")
    return duplicates

# Usage
folder = r"C:\Users\91947\Desktop\Data cleaning\lumpy"
duplicates = remove_duplicates(folder, threshold=5)
