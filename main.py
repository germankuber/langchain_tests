import getpass
import os
from langchain.chat_models import init_chat_model

from langchain_core.messages import (
    BaseMessage,
)
from dotenv import load_dotenv
import os

# Cargar variables desde .env
load_dotenv()

# if not os.environ.get("OPENAI_API_KEY"):
#   os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")


# model = init_chat_model("gpt-4o-mini", model_provider="openai")

# response: BaseMessage =model.invoke("Hello, world!")
# print(response.content)
from langchain_openai import ChatOpenAI

# llm = ChatOpenAI()
# print(llm.invoke("Hello, world!"))
from langchain.chat_models import init_chat_model

from langchain_core.messages import HumanMessage, SystemMessage
llm = init_chat_model("gpt-4o-mini", model_provider="openai")



from typing import List

from langchain_core.tools import InjectedToolArg, tool
from typing_extensions import Annotated

user_to_pets = {}


@tool(parse_docstring=True)
def update_favorite_pets(
    pets: List[str], user_id: Annotated[str, InjectedToolArg]
) -> None:
    """Add the list of favorite pets.

    Args:
        pets: List of favorite pets to set.
        user_id: User's ID.
    """
    user_to_pets[user_id] = pets


@tool(parse_docstring=True)
def delete_favorite_pets(user_id: Annotated[str, InjectedToolArg]) -> None:
    """Delete the list of favorite pets.

    Args:
        user_id: User's ID.
    """
    if user_id in user_to_pets:
        del user_to_pets[user_id]


@tool(parse_docstring=True)
def list_favorite_pets(user_id: Annotated[str, InjectedToolArg]) -> None:
    """List favorite pets if any.

    Args:
        user_id: User's ID.
    """
    return user_to_pets.get(user_id, [])


from pprint import pprint
tools = [
    update_favorite_pets,
    delete_favorite_pets,
    list_favorite_pets,
]
def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b




from typing_extensions import Annotated, TypedDict
class add(TypedDict):
    """Add two integers."""

    # Annotations must have the type and can optionally include a default value and description (in that order).
    a: Annotated[int, ..., "First integer"]
    b: Annotated[int, ..., "Second integer"]





from typing import Optional

from pydantic import BaseModel, Field

# Pydantic
class Joke(BaseModel):
    """Joke to tell user."""

    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline to the joke")
    rating: Optional[int] = Field(
        default=None, description="How funny the joke is, from 1 to 10"
    )


structured_llm = llm.with_structured_output(Joke)

result = structured_llm.invoke("Tell me a joke about cats")
print(result)



















