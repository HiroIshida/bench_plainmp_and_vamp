import argparse

import numpy as np
from plainmp.robot_spec import FetchSpec
from skrobot.model.primitives import Box

from lib import benchmark_plainmp_vs_vamp, plot_plainmp_vs_vamp, save_rawdata

parser = argparse.ArgumentParser()
parser.add_argument("--internal", action="store_true", help="use internal measurement")
parser.add_argument("--res", type=int, help="resolution inverse", default=32)
args = parser.parse_args()

if __name__ == "__main__":
    q_start = np.array([0.0, 1.32, 1.40, -0.20, 1.72, 0.0, 1.66, 0.0])
    q_goal = np.array([0.386, 0.205, 1.41, 0.308, -1.82, 0.245, 0.417, 6.01])
    table = Box([1.0, 2.0, 0.05], face_colors=[100, 200, 100, 200])
    table.translate([0.95, 0.0, 0.8])
    n_sample = 10000
    times_plainmp, times_vamp = benchmark_plainmp_vs_vamp(
        FetchSpec(), q_start, q_goal, [table], args.res, n_sample, args.internal
    )
    plot_plainmp_vs_vamp(times_plainmp, times_vamp, "fetch_table", args.res, args.internal)
    save_rawdata(times_plainmp, times_vamp, "fetch_table", args.res, args.internal)
