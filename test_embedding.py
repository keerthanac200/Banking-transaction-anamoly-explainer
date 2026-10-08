from sentence_transformers import SentenceTransformer

print("Loading GTE-large...")

model = SentenceTransformer("thenlper/gte-large")

print("GTE-large loaded successfully!")

text = "AI hackathon scholarship eligibility"
embedding = model.encode(text)

print("Embedding created!")
print("Embedding dimensions:", len(embedding))