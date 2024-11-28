# This must be run from the root directory of this repo

# docker build -f dockerfiles/rust_devenv.Dockerfile -t rust_devenv .
# If running this, you'll have to add the new publickey to your github account
# THe keys are built into the image, so you won't need a new key for each 
# image you create

# docker run --name rust_devenv -ti devenv

FROM ubuntu:latest

RUN apt-get update && apt-get upgrade -y && \
apt-get install --no-install-recommends \
build-essential \
cmake \
curl \
file \
gettext \
git \
make \
openssh-server \
software-properties-common \
unzip \
-y \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

RUN ssh-keygen -b 2048 -t rsa -f /root/.ssh/id_rsa -q -N ""
RUN eval "$(ssh-agent -s)" &&  ssh-add /root/.ssh/id_rsa

RUN curl https://sh.rustup.rs -o rustup.sh
RUN bash rustup.sh -y
RUN . /root/.bashrc && rustup component add rust-analyzer
RUN git clone --depth=1 --branch=v0.10.2 https://github.com/neovim/neovim
RUN cd neovim && \
	 make CMAKE_BUILD_TYPE=RelWithDebInfo && \
	 make install
RUN rm -rf neovim
RUN mkdir -p /root/.config/nvim workspace /root/.ssh
RUN git clone --depth=1 https://github.com/savq/paq-nvim.git \
    "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/pack/paqs/start/paq-nvim

COPY lua/devenv_nvim_config.lua /root/.config/nvim/init.lua
# RUN nvim --headless -c 'PaqInstall' +q

WORKDIR /workspace
