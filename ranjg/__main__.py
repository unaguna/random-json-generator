import sys
import argparse
from . import gen

def parse_args():
    parser = argparse.ArgumentParser(description="Generate json file randomly according to json schema.")

    parser.add_argument("schema_file_path", help="Path of json schema file. This file is used as base schema.")
    parser.add_argument("--jsonoutput", "-j", help="Path to which json file is written.")

    return parser.parse_args()

def get_output_target(args):
    if args.jsonoutput is not None:
        return args.jsonoutput, None
    else:
        return None, sys.stdout

args = parse_args()

# 出力先を決定
output_file, output_fp = get_output_target(args)

gen(schema_file=args.schema_file_path, output_file=output_file, output_fp=output_fp)
