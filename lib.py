"""
This file contains code that interfaces with VAMP and is subject to
Polyform Noncommercial License restrictions due to its dependency on VAMP.
Any use of this code must comply with the Polyform Noncommercial License terms.
"""

import json
import time
from pathlib import Path
from typing import List, Sequence, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import vamp
from plainmp.ompl_solver import OMPLSolver, set_log_level_none
from plainmp.problem import Problem
from plainmp.psdf import UnionSDF
from plainmp.robot_spec import FetchSpec, PandaSpec, RobotSpec
from plainmp.utils import primitive_to_plainmp_sdf
from skrobot.coordinates import rpy_angle
from skrobot.model.primitives import Box, Cylinder, Sphere


def add_skrobot_primitive_to_vamp_env(env, skshape: Union[Box, Sphere, Cylinder]) -> None:
    pos = skshape.worldpos()
    ypr = rpy_angle(skshape.worldrot())[0]
    rpy = [ypr[2], ypr[1], ypr[0]]
    if isinstance(skshape, Box):
        cub = vamp.Cuboid(pos, rpy, np.array(skshape._extents) * 0.5)
        env.add_cuboid(cub)
    elif isinstance(skshape, Sphere):
        sphere = vamp.Sphere(pos, skshape.radius)
        env.add_sphere(sphere)
    elif isinstance(skshape, Cylinder):
        cylinder = vamp.Cylinder(pos, rpy, skshape.radius, skshape.height)
        env.add_capsule(cylinder)
    else:
        raise ValueError("Unknown primitive type")


def benchmark_plainmp(
    spec: RobotSpec,
    q_start: np.ndarray,
    q_goal: np.ndarray,
    primitive_list: Sequence[Union[Box, Sphere, Cylinder]],
    resolution_inverse: int,
    n_sample: int,
    internal: bool,
) -> List[float]:

    cst = spec.create_collision_const()
    sdf_list = [primitive_to_plainmp_sdf(p) for p in primitive_list]
    cst.set_sdf(UnionSDF(sdf_list))
    lb, ub = spec.angle_bounds()
    resolution = 1.0 / resolution_inverse
    problem = Problem(
        q_start, lb, ub, q_goal, cst, None, resolution, "euclidean"
    )  # use euclidean rather than Box, to be consistent with vamp
    solver = OMPLSolver()

    set_log_level_none()
    time_list_plainmp = []
    for _ in range(n_sample):
        ts = time.time()
        ret = solver.solve(problem)
        if internal:
            time_list_plainmp.append(ret.ns_internal * 0.000001)  # nano to milli
        else:
            time_list_plainmp.append((time.time() - ts) * 1000)  # sec to ms
        assert ret.success
    return time_list_plainmp


def benchmark_vamp(
    spec: RobotSpec,
    q_start: np.ndarray,
    q_goal: np.ndarray,
    primitive_list: Sequence[Union[Box, Sphere, Cylinder]],
    resolution_inverse: int,
    n_sample: int,
    internal: bool,
) -> List[float]:

    env = vamp.Environment()

    if isinstance(spec, FetchSpec):
        robot_name = "fetch"
    elif isinstance(spec, PandaSpec):
        robot_name = "panda"
    else:
        assert False, "not supported"

    comment = f"compiled resolution_inverse: {vamp.fetch.resolution()} mismatch with resolution_inverse: {resolution_inverse}"
    comment += (
        "\n You need to re-compile vamp by changing the resolution in robot spec (e.g. fetch.hh)"
    )
    if robot_name == "fetch":
        assert vamp.fetch.resolution() == resolution_inverse, comment
    elif robot_name == "panda":
        assert vamp.panda.resolution() == resolution_inverse, comment
    else:
        assert False, "not supported"

    for p in primitive_list:
        add_skrobot_primitive_to_vamp_env(env, p)
    (
        vamp_module,
        planner_func,
        plan_settings,
        simp_settings,
    ) = vamp.configure_robot_and_planner_with_kwargs(robot_name, "rrtc")

    time_list_vamp = []
    vamp_results = []
    for i in range(n_sample):
        sampler = vamp_module.halton()
        sampler.reset()
        sampler.skip(i)
        ts = time.time()
        res = planner_func(q_start, q_goal, env, plan_settings, sampler)
        elapsed = time.time() - ts
        if internal:
            elapsed = res.nanoseconds
            time_list_vamp.append(elapsed * 0.000001)  # nano to milli
        else:
            time_list_vamp.append(elapsed * 1000)  # sec to ms
        assert res.solved
        vamp_results.append(np.array(res.path.numpy()))
    return time_list_vamp


