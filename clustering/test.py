from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from sklearn.decomposition import PCA

def test(sentences):
    # TF-IDF 벡터화
    vectorizer = TfidfVectorizer(min_df=2)
    tfidf_matrix = vectorizer.fit_transform(sentences)

    # DBSCAN을 사용하여 군집화
    model = DBSCAN(eps=0.4, min_samples=2, metric='cosine')
    clusters = model.fit_predict(tfidf_matrix)

    # 군집 결과 출력
    for i, sentence in enumerate(sentences):
        print(f"문장: '{sentence}', 군집: {clusters[i]}")

    # 시각화를 위한 차원 축소 (2차원으로)
    pca = PCA(n_components=2)
    tfidf_2d = pca.fit_transform(tfidf_matrix.toarray())

    # 군집화 결과를 시각화
    font_path = 'C:/Windows/Fonts/gulim.ttc'
    font_name = fm.FontProperties(fname=font_path).get_name()
    plt.rc('font', family=font_name)
    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(tfidf_2d[:, 0], tfidf_2d[:, 1], c=clusters, cmap='plasma', marker='o', s=30, alpha=0.1)

    # 각 데이터 포인트에 라벨 추가 (동적으로)
    annot = plt.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                         bbox=dict(boxstyle="round", fc="w"),
                         arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    def update_annot(ind):
        pos = scatter.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        text = f'{sentences[ind["ind"][0]]}\nCluster: {clusters[ind["ind"][0]]}'
        annot.set_text(text)
        annot.get_bbox_patch().set_facecolor(plt.cm.plasma(clusters[ind["ind"][0]]))
        annot.get_bbox_patch().set_alpha(0.4)

    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == plt.gca():
            cont, ind = scatter.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                plt.draw()
            else:
                if vis:
                    annot.set_visible(False)
                    plt.draw()

    plt.gcf().canvas.mpl_connect("motion_notify_event", hover)

    plt.title('DBSCAN Clustering of 비슷한 제목')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.colorbar(scatter, label='Clusters')
    plt.show()
