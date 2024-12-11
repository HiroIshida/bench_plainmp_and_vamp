import argparse

import numpy as np
from plainmp.robot_spec import PandaSpec
from skrobot.model.primitives import Box, Cylinder

from lib import benchmark_plainmp_vs_vamp, plot_plainmp_vs_vamp, save_rawdata

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--difficult", action="store_true", help="difficult")
    parser.add_argument("--internal", action="store_true", help="use internal measurement")
    parser.add_argument("--res", type=int, help="resolution inverse", default=32)
    args = parser.parse_args()

    ground = Box([2.0, 2.0, 0.05])
    ground.translate([0, 0, -0.05])

    height = 1.0

    poll1 = Cylinder(0.05, height, face_colors=[100, 100, 200, 200])
    poll1.translate([0.3, 0.3, 0.5 * height])

    poll2 = Cylinder(0.05, height, face_colors=[100, 100, 200, 200])
    poll2.translate([-0.3, -0.3, 0.5 * height])

    primitives = [ground, poll1, poll2]

    if args.difficult:
        ceil = Box([2.0, 2.0, 0.05], face_colors=[100, 200, 100, 200])
        ceil.translate([0, 0, height])
        primitives.append(ceil)

    n_sample = 10000
    q_start = np.array([-1.54, 1.54, 0, -0.1, 0, 1.5, 0.81])
    q_goal = np.array([1.54, 1.54, 0, -0.1, 0, 1.5, 0.81])
    times_plainmp, times_vamp = benchmark_plainmp_vs_vamp(
        PandaSpec(), q_start, q_goal, primitives, args.res, n_sample, args.internal
    )
    domain = "panda_dual_bars"
    if args.difficult:
        domain += "_difficult"
    plot_plainmp_vs_vamp(times_plainmp, times_vamp, domain, args.res, args.internal)
    save_rawdata(times_plainmp, times_vamp, domain, args.res, args.internal)
