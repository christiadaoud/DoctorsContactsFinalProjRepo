import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Doctor

# Cache
tfidf_matrix = None
similarity_matrix = None
doctor_df = None

def initialize_doctor_similarity():
    global tfidf_matrix, similarity_matrix, doctor_df
    all_doctors = Doctor.objects.all()
    if not all_doctors.exists():
        return

    doctor_df = pd.DataFrame(list(all_doctors.values(
        'id', 'name', 'specialty', 'city', 'hospital', 'fee', 'rating'
    )))
    doctor_df['text_features'] = doctor_df['specialty'] + ' ' + doctor_df['city']

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(doctor_df['text_features'])

    similarity_matrix = cosine_similarity(tfidf_matrix)

def get_similar_doctors_by_id(doctor_id, top_n=3):
    global tfidf_matrix, similarity_matrix, doctor_df
    if tfidf_matrix is None or similarity_matrix is None:
        initialize_doctor_similarity()
    if doctor_df.empty or doctor_id not in doctor_df['id'].values:
        return []

    idx = doctor_df.index[doctor_df['id'] == doctor_id][0]
    sim_scores = list(enumerate(similarity_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    similar = []
    for i, score in sim_scores[1:top_n+1]:  # skip self
        similar.append(doctor_df.loc[i].to_dict())
    return similar

