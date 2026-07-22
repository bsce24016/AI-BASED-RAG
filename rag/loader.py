from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader
)

import os


def load_documents(folder_path="uploads"):

    documents = []

    for file in os.listdir(folder_path):

        path = os.path.join(folder_path, file)

        if file.endswith(".pdf"):

            loader = PyPDFLoader(path)

        elif file.endswith(".txt"):

            loader = TextLoader(path, encoding="utf-8")

        elif file.endswith(".docx"):

            loader = Docx2txtLoader(path)

        else:

            continue

        documents.extend(loader.load())

    return documents