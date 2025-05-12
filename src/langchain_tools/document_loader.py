from langchain_community.document_loaders import TextLoader

def load_documents_from_folder(folder_path: str):
    """
    Load all text documents from a specified folder.

    Args:
        folder_path (str): The path to the folder containing text documents.

    Returns:
        list: A list of loaded documents.
    """
    loader = TextLoader(folder_path)
    documents = loader.load()
    return documents