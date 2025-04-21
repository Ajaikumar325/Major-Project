# hdbscan_clustering.py
import numpy as np
import hdbscan
import json
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import TSNE

# Load saved distance matrix and filenames
distance_matrix = np.load("tlsh_distance_matrix.npy")
with open("filenames.json", "r") as f:
    filenames = json.load(f)

# Run HDBSCAN clustering
clusterer = hdbscan.HDBSCAN(metric='precomputed', min_cluster_size=5)
labels = clusterer.fit_predict(distance_matrix)

# Save clustering results to JSON
cluster_result = [{"filename": name, "cluster": int(label)} for name, label in zip(filenames, labels)]
with open("cluster_output.json", "w") as f:
    json.dump(cluster_result, f, indent=2)

print(f"✅ Clustering results saved to cluster_output.json.")

# Optional: Visualize with t-SNE
tsne = TSNE(metric="precomputed", random_state=42)
embedding = tsne.fit_transform(distance_matrix)

plt.figure(figsize=(10, 8))
sns.scatterplot(x=embedding[:, 0], y=embedding[:, 1], hue=labels, palette="tab10")
plt.title("HDBSCAN Clustering of TLSH Distance Matrix (t-SNE)")
plt.show()
