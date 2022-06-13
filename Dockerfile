FROM ubuntu:20.04

# Install stegseek
RUN apt update
RUN apt install wget -y

RUN apt install python3 python3-pip curl -y

# Install poetry 
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -

# Install support libraries for python-ldap dependency of secrets
RUN apt-get install python-dev libldap2-dev libsasl2-dev libssl-dev -y  

COPY main.py /hash_mechanism/main.py
COPY verification_hash.py /hash_mechanism/verification_hash.py
COPY poetry.lock /hash_mechanism/poetry.lock
COPY pyproject.toml /hash_mechanism/pyproject.toml

WORKDIR /hash_mechanism

RUN mkdir image

RUN /bin/bash -c "source $HOME/.poetry/env  && poetry install" 

RUN echo "source $HOME/.poetry/env" >> .bashrc
RUN echo "poetry shell" >> .bashrc
RUN echo "pip install pyOpenSSL" >> .bashrc
RUN echo "poetry add secrets" >> .bashrc

ENTRYPOINT bash .bashrc
