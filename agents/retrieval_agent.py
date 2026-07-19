import numpy as np

class RetrievalAgent:
   def search(
       self,
       query,
       vectorizer,
       index,
       chunks,
       top_k=3
   ):
       query_vector = (
           vectorizer
           .transform([query])
           .toarray()
       )
       distances, indices = index.search(
           np.array(query_vector, dtype=np.float32),
           top_k
       )
       results = []
       for idx in indices[0]:
           if 0 <= idx < len(chunks):
               results.append(chunks[idx])
       return results