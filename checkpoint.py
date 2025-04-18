from operator import add
from typing import Annotated

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict


class State(TypedDict):
    foo: str
    bar: Annotated[list[str], add]


def node_a(state: State):
    print(state)
    return {"foo": "a", "bar": ["a"]}


def node_b(state: State):
    return {"foo": "b", "bar": ["b"]}


load_dotenv()

llm = init_chat_model("gpt-4o-mini", model_provider="openai")


workflow = StateGraph(State)
workflow.add_node(node_a)
workflow.add_node(node_b)
workflow.add_edge(START, "node_a")
workflow.add_edge("node_a", "node_b")
workflow.add_edge("node_b", END)

checkpointer = InMemorySaver()
graph = workflow.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "1"}}

# inputs que envías al grafo
inputs = {"foo": ""}

# mismo config que ya usas

graph.invoke(inputs, config)


print("==============================") 
print(graph.get_state(config).values)  # <- TypedDict/ Pydantic con todas las claves de State
print("*****************************") 
graph.invoke(inputs, config)

print("==============================") 
print(graph.get_state(config).config["configurable"]["checkpoint_id"])  # <- TypedDict/ Pydantic con todas las claves de State
print("*****************************") 
config_update = {"configurable": {"thread_id": "1", "checkpoint_id": graph.get_state(config).config["configurable"]["checkpoint_id"]}}
graph.invoke(None, config_update)

print("==============================") 
print(graph.get_state(config).values)  # <- TypedDict/ Pydantic con todas las claves de State

print("*****************************") 
# «values» ⇒ emite el *state* completo tras cada paso
# for step_state in graph.stream(inputs, config, stream_mode="values"):
#     print("‑‑ paso completado ‑‑")
#     print(graph.get_state(config))  # <- TypedDict/ Pydantic con todas las claves de State
#     # print(step_state)        # <- TypedDict/ Pydantic con todas las claves de State
# print(list(graph.get_state_history(config)))
# print(graph.get_state(config))  # <- TypedDict/ Pydantic con todas las claves de State
#
# for step_state in graph.stream(inputs, config, stream_mode="values"):
#     print("‑‑ paso completado ‑‑")
#     print(graph.get_state(config))  # <- TypedDict/ Pydantic con todas las claves de State
#     # print(step_state)        # <- TypedDict/ Pydantic con todas las claves de State
# print(list(graph.get_state_history(config)))
# print(graph.get_state(config))  # <- TypedDict/ Pydantic con todas las claves de State
