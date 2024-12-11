FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    python3-dev \
    python3-pip \
    libeigen3-dev \
    libboost-all-dev \
    libompl-dev \
    libspatialindex-dev \
    freeglut3-dev \
    libsuitesparse-dev \
    libblas-dev \
    liblapack-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

RUN git clone https://github.com/HiroIshida/plainmp.git
WORKDIR /workspace/plainmp
RUN git submodule update --init
RUN pip install scikit-build
RUN pip install -e .

WORKDIR /workspace
RUN git clone https://github.com/KavrakiLab/vamp.git
WORKDIR /workspace/vamp

# for changing resolution
# RUN sed -i 's/static constexpr auto resolution = 32;/static constexpr auto resolution = 24;/' src/impl/vamp/robots/fetch.hh && \
#     sed -i 's/static constexpr auto resolution = 32;/static constexpr auto resolution = 24;/' src/impl/vamp/robots/panda.hh

RUN pip install . -v

WORKDIR /workspace
RUN pip install matplotlib
RUN git clone https://github.com/HiroIshida/bench_plainmp_and_vamp.git

WORKDIR /workspace/bench_plainmp_and_vamp

# Create entrypoint script
RUN echo '#!/bin/bash\n\
echo "Running Panda benchmark..."\n\
python3 /workspace/bench_plainmp_and_vamp/panda_plan.py\n\
python3 /workspace/bench_plainmp_and_vamp/panda_plan.py --internal\n\
echo "Running Panda difficult benchmark..."\n\
python3 /workspace/bench_plainmp_and_vamp/panda_plan.py --difficult\n\
python3 /workspace/bench_plainmp_and_vamp/panda_plan.py --difficult --internal\n\
echo "Running Fetch benchmark..."\n\
python3 /workspace/bench_plainmp_and_vamp/fetch_plan.py\n\
python3 /workspace/bench_plainmp_and_vamp/fetch_plan.py --internal' > /workspace/run_benchmarks.sh && \
chmod +x /workspace/run_benchmarks.sh

ENTRYPOINT ["/workspace/run_benchmarks.sh"]
