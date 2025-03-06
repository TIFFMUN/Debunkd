from googleapiclient.discovery import build
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import CSVLoader, WebBaseLoader, MergedDataLoader
import pandas as pd
import os

# Initialize the Fact Check Tools API service
service = build("factchecktools", "v1alpha1", developerKey="AIzaSyC_TbIg8TAXmFgn8RkOT-cYvnRTk6ULxRQ")

# Initialize the Large Language Model (LLM)
llm = ChatGroq(
    api_key="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",
    model_name="mixtral-8x7b-32768"
)

# Load and process documents
def load_documents():
    # Load CSV dataset
    # csv_loader = CSVLoader(file_path="debunkd\backend\chatbot\COVID Fake News Data.csv", encoding="utf-8")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "COVID Fake News Data.csv")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV file not found at: {file_path}")
    csv_loader = CSVLoader(file_path=file_path, encoding="utf-8")
    docs1 = csv_loader.load()

    # Load Web Data
    # web_loader = WebBaseLoader("https://theonion.com/")  # Example satire source
    web_loader = WebBaseLoader(
    "https://theonion.com/",
    requests_kwargs={"headers": {"User-Agent": "YourAppName/1.0"}}
    )

    docs2 = web_loader.load()

    # Merge both datasets correctly
    merged_loader = MergedDataLoader(loaders=[csv_loader, web_loader])
    docs = merged_loader.load()

    # Apply text splitting
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # Initialize embeddings and vectorstore
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)

    return vectorstore

vectorstore = load_documents()

def verify_misinformation(claim):
    """
    Verifies a claim using Google's Fact Check Tools API.
    :param claim: The claim to verify.
    :return: A formatted string with the fact-checking result or a message if no results are found.
    """
    try:
        # Search for the claim
        response = service.claims().search(query=claim).execute()
        claims = response.get('claims', [])

        if not claims:
            return "No fact-check results found for this statement."

        # Extract the first claim review
        claim_review = claims[0].get('claimReview', [])[0]
        publisher = claim_review.get('publisher', {}).get('name', 'Unknown publisher')
        url = claim_review.get('url', 'No URL')
        rating = claim_review.get('textualRating', 'No rating provided')

        # Format the result
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
    # 1. Retrieve relevant documents from ChromaDB
    docs = vectorstore.similarity_search(statement, k=num_docs)

    if docs:
        # 2. Format context from documents
        context = "\n\n".join([doc.page_content for doc in docs])
        fact_check_result = "Fact-checking skipped (reliable ChromaDB source found)."
    else:
        # 3. If no relevant documents in ChromaDB, call Google Fact Check API
        context = "No relevant articles found in ChromaDB."
        fact_check_result = verify_misinformation(statement)

    # 4. Create verification prompt
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

    # 5. Get formatted prompt
    formatted_prompt = prompt.format(
        statement=statement,
        context=context,
        fact_check_result=fact_check_result
    )

    # 6. Get response from LLM (ChatGroq)
    response = llm.invoke(formatted_prompt, frequency_penalty=0.5)

    return response.content