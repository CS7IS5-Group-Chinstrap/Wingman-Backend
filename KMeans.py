from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pandas as pd

def  getSimilarUsers(df,id):
  
    data = pd.DataFrame({
        'age': df['age'],
        'diet': df['diet'],
        'drinks': df['drinks'],
        'orientation':df['orientation']
    })

    # Converting categorical features to numerical using label encoding
    label_encoder = LabelEncoder()
    data['diet'] = label_encoder.fit_transform(data['diet'])
    data['drinks'] = label_encoder.fit_transform(data['drinks'])
    data['orientation'] = label_encoder.fit_transform(data['orientation'])

    # Scaling the features (standardization)
    scaler = StandardScaler()
    X = scaler.fit_transform(data)

    #  using 3 clusters
    kmeans = KMeans(n_clusters=3)
    kmeans.fit(X)

    # import matplotlib.pyplot as plt

    # plt.scatter(X[:, 0], X[:, 1], c=kmeans.labels_)
    # plt.xlabel('Age')
    # plt.ylabel('Diet')
    # plt.show()

    # Find similar users 
    user_index = df.id[df.id == id].index.tolist()[0]
    print(user_index)
    cluster_label = kmeans.predict([X[user_index]])[0]
    similar_users = [i for i, label in enumerate(kmeans.labels_) if label == cluster_label and i != user_index]
    return df.iloc[similar_users]

