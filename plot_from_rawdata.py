import argparse
import json
from pathlib import Path

from lib import plot_plainmp_vs_vamp

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--difficult", action="store_true", help="difficult")
    parser.add_argument("--internal", action="store_true", help="use internal measurement")
    parser.add_argument("--res", type=int, help="resolution inverse", default=32)
    parser.add_argument("--domain", type=str, help="domain name", default="panda_dual_bars")
    args = parser.parse_args()
    domain = args.domain
    if args.difficult:
        domain += "_difficult"
    if args.internal:
        file_name = f"{args.domain}_res{args.res}_internal.json"
    else:
        file_name = f"{args.domain}_res{args.res}.json"
    rawdata_path = Path("./rawdata") / file_name
    with open(rawdata_path, "r") as f:
        rawdata = json.load(f)
    plot_plainmp_vs_vamp(
        rawdata["plainmp"], rawdata["vamp"], domain, args.res, args.internal, interactive=True
    )
