from __future__ import annotations

import argparse


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("formatter_class", argparse.RawTextHelpFormatter)
        super().__init__(*args, **kwargs)


def argument_parser(*args, **kwargs) -> ArgumentParser:
    return ArgumentParser(*args, **kwargs)


def add_standard_args(
    parser: argparse.ArgumentParser, *, allow_toon: bool = False
) -> None:
    """Add ACLI output flags to an argparse parser."""
    if getattr(parser, "_acli_standard_args", False):
        return
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--format",
        choices=["compact", "jsonl", "pretty", "toon"],
        dest="format",
        help="Output format. compact/jsonl is JSON Lines; pretty is indented JSON; toon is flat-table TOON.",
    )
    group.add_argument(
        "--compact",
        action="store_const",
        const="compact",
        dest="format",
        help="Output compact JSON Lines.",
    )
    group.add_argument(
        "--pretty",
        action="store_const",
        const="pretty",
        dest="format",
        help="Output indented JSON.",
    )
    group.add_argument(
        "--toon",
        action="store_const",
        const="toon",
        dest="format",
        help="Output TOON; valid only for table-producing subcommands.",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Include the full structured schema instead of the minimal default.",
    )
    parser.set_defaults(format=None, full=False, acli_toon_allowed=allow_toon)
    setattr(parser, "_acli_standard_args", True)
