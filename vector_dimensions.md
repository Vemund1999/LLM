# What if you change embeddings/LLM model, and the vector database says the embedding function and vector dimensions do not match

## Delete the previous index
- Go to http://localhost:7474/browser/
- SHOW INDEXES
- DROP INDEX vector;


## Recreate the index witht he correct dimensions
CREATE VECTOR INDEX vector IF NOT EXISTS
FOR (m:Chunk)
ON m.embedding
OPTIONS {indexConfig: {
 `vector.dimensions`: <dimension value, ex:4096>,
 `vector.similarity_function`: 'cosine'
}}



