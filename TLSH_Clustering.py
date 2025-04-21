# tlsh_clustering.py
import os
import tlsh
import numpy as np
import json

def compute_tlsh_hashes(folder_path):
    hashes = {}
    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)
        if os.path.isfile(full_path):
            with open(full_path, 'rb') as f:
                data = f.read()
                if len(data) > 50:
                    try:
                        hashes[filename] = tlsh.hash(data)
                    except:
                        print(f"[!] Skipping {filename}, unable to generate TLSH hash.")
    return hashes

def compute_tlsh_distance_matrix(hashes):
    filenames = list(hashes.keys())
    n = len(filenames)
    matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(i + 1, n):
            d = tlsh.diff(hashes[filenames[i]], hashes[filenames[j]])
            matrix[i][j] = matrix[j][i] = d
    return filenames, matrix

if __name__ == "__main__":
    folder = "path_to_malware_samples"  # 🔁 Replace with your actual path
    hashes = compute_tlsh_hashes(folder)
    filenames, matrix = compute_tlsh_distance_matrix(hashes)
    
    np.save("tlsh_distance_matrix.npy", matrix)
    with open("filenames.json", "w") as f:
        json.dump(filenames, f)

    print(f"✅ TLSH distance matrix and filenames saved. Total samples: {len(filenames)}")
