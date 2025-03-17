# Use Miniconda-based image
FROM continuumio/miniconda3


ENV PATH="/opt/venv/bin:$PATH"

WORKDIR .

COPY requirements.txt .
# Create and activate a Conda environment, installing dependencies from Conda Forge
RUN conda create -n geo_env -c conda-forge python=3.11 geopandas pyogrio shapely \
    && conda install -n geo_env -c conda-forge --file requirements.txt

# Activate the environment for all shell commands
SHELL ["conda", "run", "-n", "geo_env", "/bin/bash", "-c"]

# Set entrypoint to ensure Conda environment is used
ENTRYPOINT ["conda", "run", "-n", "geo_env"]

RUN mkdir code
RUN cd code

EXPOSE 5500
