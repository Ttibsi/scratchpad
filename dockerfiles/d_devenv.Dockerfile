# This must be run from the root directory of this repo

# docker build -f dockerfiles/d_devenv.Dockerfile -t d_devenv .
# If running this, you'll have to add the new publickey to your github account
# THe keys are built into the image, so you won't need a new key for each 
# image you create

# docker run --rm -ti d_devenv

FROM fedora:41

RUN dnf update -y && dnf install \
file \
gdb \
gcc-gdc \
gettext \
git \
glibc-gconv-extra \
neovim \
openssh-server \
python3-pip \
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

RUN pip install pre-commit

RUN mkdir -p .config/nvim workspace
RUN git clone --depth=1 https://github.com/savq/paq-nvim.git \
    /home/admin/.local/share/nvim/site/pack/paqs/start/paq-nvim

COPY lua/devenv_nvim_config.lua .config/nvim/init.lua
WORKDIR workspace
