📂 Files

app3.py → ORB feature-based duplicate removal

  Uses OpenCV’s ORB keypoints & descriptors
  Handles rotation & scale
  Keeps the highest resolution version when duplicates are found

app4.py → Deep Learning (ResNet50) based duplicate removal

  Extracts embeddings using a pre-trained ResNet50 model
  Compares images via cosine similarity
  Robust to rotation, cropping, compression, and color changes
  Best choice for large or diverse datasets

app5.py → Perceptual Hashing with rotation & flip checks
  
  Uses perceptual hashing (imagehash)
  Compares multiple rotations (0°–350°, step of 10°) + horizontal/vertical flips
  Deletes duplicates directly from the original folder

🚀 Usage

Install dependencies:

  pip install opencv-python pillow imagehash tensorflow scikit-learn tqdm
  Update the folder path inside the script to point to your dataset.

Run the script:

  python app3.py   # ORB approach
  python app4.py   # Deep learning approach
  python app5.py   # Perceptual hashing approach
  
Results:

  app3.py and app4.py → keep unique images in a cleaned folder.
  app5.py → deletes duplicates directly from the original folder.

⚙️ Parameters

  ORB (app3.py) → ratio_threshold (default = 0.5).
  ResNet50 (app4.py) → similarity_threshold (default = 0.9, lower to 0.8 for looser matching).
  Perceptual Hash (app5.py) → threshold (default = 5, higher values catch more near-duplicates).

📊 Comparison
  Approach	Speed ⏱️	Robustness 🛡️	Handles Rotations 🔄	Handles Flips ↔️	Best Use Case
  ORB (app3.py)	⚡ Fast	Medium	✅ Yes	❌ No	Small datasets with simple duplicates
  ResNet50 (app4.py)	🐢 Slower	⭐ High	✅ Yes	✅ Yes (semantic)	Large & diverse datasets, high accuracy
  pHash (app5.py)	⚡ Very Fast	Low–Medium	✅ Yes (0°–350°)	✅ Yes	Lightweight, rotation/flip duplicates

📌 Notes

  ORB is fast, good for smaller datasets.
  ResNet50 is robust, recommended for large datasets with complex variations.
  Perceptual hashing is lightweight, useful when rotation/flip duplicates are common.


ResNet50 is robust, recommended for large datasets with complex variations.

Perceptual hashing is lightweight, useful when rotation/flip duplicates are common.
