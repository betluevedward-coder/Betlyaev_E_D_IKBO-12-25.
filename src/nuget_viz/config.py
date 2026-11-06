"""Configuration parsing and validation module."""
import argparse
import sys


def parse_args(args_list: list[str] | None = None) -> argparse.Namespace:
    """Parses command line arguments."""
    parser = argparse.ArgumentParser(description="NuGet Graph Visualizer")
    parser.add_argument("--package", required=True, help="Package name")
    parser.add_argument("--repo", required=True, help="Repository URL or path")
    parser.add_argument("--test-mode", action="store_true", help="Test mode")
    parser.add_argument("--version", default="latest", help="Version")
    parser.add_argument("--output", required=True, help="Output SVG file")
    parser.add_argument("--ascii", action="store_true", help="ASCII tree")
    return parser.parse_args(args_list)


def print_config(args: argparse.Namespace) -> None:
    """Prints configuration in key-value format."""
    print("--- Configuration ---")
    print(f"Package: {args.package}")
    print(f"Repository: {args.repo}")
    print(f"Test Mode: {args.test_mode}")
    print(f"Version: {args.version}")
    print(f"Output: {args.output}")
    print(f"ASCII Mode: {args.ascii}")
    print("---------------------")


def validate_config(args: argparse.Namespace) -> bool:
    """Validates configuration parameters."""
    if not args.package.strip():
        print("Error: Package name cannot be empty.", file=sys.stderr)
        return False
    if not args.output.endswith(".svg"):
        print("Error: Output must be an .svg file.", file=sys.stderr)
        return False
    if not args.test_mode and not args.repo.startswith("http"):
        print("Error: Real repo must be a valid URL.", file=sys.stderr)
        return False
    return True
