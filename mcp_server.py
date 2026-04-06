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
    return get_document(doc_id)


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
    content = get_document(doc_id)
    if old_string not in content:
        return content  # If the old string is not found, return the original content without making any changes.

    updated_doc = content.replace(old_string, new_string)
    set_document(doc_id, updated_doc)
    return updated_doc


@mcp.resource(
    "docs:/documents",
    mime_type="application/json"
)
def list_documents() -> list[str]:
    return list(docs.keys())


# TODO: Write a resource to return the contents of a particular doc
@mcp.resource(
        "docs:/documents/{doc_id}",
        mime_type="text/plain")
def get_document(doc_id:str) -> str:
    return get_document(doc_id)


# TODO: Write a prompt to rewrite a doc in markdown format
# TODO: Write a prompt to summarize a doc


def get_document(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document with id {doc_id} not found.")
    return docs[doc_id]


def set_document(doc_id: str, content: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document with id {doc_id} not found.")
    docs[doc_id] = content
    return docs[doc_id]


if __name__ == "__main__":
    mcp.run(transport="stdio")
