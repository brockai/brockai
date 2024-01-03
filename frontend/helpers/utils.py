import streamlit as st
import numpy as np
import execjs
import os
from typing import List
from scipy import spatial

from openai import OpenAI
from IPython.display import display

client = OpenAI(
    api_key=os.getenv("OPENAI_KEY")
)

# embedding model parameters
embedding_model = "text-embedding-ada-002"
embedding_encoding = "cl100k_base"  # this the encoding for text-embedding-ada-002
max_tokens = 8000  # the maximum for text-embedding-ada-002 is 8191

def get_token():
  ctx = execjs.compile("""
    function getLocalStorageItem(key) {
        return localStorage.getItem(key);
    }
    """)
  token = ctx.call("get_token", "accessToken")
  return token

@st.cache_data(show_spinner=True)
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

@st.cache_data(show_spinner=True)
def get_embedding(text, model="text-embedding-ada-002"): # model = "deployment_name"
    return client.embeddings.create(input = [text], model=model).data[0].embedding

@st.cache_data(show_spinner=True)
def search_docs(df, user_query, top_n=4, to_print=True):
    embedding = get_embedding(
        user_query,
        model="text-embedding-ada-002" # model should be set to the deployment name you chose when you deployed the text-embedding-ada-002 (Version 2) model
    )
    df["similarities"] = df.ada_v2.apply(lambda x: cosine_similarity(x, embedding))

    res = (
        df.sort_values("similarities", ascending=False)
        .head(top_n)
    )
    if to_print:
        display(res)
    return res

@st.cache_data(show_spinner=True)
def query(_pipeline, question):
    params = {}
    results = _pipeline.run(question, params=params)
    return results

@st.cache_data(show_spinner=True)
def indices_of_nearest_neighbors_from_distances(distances) -> np.ndarray:
    """Return a list of indices of nearest neighbors from a list of distances."""
    return np.argsort(distances)

def distances_from_embeddings(
    query_embedding: List[float],
    embeddings: List[List[float]],
    distance_metric="cosine",
) -> List[List]:
    """Return the distances between a query embedding and a list of embeddings."""
    distance_metrics = {
        "cosine": spatial.distance.cosine,
        "L1": spatial.distance.cityblock,
        "L2": spatial.distance.euclidean,
        "Linf": spatial.distance.chebyshev,
    }
    distances = [
        distance_metrics[distance_metric](query_embedding, embedding)
        for embedding in embeddings
    ]
    return distances

def create_context(
        question, df, max_len=1800, size="ada"
    ):
        """
        Create a context for a question by finding the most similar context from the dataframe
        """
        # Get the embeddings for the question
        q_embeddings = client.embeddings.create(input=question, model=embedding_model).data[0].embedding
    
        # Get the distances from the embeddings
        df['distances'] = distances_from_embeddings(q_embeddings, df['embedding'].values, distance_metric='cosine')
    
        returns = []
        cur_len = 0

        # Sort by distance and add the text to the context until the context is too long
        for i, row in df.sort_values('distances', ascending=True).iterrows():

            # Add the length of the text to the current length
            cur_len += row['n_tokens'] + 4

            # If the context is too long, break
            if cur_len > max_len:
                break

            # Else add it to the text that is being returned
            returns.append(row["Text"])

        # Return the context
        return "\n\n###\n\n".join(returns)

@st.cache_data(show_spinner=True)  
def answer_question(
    df,
    model="gpt-3.5-turbo",
    question="Am I allowed to publish model outputs to Twitter, without a human review?",
    max_len=1800,
    size="ada",
    debug=False,
    max_tokens=150,
    stop_sequence=None
):
  
    """
    Answer a question based on the most similar context from the dataframe texts
    """
    context = create_context(
        question,
        df,
        max_len=max_len,
        size=size,
    )
    
    st.dataframe(df.head(1000))
    # If debug, print the raw model response
    if debug:
        print("Context:\n" + context)
        print("\n\n")

    try:
        # Create a chat completion using the question and context
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Answer the question based on the context below, and if the question can't be answered based on the context, say \"I don't know\"\n\n"},
                {"role": "user", f"content": "Context: {context}\n\n---\n\nQuestion: {question}\nAnswer:"}
            ],
            temperature=0,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        stop=stop_sequence,
        )
        return response.choices[0].message.strip()
    except Exception as e:
        print(e)
        return ""