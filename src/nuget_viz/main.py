"""Main entry point for NuGet Visualizer."""
import sys
import argparse
from .config import parse_args, print_config, validate_config
from .fetcher import fetch_nuspec, load_test_graph
from .graph import build_bfs_graph, get_loading_order
from .visualizer import generate_d2, render_svg, print_ascii_tree


def process_graph(args: argparse.Namespace) -> dict[str, list[str]]:
    """Builds the dependency graph based on mode."""
    if args.test_mode:
        test_graph = load_test_graph(args.repo)
        return build_bfs_graph(
            args.package, test_graph, args.repo, args.version, None
        )
    return build_bfs_graph(
        args.package, None, args.repo, args.version, fetch_nuspec
    )


def print_results(graph: dict[str, list[str]], package: str) -> None:
    """Prints direct dependencies, graph and loading order."""
    print("\n--- Direct Dependencies ---")
    print(f"{package}: {graph.get(package, [])}")
    print("\n--- Dependency Graph ---")
    for k, v in graph.items():
        print(f"{k} -> {v}")
    print("\n--- Loading Order ---")
    try:
        order = get_loading_order(graph)
        print(" -> ".join(order))
    except ValueError as err:
        print(f"Warning: {err}")


def render_graph(
    graph: dict[str, list[str]], args: argparse.Namespace
) -> None:
    """Generates and saves D2/SVG visualization."""
    print("\n--- Visualization ---")
    d2_file = generate_d2(graph, args.output)
    render_svg(d2_file, args.output)
    print(f"Saved SVG to {args.output}")
    if args.ascii:
        print("\n--- ASCII Tree ---")
        print_ascii_tree(graph, args.package)


def main() -> None:
    """Orchestrates the application."""
    args = parse_args()
    print_config(args)

    if not validate_config(args):
        sys.exit(1)

    try:
        graph = process_graph(args)
        print_results(graph, args.package)
        render_graph(graph, args)
    except Exception as err:
        print(f"Fatal Error: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
