import pandas as pd
import tiktoken
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_KEY")
)

# embedding model parameters
embedding_model = "text-embedding-ada-002"
embedding_encoding = "cl100k_base"  # this the encoding for text-embedding-ada-002
max_tokens = 8000

def get_embedding(text, model="text-embedding-ada-002"): # model = "deployment_name"
    return client.embeddings.create(input = [text], model=model).data[0].embedding

    
input_datapath = "/Users/brock/Desktop/brockai/backend/services/Reviews.csv"  # to save space, we provide a pre-filtered dataset
df = pd.read_csv(input_datapath, index_col=0)
df = df[["Time", "ProductId", "UserId", "Score", "Summary", "Text"]]

df = df.dropna()

df["combined"] = (
    "Title: " + df.Summary.str.strip() + "; Content: " + df.Text.str.strip()
)

top_n = 1000
df = df.sort_values("Time").tail(top_n * 2)  # first cut to first 2k entries, assuming less than half will be filtered out
df.drop("Time", axis=1, inplace=True)

encoding = tiktoken.get_encoding(embedding_encoding)

# omit reviews that are too long to embed
df["n_tokens"] = df.combined.apply(lambda x: len(encoding.encode(x)))
df = df[df.n_tokens <= max_tokens].tail(top_n)
len(df)
    
embedding_model = "text-embedding-ada-002"
# This may take a few minutes
df["embedding_vector"] = df.combined.apply(lambda x: get_embedding(x, embedding_model))
df.to_csv("/Users/brock/Desktop/brockai/backend/services/data/processed/fine_food_reviews_with_embeddings_1k.csv")

# # create_index("reviews", df)

#   # answer_question(df, question="What is the best price for coffee?", debug=True)
    