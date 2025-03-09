from googleapiclient.discovery import build
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import CSVLoader, WebBaseLoader, MergedDataLoader
import pandas as pd
import os

service = build("factchecktools", "v1alpha1", developerKey="AIzaSyC_TbIg8TAXmFgn8RkOT-cYvnRTk6ULxRQ")

llm = ChatGroq(
    api_key="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",
    model_name="mixtral-8x7b-32768"
)

# Load and process documents
def load_documents(persist_directory="chroma_verify_db"):
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Check if precomputed vector store exists
    if os.path.exists(persist_directory) and os.listdir(persist_directory):
        print(f"Loading precomputed vector store from {persist_directory}")
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
        return vectorstore

    print(f"Building new vector store and saving to {persist_directory}")

    # Load CSV dataset
    file_path = os.path.join(current_dir, "COVID Fake News Data.csv")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV file not found at: {file_path}")
    csv_loader = CSVLoader(file_path=file_path, encoding="utf-8")
    docs1 = csv_loader.load()

    # Load Web Data
    web_loader = WebBaseLoader(
        "https://theonion.com/",
        requests_kwargs={"headers": {"User-Agent": "YourAppName/1.0"}}
    )
    docs2 = web_loader.load()

    # Merge datasets
    merged_loader = MergedDataLoader(loaders=[csv_loader, web_loader])
    docs = merged_loader.load()

    # Apply text splitting
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # Initialize embeddings and vector store with persistence
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=persist_directory
    )

    # Ensure data is saved (often automatic in newer Chroma versions)
    vectorstore.persist()
    print(f"Vector store saved to {persist_directory}")
    return vectorstore

# Initialize with persistence
vectorstore = load_documents(persist_directory="chroma_verify_db")

def load_teacher_documents(persist_directory="chroma_teacher_db"):
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Check if precomputed vector store exists
    if os.path.exists(persist_directory) and os.listdir(persist_directory):
        print(f"Loading precomputed teacher vector store from {persist_directory}")
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
        return vectorstore

    print(f"Building new teacher vector store and saving to {persist_directory}")

    # Load first CSV file
    file_path1 = os.path.join(current_dir, "COVID Fake News Data.csv")
    if not os.path.exists(file_path1):
        raise FileNotFoundError(f"CSV file not found at: {file_path1}")
    csv_loader1 = CSVLoader(file_path=file_path1, encoding="utf-8")
    docs1 = csv_loader1.load()

    # Load second CSV file
    file_path2 = os.path.join(current_dir, "Fake.csv")
    if not os.path.exists(file_path2):
        raise FileNotFoundError(f"CSV file not found at: {file_path2}")
    csv_loader2 = CSVLoader(file_path=file_path2, encoding="utf-8")
    docs2 = csv_loader2.load()

    # Load third CSV file
    file_path3 = os.path.join(current_dir, "tips.csv")
    if not os.path.exists(file_path3):
        raise FileNotFoundError(f"CSV file not found at: {file_path3}")
    csv_loader3 = CSVLoader(file_path=file_path3, encoding="utf-8")
    docs3 = csv_loader3.load()

    # Combine documents
    combined_docs = docs1 + docs2 + docs3

    # Apply text splitting
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    splits = text_splitter.split_documents(combined_docs)

    # Initialize embeddings and vector store with persistence
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=persist_directory
    )

    vectorstore.persist()
    print(f"Teacher vector store saved to {persist_directory}")
    return vectorstore

# Initialize with persistence
teacher_vectorstore = load_teacher_documents(persist_directory="chroma_teacher_db")

def verify_misinformation(claim):
    """
    Verifies a claim using Google's Fact Check Tools API.
    :param claim: The claim to verify.
    :return: A formatted string with the fact-checking result or a message if no results are found.
    """
    try:
        response = service.claims().search(query=claim).execute()
        claims = response.get('claims', [])

        if not claims:
            return "No fact-check results found for this statement."
        claim_review = claims[0].get('claimReview', [])[0]
        publisher = claim_review.get('publisher', {}).get('name', 'Unknown publisher')
        url = claim_review.get('url', 'No URL')
        rating = claim_review.get('textualRating', 'No rating provided')

        result = (f"**Fact-Check Result:**\n"
                  f"- **Publisher:** {publisher}\n"
                  f"- **Rating:** {rating}\n"
                  f"- **URL:** {url}\n")
        return result

    except Exception as e:
        return f"An error occurred: {e}"

