import subprocess
import sys
import webbrowser
from pathlib import Path
from typing import Annotated


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
