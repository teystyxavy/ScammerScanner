import sqlite3
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

SIMILARITY_THRESHOLD = 0.7

class ScamSecondCheckService:
    def __init__(self) -> None:
        conn = sqlite3.connect('ScamDetectorDB.db')
        cursor = conn.cursor()

        # Fetch data from db
        cursor.execute("SELECT analyzed_text, scam_status FROM Screenshots")
        data = cursor.fetchall()

        self.texts = [row[0] for row in data]
        self.scam_statuses = [row[1] for row in data]
        self.is_scam = False

        conn.close()
        pass

    def check_text(self,chk_text:str) -> bool:
        """
        Finds most similar text in database ( min similarity = SIMILARITY_THRESHOLD )
        Returns True if database text is identified as a scam
        """

        all_texts = self.texts + [chk_text]

        # Compute TF-IDF for all texts
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(all_texts)

        # Compute cosine similarity between new_text and all other texts
        new_text_vector = tfidf_matrix[-1]  # The last row is the new_text
        similarities = tfidf_matrix.dot(new_text_vector.T).toarray().flatten()[:-1]  # Exclude new_text itself

        most_similar_score = np.max(similarities)
        most_similar_index = np.argmax(similarities)

        #check if higher than threshold
        if most_similar_score > SIMILARITY_THRESHOLD:
            if self.scam_statuses[most_similar_index] == 'RED':
                self.is_scam = True
            
            return True
        
        # If not higher, return false as our database not high enough (YELLOW)
        return False