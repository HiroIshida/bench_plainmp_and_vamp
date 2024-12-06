## [WIP] Benchmark plainmp and VAMP
For plainmp implementation, please refer to the following repository: https://github.com/HiroIshida/plainmp
For VAMP implementation, please refer to the following repository: https://github.com/KavrakiLab/vamp
To change resolution, please modify the VAMP source code a bit and re-compile it.
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

This benchmark is still a work in progress.
The benchmark may unintentionally favor one implementation over the other, or have other issues.
Also, I need to double-check the fairness regarding the resolution in motion validation.

## Usage
```bash
python3 panda_plan.py
python3 panda_plan.py --difficult
python3 fetch_plan.py
```
\*same problem as in https://github.com/HiroIshida/plainmp/tree/master/example

```
optional arguments:
  --res  # int: (inverse) resolution of motion validation. Default is 32.
  --internal  # flag: use internal measurement. Default is False.
```


## LICENSE NOTICE
This repo contains code that interfaces with VAMP and is subject to 
Polyform Noncommercial License restrictions due to its dependency on VAMP.
Any use of this code must comply with the Polyform Noncommercial License terms.
At least, this repository is for hobby and research purposes only.
I don't know how to license this repository, so I just do not put any license here.
