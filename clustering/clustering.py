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
                'id': list[i]['id'],
                'title': list[i]['title'],
                'count': 0,
                'recommend': 0,
                'date': '',
                'list': [],
                'og_image': list[i]['og_image'],
            }
        clusters[label]['writer_object_id'] = list[i]['writer_object_id']
        clusters[label]['writer_id'] = list[i]['writer_id']
        clusters[label]['writer_nickname'] = list[i]['writer_nickname']
        clusters[label]['count'] += 1
        clusters[label]['recommend'] += list[i]['recommend']
        clusters[label]['date'] = str(list[i]['date'])
        clusters[label]['list'].append(list[i]['id'])
    # 2024 06 04 몽고db로 바꿔서 주석함 ㅎㅎ;
    # for i, label in enumerate(labels):
    #     print(list[i])
    #     if label not in clusters:
    #         clusters[label] = {
    #             'id': list[i][0],
    #             'title': list[i][1],
    #             'count': 0,
    #             'recommend': 0,
    #             'date': '',
    #             'list': []
    #         }
    #     clusters[label]['count'] += 1
    #     clusters[label]['recommend'] += list[i][3]
    #     clusters[label]['date'] = str(list[i][2])
    #     clusters[label]['list'].append(list[i][0])

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