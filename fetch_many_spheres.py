import argparse

import numpy as np
from plainmp.robot_spec import FetchSpec
from skrobot.model.primitives import Box, Sphere

from lib import benchmark_plainmp_vs_vamp, plot_plainmp_vs_vamp, save_rawdata

parser = argparse.ArgumentParser()
parser.add_argument("--internal", action="store_true", help="use internal measurement")
parser.add_argument("--difficult", action="store_true", help="difficult")
parser.add_argument("--res", type=int, help="resolution inverse", default=32)
args = parser.parse_args()

if __name__ == "__main__":
    np.random.seed(7)  # fixed to make feasible problem
    ground = Box([1.0, 1.0, 0.05])
    ground.translate([0, 0, -0.1])
    primitives = [ground]
    n_sphere = 9 if args.difficult else 4
    for _ in range(n_sphere):
        sphere = Sphere(0.15, with_sdf=True)
        x = np.random.uniform(0.2, 1) + 0.2
        y = np.random.uniform(-0.6, 0.6) * -1
        z = np.random.uniform(0.3, 1.5)
        sphere.translate([x, y, z])
        primitives.append(sphere)
    q_start = np.array([0.0, 1.31999949, 1.40000015, -0.20000077, 1.71999929, 0.0, 1.6600001, 0.0])
    q_goal = np.array([0.386, 0.20565, 1.41370, 0.30791, -1.82230, 0.24521, 0.41718, 6.01064])
    n_sample = 10000
    times_plainmp, times_vamp = benchmark_plainmp_vs_vamp(
        FetchSpec(), q_start, q_goal, primitives, args.res, n_sample, args.internal
    )
    plot_plainmp_vs_vamp(times_plainmp, times_vamp, "fetch_many_spheres", args.res, args.internal)
    save_rawdata(times_plainmp, times_vamp, "fetch_maby_spheres", args.res, args.internal)
