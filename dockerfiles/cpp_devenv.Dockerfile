# This must be run from the root directory of this repo

# docker build -f dockerfiles/cpp_devenv.Dockerfile -t devenv .
# If running this, you'll have to add the new publickey to your github account
# THe keys are built into the image, so you won't need a new key for each 
# image you create

# docker run --rm -ti devenv

FROM fedora:40

#RUN apt-get update && apt-get upgrade -y && \
#apt-get install --no-install-recommends \
RUN dnf update -y && dnf install \
clang \
clang-tools-extra \
cmake \
gettext \
git \
glibc-gconv-extra \
make \
ninja-build \
openssh-server \
python3-pip \
unzip \
-y

RUN ssh-keygen -b 2048 -t rsa -f /root/.ssh/id_rsa -q -N ""
RUN eval "$(ssh-agent -s)" &&  ssh-add /root/.ssh/id_rsa

# break-system-packages because of running `pip` at root
RUN pip install cmake-language-server --break-system-packages 

RUN git clone --depth=1 --branch=v0.10.2 https://github.com/neovim/neovim
RUN cd neovim && \
make CMAKE_BUILD_TYPE=RelWithDebInfo && \
make install

RUN rm -rf neovim
RUN mkdir -p /root/.config/nvim workspace /root/.ssh
RUN git clone --depth=1 https://github.com/savq/paq-nvim.git \
    "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/pack/paqs/start/paq-nvim

COPY lua/devenv_nvim_config.lua /root/.config/nvim/init.lua
RUN nvim --headless -c 'PaqInstall' +q

WORKDIR /workspace
