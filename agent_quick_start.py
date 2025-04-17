import os
import subprocess
import sys
import webbrowser
from pathlib import Path
from typing import Annotated

from dotenv import load_dotenv
from IPython.display import Image, display
from langchain_anthropic import ChatAnthropic
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

load_dotenv()


class State(TypedDict):
    # Messages have type “list”. The add_messages annotation
    # tells StateGraph to append new messages rather than overwrite.
    messages: Annotated[list, add_messages]


def build_chat_graph() -> StateGraph:
    graph_builder = StateGraph(State)

    # LLM node
    llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")

    def chatbot(state: State):
        return {"messages": [llm.invoke(state["messages"])]}

    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", END)

    return graph_builder.compile()


def save_and_open_graph_png(graph, output_filename: str = "graph.png"):
    """
    Renders the graph to a Mermaid PNG, writes it to disk,
    and opens it using the default macOS image viewer.
    """
    # 1. Render PNG bytes
    png_bytes = graph.get_graph().draw_mermaid_png()

    # 2. Save to file
    output_path = Path(output_filename)
    output_path.write_bytes(png_bytes)
    print(f"Graph image saved to {output_path.resolve()}")

    # 3. Open with the default macOS viewer
    if sys.platform == "darwin":
        subprocess.run(["open", str(output_path)], check=False)
    else:
        # fallback: open in default browser if not on macOS
        webbrowser.open(output_path.resolve().as_uri())


if __name__ == "__main__":
    # Build your state graph
    graph = build_chat_graph()

    # Option 1: Display inline in Jupyter
    try:
        display(Image(graph.get_graph().draw_mermaid_png()))
    except Exception:
        pass

    # Option 2: Save to disk and open in Preview
    save_and_open_graph_png(graph, output_filename="graph.png")
