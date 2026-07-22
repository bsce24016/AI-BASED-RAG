from dotenv import load_dotenv

from langchain_groq import ChatGroq

from langchain_core.prompts import ChatPromptTemplate

from langchain.chains.combine_documents import create_stuff_documents_chain

load_dotenv()


def get_llm():

    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.3
    )


def get_rag_chain():

    prompt = ChatPromptTemplate.from_template(
        """
You are an Enterprise AI Assistant.

Answer ONLY using the provided context.

If the answer is not available inside the context, reply exactly:

"I couldn't find this information in the uploaded documents."

Context:
{context}

Conversation History:
{chat_history}

Question:
{input}
"""
    )

    llm = get_llm()

    return create_stuff_documents_chain(
        llm,
        prompt
    )