"""Visualizes graph as D2 diagram and ASCII tree."""
import subprocess


def generate_d2(graph: dict[str, list[str]], output_path: str) -> str:
    """Generates D2 diagram text and saves to file."""
    lines = []
    for parent, children in graph.items():
        for child in children:
            lines.append(f"{parent} -> {child}")
    d2_content = "\n".join(lines)
    d2_path = output_path.replace(".svg", ".d2")
    with open(d2_path, "w", encoding="utf-8") as file:
        file.write(d2_content)
    return d2_path


def render_svg(d2_path: str, svg_path: str) -> None:
    """Calls D2 CLI to render SVG."""
    try:
        subprocess.run(
            ["d2", d2_path, svg_path], check=True, capture_output=True
        )
    except FileNotFoundError:
        print("Warning: 'd2' binary not found. SVG not rendered.")
    except subprocess.CalledProcessError as err:
        print(f"Error rendering SVG: {err}")


def print_ascii_tree(
    graph: dict[str, list[str]], root: str, indent: int = 0
) -> None:
    """Prints ASCII tree of dependencies."""
    prefix = "  " * indent + f"|-- {root}"
    print(prefix)
    for child in graph.get(root, []):
        print_ascii_tree(graph, child, indent + 1)
