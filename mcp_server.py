from pydantic import Field

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}


@mcp.tool(
    name="read_doc_contents",
    description="Reads the contents of a document given its ID and returns it as a string.",
)
def read_document(
    doc_id: str = Field(description="The ID of the document to read."),
) -> str:
    """Reads the contents of a document given its ID.

    Args:
        doc_id (str): The ID of the document to read.

    Returns:
        str: The contents of the document.
    """

    return fetch_document(doc_id)


@mcp.tool(
    name="edit_doc_contents",
    description="Edits a document by replacing a string in the document with a new string. "
    "Returns the updated document contents.",
)
def edit_document(
    doc_id: str = Field(description="The ID of the document to edit."),
    old_string: str = Field(description="The text to replace. Match must be exact, including whitespaces."),
    new_string: str = Field(description="The text to replace the old text with."),
) -> str:
    """
    Edits a document by replacing a string in the document with a new string.
    Returns the updated document contents.

    Args:
        doc_id (str): The ID of the document to edit.
        old_string (str): The text to replace. Match must be exact, including whitespaces.
        new_string (str): The text to replace the old text with.

    Returns:
        str: The updated document contents.
    """

    content = fetch_document(doc_id)
    if old_string not in content:
        return content  # If the old string is not found, return the original content without making any changes.

    updated_doc = content.replace(old_string, new_string)
    update_document(doc_id, updated_doc)
    return updated_doc


@mcp.resource(uri="docs://documents", mime_type="application/json", description="A list of document IDs available in the system.")
def list_documents() -> list[str]:
    """Lists all document IDs available in the system.

    Returns:
        list[str]: A list of document IDs.
    """
    return list(docs.keys())


# TODO: Write a resource to return the contents of a particular doc
@mcp.resource(uri="docs://documents/{doc_id}", mime_type="text/plain", description="The contents of a particular document.")
def get_document(doc_id: str) -> str:
    """Gets the contents of a particular document.

    Args:
        doc_id (str): The ID of the document to retrieve.

    Returns:
        str: The contents of the document.
    """
    return fetch_document(doc_id)


# TODO: Write a prompt to rewrite a doc in markdown format
# TODO: Write a prompt to summarize a doc


def fetch_document(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document with id {doc_id} not found.")
    return docs[doc_id]


def update_document(doc_id: str, content: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document with id {doc_id} not found.")
    docs[doc_id] = content
    return docs[doc_id]


if __name__ == "__main__":
    mcp.run(transport="stdio")
