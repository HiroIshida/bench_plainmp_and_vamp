FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
ARG VAMP_RESOLUTION=32

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

RUN pip install . -v  # run this first to install dependencies (for caching)
RUN sed -i "s/static constexpr auto resolution = 32;/static constexpr auto resolution = $VAMP_RESOLUTION;/" src/impl/vamp/robots/fetch.hh && \
    sed -i "s/static constexpr auto resolution = 32;/static constexpr auto resolution = $VAMP_RESOLUTION;/" src/impl/vamp/robots/panda.hh
RUN pip install . -v

RUN python3 -c "from skrobot.models.panda import Panda; Panda()"   # to download the panda model
RUN python3 -c "from skrobot.models.fetch import Fetch; Fetch()"   # to download the fetch model

WORKDIR /workspace
RUN git clone https://github.com/HiroIshida/bench_plainmp_and_vamp.git
RUN pip install matplotlib

WORKDIR /workspace/bench_plainmp_and_vamp

RUN chmod +x /workspace/bench_plainmp_and_vamp/run_bench.sh
ENV VAMP_RESOLUTION=${VAMP_RESOLUTION}
CMD /workspace/bench_plainmp_and_vamp/run_bench.sh "$VAMP_RESOLUTION"
