from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import DBSCAN

def main(eps, vectors, list):
    # dbscan 클러스터링
    cosine_sim_matrix = cosine_similarity(vectors, vectors)
    model = DBSCAN(eps=eps, min_samples=3, metric='cosine')
    clusters = model.fit(cosine_sim_matrix)

    # 군집 결과 출력
    labels = clusters.labels_
    clusters = {}
    for i, label in enumerate(labels):
        if label not in clusters:
            clusters[label] = {
                'id': list[i][0],
                'title': list[i][1],
                'count': 0,
                'recommend': 0,
                'date': '',
                'list': []
            }
        clusters[label]['count'] += 1
        clusters[label]['recommend'] += list[i][3]
        clusters[label]['date'] = str(list[i][2])
        clusters[label]['list'].append(list[i][0])

    # # 결과 출력
    # for cluster_id, cluster_data in clusters.items():
    #     print(f"Cluster {cluster_id}:")
    #     print(f"Title: {cluster_data['title']}")
    #     print(f"Count: {cluster_data['count']}")
    #     print(f"Recommend: {cluster_data['recommend']}")
    #     print(f"Date: {cluster_data['date']}")
    #     print(f"List: {cluster_data['list']}")
    #     print()

    return clusters