def verify_and_correct_statement(statement: str, num_docs: int = 1):
    """
    Verifies the accuracy of a statement using ChromaDB and Google Fact Check API,
    and provides corrections if misinformation is detected.
    :param statement: The statement to verify.
    :param num_docs: Number of documents to retrieve from ChromaDB.
    :return: Verification result and corrections if applicable.
    """
    docs = vectorstore.similarity_search(statement, k=num_docs)

    if docs:
        context = "\n\n".join([doc.page_content for doc in docs])
        fact_check_result = "Fact-checking skipped (reliable ChromaDB source found)."
    else:
        context = "No relevant articles found in ChromaDB."
        fact_check_result = verify_misinformation(statement)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an AI assistant specialized in fact-checking.
        Evaluate the following statement for accuracy. If it's false or misleading,
        provide the correct information and cite credible sources. Do not ask follow up questions or request supporting information. 

        Statement:
        {statement}

        Context:
        {context}

        Fact-Check:
        {fact_check_result}
        """),
        ("human", "{statement}")
    ])

    formatted_prompt = prompt.format(
        statement=statement,
        context=context,
        fact_check_result=fact_check_result
    )

    response = llm.invoke(formatted_prompt, frequency_penalty=0.5)

    return response.content


# def teach_deepfakes_and_misinfo(user_input: str, history: str) -> str:
#     """
#     Engages the user in a conversational manner to teach about deepfakes and misinformation.
#     Uses a vector store loaded from a CSV file to provide context-aware responses.
#     :param user_input: The user's current message.
#     :param history: The conversation history as a string.
#     :return: A conversational, educational response from the LLM.
#     """
#     docs = teacher_vectorstore.similarity_search(user_input, k=2)
#     context = "\n\n".join([doc.page_content for doc in docs]) if docs else "No relevant data found in the knowledge base."

#     prompt = ChatPromptTemplate.from_messages([
#         ("system", """You are an expert educator on identifying deepfakes and misinformation. 
#         Do not give random advice unless explicitly requested.
#         Your goal is to help users learn about these topics through conversational dialogue, provide sources for claims if possible. 
#         Use clear explanations, examples while being brief. Use the conversation history and provided context to provide context-aware responses and build on previous discussions, do not repeat things.

#         Conversation History:
#         {history}

#         Context from Knowledge Base:
#         {context}

#         Current User Message:
#         {user_input}
#         """),
#         ("human", "{user_input}")
#     ])

#     formatted_prompt = prompt.format(
#         history=history if history else "No previous conversation history.",
#         context=context,
#         user_input=user_input
#     )
    
#     try:
#         response = llm.invoke(formatted_prompt, frequency_penalty=0.5)
#         return response.content
#     except Exception as e:
#         return f"An error occurred while generating a response: {str(e)}"

def teach_deepfakes_and_misinfo(user_input: str, history: str) -> str:
    """
    Engages the user in a conversational manner to teach about deepfakes and misinformation.
    Provides structured but concise answers with sources while maintaining conversation flow.
    
    :param user_input: The user's current message.
    :param history: The conversation history as a string.
    :return: A well-structured, conversational response from the LLM.
    """
    # Retrieve only the most relevant document for faster response time
    docs = teacher_vectorstore.similarity_search(user_input, k=1)
    context = docs[0].page_content if docs else "No relevant data found in the knowledge base."

    # Limit conversation history to last 4 exchanges to keep responses relevant
    history_lines = history.split("\n")[-8:] if history else ["No previous conversation history."]
    formatted_history = "\n".join(history_lines)

    # Improved prompt for better flow
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an AI misinformation expert. Your job is to provide **clear, factual answers** while maintaining a smooth conversation. 
        - **If a claim is true**, confirm it and provide a reliable source.
        - **If a claim is false**, debunk it with a short explanation and a credible source.
        - **If there's no clear answer**, provide an analysis and suggest ways to verify the claim.
        - Keep responses **concise, engaging, and natural** while ensuring they remain informative.

        **Response Format:**
        - **Answer in a paragraph** (not too short, not too long).
        - **Always include at least one credible source.**
        - **Be conversational and prepared for follow-up questions.**

        **Recent Conversation History:**
        {formatted_history}

        **Context from Knowledge Base:**
        {context}

        **User Message:**
        {user_input}

        **Your Response:**
        """),
        ("human", "{user_input}")
    ])

    formatted_prompt = prompt.format(
        formatted_history=formatted_history,
        context=context,
        user_input=user_input
    )

    try:
        response = llm.invoke(formatted_prompt, frequency_penalty=0.1)  # Lower penalty for faster response
        return response.content if hasattr(response, "content") else str(response)

    except Exception as e:
        return f"An error occurred while generating a response: {str(e)}"
