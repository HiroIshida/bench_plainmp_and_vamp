## Benchmark plainmp and VAMP
TL;DR: On x86_64 (with 256-bit AVX), VAMP is significantly faster than plainmp. On ARM (with 128-bit NEON), although it is case-by-case VAMP and plainmp seem to have similar but maybe slightly on the side of VAMP.

## bechmark result (--internal)
\* all the values are median execution times in milliseconds (ms)

\* resolution 20 for typical settings for my demo, 32 for the default resolution of VAMP

\* plainmp: https://github.com/HiroIshida/plainmp (v0.1.0) @83de8d5

\* VAMP: https://github.com/KavrakiLab/vamp (v0.3.0) @0d13c50

On AMD Ryzen 7 7840HS for x86_64
| Scene Name | plainmp (ms) | vamp (ms) |
|------------|--------------|-----------|
| panda_dual_bars_res20 | 0.206 | 0.153 |
| panda_dual_bars_res32 | 0.298 | 0.198 |
| panda_dual_bars_difficult_res20 | 0.835 | 0.856 |
| panda_dual_bars_difficult_res32 | 1.133 | 1.048 |
| fetch_table_res20 | 0.773 | 0.197 |
| fetch_table_res32 | 1.164 | 0.240 |
| fetch_many_spheres_res20 | 0.296 | 0.029 |
| fetch_many_spheres_res32 | 0.444 | 0.035 |

On ARM Neoverse-N1 for aarch64
| Scene Name | plainmp (ms) | vamp (ms) |
|------------|--------------|-----------|
| panda_dual_bars_res20 | 0.404 | 0.686 |
| panda_dual_bars_res32 | 0.557 | 1.053 |
| panda_dual_bars_difficult_res20 | 1.451 | 3.329 |
| panda_dual_bars_difficult_res32 | 2.059 | 4.968 |
| fetch_table_res20 | 1.349 | 0.608 |
| fetch_table_res32 | 1.881 | 0.860 |
| fetch_many_spheres_res20 | 0.563 | 0.129 |
| fetch_many_spheres_res32 | 0.801 | 0.184 |

Note: All values are median execution times in milliseconds (ms).

## Usage
```bash
python3 panda_plan.py --internal
python3 panda_plan.py --difficult --internal
python3 fetch_plan.py --interanl
python3 fetch_many_spheres.py --internal
```
\* panda_plan and fetch_plan are the same in https://github.com/HiroIshida/plainmp/tree/master/example
```
optional arguments:
  --res  # int: (inverse) resolution of motion validation. Default is 32.
  --internal  # flag: use internal measurement. Default is False.
```
NOTE: The --internal flag in VAMP significantly affects measurements since memory allocation for RRTConnect nodes (0.2ms) is included in raw times but excluded from internal times. As this overhead is an API design consideration rather than algorithmic, comparing results with --internal seems to be more fair.

## How to change resolution of VAMP
The default (inverse) resolution is 32. To change the resolution to 1/24 of fetch and panda robots, for example, you need to modify the following files:
```diff
diff --git a/src/impl/vamp/robots/fetch.hh b/src/impl/vamp/robots/fetch.hh
index 2257902..83059c3 100644
--- a/src/impl/vamp/robots/fetch.hh
+++ b/src/impl/vamp/robots/fetch.hh
@@ -9,7 +9,7 @@ namespace vamp::robots
     {
         static constexpr auto name = "fetch";
         static constexpr auto dimension = 8;
-        static constexpr auto resolution = 32;
+        static constexpr auto resolution = 24;
         static constexpr auto n_spheres = fetch::n_spheres;
         static constexpr auto space_measure = fetch::space_measure;
         using Configuration = FloatVector<dimension>;
diff --git a/src/impl/vamp/robots/panda.hh b/src/impl/vamp/robots/panda.hh
index 61672c9..fc11a8e 100644
--- a/src/impl/vamp/robots/panda.hh
+++ b/src/impl/vamp/robots/panda.hh
@@ -9,7 +9,7 @@ namespace vamp::robots
     {
         static constexpr auto name = "panda";
         static constexpr auto dimension = 7;
-        static constexpr auto resolution = 32;
+        static constexpr auto resolution = 24;
         static constexpr auto n_spheres = panda::n_spheres;
         static constexpr auto space_measure = panda::space_measure;
``` 
Then, re-compile VAMP.


## LICENSE NOTICE
This repo contains code that interfaces with VAMP and is subject to 
Polyform Noncommercial License restrictions due to its dependency on VAMP.
Any use of this code must comply with the Polyform Noncommercial License terms.
At least, this repository is for hobby and research purposes only.
I don't know how to license this repository, so I just do not put any license here.