def benchmark_plainmp_vs_vamp(
    spec: RobotSpec,
    q_start: np.ndarray,
    q_goal: np.ndarray,
    primitive_list: Sequence[Union[Box, Sphere, Cylinder]],
    resolution_inverse: int,
    n_sample: int,
    internal: bool,
) -> Tuple[List[float], List[float]]:

    print("start benchmarking plainmp...")
    time_list_plainmp = benchmark_plainmp(
        spec, q_start, q_goal, primitive_list, resolution_inverse, n_sample, internal
    )

    print("start benchmarking vamp...")
    time_list_vamp = benchmark_vamp(
        spec, q_start, q_goal, primitive_list, resolution_inverse, n_sample, internal
    )

    return time_list_plainmp, time_list_vamp


def save_rawdata(
    time_list_plainmp: List[float],
    time_list_vamp: List[float],
    domain_name: str,
    resolution_inverse: int,
    internal: bool,
) -> None:
    if internal:
        file_name = f"{domain_name}_res{resolution_inverse}_internal.json"
    else:
        file_name = f"{domain_name}_res{resolution_inverse}.json"
    print(f"save to {file_name}")
    file_path = Path.cwd() / "rawdata" / file_name
    with open(file_path, "w") as f:
        json.dump({"plainmp": time_list_plainmp, "vamp": time_list_vamp}, f)


def plot_plainmp_vs_vamp(
    time_list_plainmp: List[float],
    time_list_vamp: List[float],
    domain_name: str,
    resolution_inverse: int,
    internal: bool,
    interactive: bool = False,
) -> None:
    plainmp_median = np.median(time_list_plainmp)
    print(f"plainmp median: {plainmp_median} ms")
    vamp_median = np.median(time_list_vamp)
    print(f"vamp median: {vamp_median} ms")

    min_value = min(min(time_list_plainmp), min(time_list_vamp))
    max_value = max(max(time_list_plainmp), max(time_list_vamp))

    bins = np.logspace(np.log10(min_value), np.log10(max_value), 50)
    fig, ax = plt.subplots(figsize=(6, 3.2))
    ax.grid(which="both", axis="both", color="gray", linestyle="--", linewidth=0.5)
    ax.hist(
        time_list_plainmp,
        bins=bins,
        alpha=0.3,
        color="blue",
        edgecolor="black",
        label="plainmp hist",
    )
    ax.hist(time_list_vamp, bins=bins, alpha=0.3, color="red", edgecolor="black", label="vamp hist")
    ax.axvline(plainmp_median, color="blue", linestyle="-", label="plainmp median")
    ax.axvline(vamp_median, color="red", linestyle="-", label="vamp median")
    ax.set_xscale("log")
    ax.set_xlabel("planning time [ms]", fontsize=14)
    ax.set_ylabel("Frequency", fontsize=14)
    ax.set_xticks([0.1, 1, 10])
    ax.set_xticklabels(["0.1", "1", "10"], fontsize=14)
    ax.legend(fontsize=10)
    plt.tight_layout()
    if interactive:
        plt.show()
    else:
        figure_path = Path.cwd() / "figures"
        figure_path = Path("figures")
        figure_path.mkdir(exist_ok=True)
        if internal:
            file_path = (
                figure_path / f"plainmp_vs_vamp_{domain_name}_res{resolution_inverse}_internal.png"
            )
        else:
            file_path = figure_path / f"plainmp_vs_vamp_{domain_name}_res{resolution_inverse}.png"
        print(f"save to {file_path}")
        plt.savefig(file_path, dpi=200)
