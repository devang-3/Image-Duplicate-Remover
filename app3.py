import cv2
import os
import shutil

def are_duplicates(img1_path, img2_path, ratio_threshold=0.5):
    """Check if two images are duplicates using ORB feature matching (rotation/scale invariant)."""
    img1 = cv2.imread(img1_path, 0)
    img2 = cv2.imread(img2_path, 0)

    if img1 is None or img2 is None:
        return False

    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    if des1 is None or des2 is None or len(kp1) == 0 or len(kp2) == 0:
        return False

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)

    # Normalize similarity by number of keypoints
    similarity = len(matches) / max(len(kp1), len(kp2))

    return similarity > ratio_threshold


def remove_duplicates(folder, keep_folder="cleaned_dataset_3", ratio_threshold=0.5):
    if not os.path.exists(keep_folder):
        os.makedirs(keep_folder)

    kept_images = []
    duplicates = []

    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)

        if os.path.isdir(filepath):
            continue  

        is_duplicate = False
        for kept_file in kept_images:
            if are_duplicates(filepath, kept_file, ratio_threshold):
                # ✅ Compare resolution → keep highest quality
                h1, w1 = cv2.imread(filepath).shape[:2]
                h2, w2 = cv2.imread(kept_file).shape[:2]

                if h1 * w1 > h2 * w2:
                    # Replace old with higher res
                    shutil.copy(filepath, os.path.join(keep_folder, os.path.basename(filepath)))
                    os.remove(os.path.join(keep_folder, os.path.basename(kept_file)))
                    kept_images.remove(kept_file)
                    kept_images.append(filepath)
                    print(f"🔁 Replaced {os.path.basename(kept_file)} with higher resolution {filename}")
                else:
                    duplicates.append(filepath)
                    print(f"🔁 Duplicate found: {filename} ~ {os.path.basename(kept_file)}")
                is_duplicate = True
                break

        if not is_duplicate:
            kept_images.append(filepath)
            shutil.copy(filepath, os.path.join(keep_folder, filename))

    print(f"\n✅ Total duplicates found: {len(duplicates)}")
    print(f"📂 Cleaned dataset saved at: {keep_folder}")
    return duplicates


# ----------------------------
# 🚀 Usage
# ----------------------------
folder = r"C:\Users\91947\Desktop\Data cleaning\healthy"  # your dataset folder
duplicates = remove_duplicates(folder, ratio_threshold=0.5)
