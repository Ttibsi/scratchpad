# This must be run from the root directory of this repo

# docker build -f dockerfiles/cpp_devenv.Dockerfile -t devenv .
# If running this, you'll have to add the new publickey to your github account
# THe keys are built into the image, so you won't need a new key for each 
# image you create

# docker run --rm -ti devenv

FROM fedora:41

RUN dnf update -y && dnf install \
clang \
clang-tools-extra \
cmake \
file \
gdb \
gettext \
git \
glibc-gconv-extra \
make \
neovim \
ninja-build \
openssh-server \
python3-pip \
tmux \
unzip \
-y

RUN useradd -ms /bin/bash admin
RUN echo "admin:admin" | chpasswd
RUN usermod -aG wheel admin
USER admin
WORKDIR /home/admin

RUN mkdir .ssh
RUN ssh-keygen -b 2048 -t rsa -f /home/admin/.ssh/id_rsa -q -N ""
RUN eval "$(ssh-agent -s)" &&  ssh-add /home/admin/.ssh/id_rsa

RUN pip install cmake-language-server pre-commit

RUN mkdir -p .config/nvim workspace
RUN git clone --depth=1 https://github.com/savq/paq-nvim.git \
    /home/admin/.local/share/nvim/site/pack/paqs/start/paq-nvim

COPY lua/devenv_nvim_config.lua .config/nvim/init.lua
# Better off running this manually on first entry, i find
# RUN nvim --headless -c 'PaqInstall' +q

WORKDIR workspace
