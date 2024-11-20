# -*- coding: utf-8 -*-
"""Copy of fullRAGDemo

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1XsOdgUgZ1czhhVxzH9Ce7TKykMIZplVL
"""

from openai import OpenAI
import numpy as np

client = OpenAI(api_key="sk-proj-3q2xNQD1H75Z*************************************t8aHZQajDOUT3OMa3JUBKWrNzYYzmeW3-81CaKuMVtdJzazvFPRdxjAA")

with open('messi.txt', "r") as f:
    text = f.read()
    print(text)

CHUNNK_SIZE = 100
chunks = []
current_place = 0
while current_place < len(text):
    current_chunk = text[current_place : current_place + CHUNNK_SIZE]
    chunks.append(current_chunk)
    current_place += CHUNNK_SIZE
print(chunks)

embedded_chunks = [] # -> [ () , () , , ]
for chunk in chunks:
    response = client.embeddings.create(
        input=chunk,
        model="text-embedding-3-small"
    )
    embedded_chunks.append( (chunk, response.data[0].embedding) )
print(embedded_chunks)

def cosine_simularity(A, B):
    return np.dot(A,B) / ( np.linalg.norm(A) * np.linalg.norm(B) )
    # ABCos / Vector A / |A| * B/|B|

question = "who is messi"

question_embedding = client.embeddings.create(
        input=question,
        model="text-embedding-3-small"
    ).data[0].embedding
print(question_embedding)

best_cosine_similarity = 0
index = 0
for i in range(len(embedded_chunks)):
    similarity = cosine_simularity(question_embedding, embedded_chunks[i][1])
    if similarity > best_cosine_similarity:
        best_cosine_similarity = similarity
        index = i

print(f"Relevant information: {embedded_chunks[index][0]}")

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user", "content": f"User question: {question}. Potentially useful information: {embedded_chunks[index][0]}"
        }
    ]
)

print(completion.choices[0].message.content)