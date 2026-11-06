"""Tests for config module."""
from src.nuget_viz.config import parse_args, validate_config


def test_parse_args_valid():
    """Tests parsing of valid arguments."""
    args = parse_args([
        "--package", "test", "--repo", "http://url",
        "--output", "out.svg"
    ])
    assert args.package == "test"
    assert validate_config(args) is True


def test_parse_args_invalid_output():
    """Tests invalid output extension."""
    args = parse_args([
        "--package", "test", "--repo", "http://url",
        "--output", "out.png"
    ])
    assert validate_config(args) is False
