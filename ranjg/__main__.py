import argparse
from . import gen

parser = argparse.ArgumentParser(description="Generate json file randomly according to json schema.")

parser.add_argument("schema_file_path", help="Path of json schema file. This file is used as base schema.")
parser.add_argument("--outputpath", "-o", required=True, help="Path to which json file is written.")

args = parser.parse_args()

gen(schema_file=args.schema_file_path, output_file=args.outputpath)
