import sys
import argparse
from typing import Tuple, Optional, TextIO
from . import gen


def main():
    """A function to be called when the module is executed on the command line.
    """
    # 引数を取得
    args = parse_args()

    # 出力先を決定
    output_file, output_fp = get_output_target(args)

    gen(schema_file=args.schema_file_path, output_file=output_file, output_fp=output_fp, options_file=args.options,
        multiplicity=args.multiplicity,
        # To ensure that generated value is exposed to garbage collection earlier.
        no_output=True)


def parse_args():
    """Get and parse command line arguments.

    Returns:
        An object that holds the values obtained from the command line arguments.
    """
    parser = argparse.ArgumentParser(description="Generate json file randomly according to json schema.")

    parser.add_argument("schema_file_path", help="Path of json schema file. This file is used as base schema.")
    parser.add_argument("--json_output", "-j", help="Path to which json file is written.")
    parser.add_argument("--options", help="Path of options file.")
    parser.add_argument("--list", "-l", dest="multiplicity", type=int,
                        help="If specified, repeats the generation for the specified number of times "
                             "and outputs the results as a list.")

    return parser.parse_args()


def get_output_target(args) -> Tuple[Optional[str], Optional[TextIO]]:
    """Returns the values to be used as ``output_file`` and ``output_fp``, arguments of ``ranjg.gen``.

    Args:
        args: An object that holds the values obtained from the command line arguments.

    Returns:
        The values to be used as ``output_file`` and ``output_fp``, arguments of ``ranjg.gen``.
    """
    if args.json_output is not None:
        return args.json_output, None
    else:
        return None, sys.stdout


if __name__ == "__main__":
    main()
