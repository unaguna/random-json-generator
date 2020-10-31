import sys
import argparse
from . import gen

parser = argparse.ArgumentParser(description="Generate json file randomly according to json schema.")

parser.add_argument("schema_file_path", help="Path of json schema file. This file is used as base schema.")
parser.add_argument("--jsonoutput", "-j", help="Path to which json file is written.")

args = parser.parse_args()

# 出力先を決定
output_file, output_fp = (args.jsonoutput, None) \
    if args.jsonoutput is not None \
    else (None, sys.stdout)

gen(schema_file=args.schema_file_path, output_file=output_file, output_fp=output_fp)
