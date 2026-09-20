"""from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
    "annual leave",
    "vacation days",
    "leftover holidays",
    "salary increment"
]

embeddings = model.encode(sentences)

print("Number of sentences:", len(sentences))
print("Number of embeddings:", len(embeddings))
print("Embedding dimensions:", len(embeddings[0]))

print()
print("First embedding:")
print(embeddings[0])"""


from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
    "annual leave",
    "vacation days",
    "leftover holidays",
    "salary increment"
]

embeddings = model.encode(sentences)

similarities = cosine_similarity(
    [embeddings[0]],
    embeddings[1:]
)

print("annual leave vs vacation days:", similarities[0][0])
print("annual leave vs leftover holidays:", similarities[0][1])
print("annual leave vs salary increment:", similarities[0][2])
