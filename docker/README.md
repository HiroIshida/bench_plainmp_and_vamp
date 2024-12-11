build
```
docker build -t plainmp_bench .
```
benchmark # with command
```
docker run -it --rm plainmp_bench  \
    /bin/bash -c "cd bench_plainmp_and_vamp && ./run_bench.sh"

```
