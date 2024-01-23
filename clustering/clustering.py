from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import DBSCAN

def main(eps, vectors, list):
    # dbscan 클러스터링
    cosine_sim_matrix = cosine_similarity(vectors, vectors)
    model = DBSCAN(eps=eps, min_samples=2, metric='cosine')
    clusters = model.fit(cosine_sim_matrix)

    # 군집 결과 출력
    labels = clusters.labels_
    clusters = {}
    for i, label in enumerate(labels):
        if label not in clusters:
            clusters[label] = {
                'id': list[i][0],
                'title': list[i][1],
                'list': ''
            }
        clusters[label]['list'] += str(list[i][0])+','

    return clusters

    # 결과 출력
    # for cluster_label, cluster_sentences in clusters.items():
    #     print(f"Cluster {cluster_label}:\n")
    #     for sentence in cluster_sentences:
    #         print(f"  - {sentence}")
    #     print("\n")