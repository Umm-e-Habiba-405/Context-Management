from agents import Agent, Runner, function_tool, RunContextWrapper,trace
import asyncio
from pydantic import BaseModel
from connection import config
import rich


class LibraryBook(BaseModel):
    book_id:str|int
    book_title: str
    author_name: str
    is_available: bool


@function_tool
async def library_book(wrapper:RunContextWrapper[LibraryBook]):
    """
    Returns the library book profile from the provided context.
    """
    return wrapper.context


library= LibraryBook(
     book_id="BOOK-123",
    book_title="Python Programming",
    author_name="John Smith",
    is_available=True

)
library_book_agent=Agent(
name="Library Book Agent",
instructions=""" "You are a helpful library assistant. "
    "You have access to a library book's profile containing the book ID, title, author name, and availability status. "
    "Always answer using the provided book profile context. "
    "If the user asks for all book details, list each detail on a separate line in the format:\n"
    "Do not make up information that is not in the profile."
      """,
    tools=[library_book]
)




async def main():
    with trace("Library Book Agent"):
        result=await Runner.run(
            library_book_agent,
            """
            "What is the book ID?"
            "Please tell me the book title and author name."
            "Is this book available?"
            "Give me all the book details."
            "Who is the author of this book?"
            "Tell me the book title and availability status."
            "What's the ID and availability of this book?"
            Can you tell me the author name and whether this book is available?
            """,
            run_config=config,
            context=library
        )
        rich.print(result.final_output)




if __name__ == "__main__":
    asyncio.run(main())