import os
import shutil
import numpy as np
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.preprocessing import image
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

# Load pre-trained ResNet50 (remove top classification layer)
model = ResNet50(weights="imagenet", include_top=False, pooling="avg")

def get_embedding(img_path):
    """Convert image into deep learning embedding."""
    try:
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        features = model.predict(x, verbose=0)
        return features.flatten()
    except Exception as e:
        print(f"⚠️ Error processing {img_path}: {e}")
        return None

def remove_duplicates(folder, keep_folder="cleaned_lumpy", similarity_threshold=0.9):
    if not os.path.exists(keep_folder):
        os.makedirs(keep_folder)

    embeddings = []
    kept_files = []
    duplicates = []

    for filename in tqdm(os.listdir(folder), desc="Processing images"):
        filepath = os.path.join(folder, filename)
        if os.path.isdir(filepath):
            continue

        emb = get_embedding(filepath)
        if emb is None:
            continue

        is_duplicate = False
        for i, existing_emb in enumerate(embeddings):
            sim = cosine_similarity([emb], [existing_emb])[0][0]
            if sim > similarity_threshold:  # higher = more similar
                duplicates.append(filepath)
                print(f"🔁 Duplicate found: {filename} ~ {os.path.basename(kept_files[i])}")
                is_duplicate = True
                break

        if not is_duplicate:
            embeddings.append(emb)
            kept_files.append(filepath)
            shutil.copy(filepath, os.path.join(keep_folder, filename))

    print(f"\n✅ Total duplicates found: {len(duplicates)}")
    print(f"📂 Cleaned dataset saved at: {keep_folder}")
    return duplicates


# ----------------------------
# 🚀 Usage
# ----------------------------
folder = r"C:\Users\91947\Desktop\Data cleaning\lumpy"  # your dataset path
duplicates = remove_duplicates(folder, similarity_threshold=0.8)
