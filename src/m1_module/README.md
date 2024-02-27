# Module 1: Docker and Terraform basics

## Videos:

### Section 1: Docker

- [1.2.1: Introduction to Docker](https://www.youtube.com/watch?v=EYNwNlOrpr0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)
- [1.2.2: Ingesting NY TAxi Data to Postgres](https://www.youtube.com/watch?v=2JM-ziJt0WI&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=6)
- [1.2.3: Connecting pgAdmin and Postgres](https://www.youtube.com/watch?v=hCAIVe9N0ow&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=8)
- [1.2.4: Dockerizing the Ingestion Script](https://www.youtube.com/watch?v=B1WwATwf-vY&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=8)
- Skipped both 1.2.5 and 1.2.6.

## Notes

### Docker & Nix Flake

- We use Docker as it allows to have reproducibility, local development,
  integration tests, between other things.
- For the docker-compose I needed to create a network to allow both connecting
  from my host and to be able to connect between the containers based on their
  names in the file.
- Creating the image using Nix was... Tough. I did it tho. Use the `dockerTools`
  library and read the examples. Many things failed at first, mainly because of
  the base image and how to install the app.
- Using `poetry2nix` makes creating the environment and more easy, once you read
  the docs. It also helps me verify that the app that's being built is the same
  one that's in the container.
- `LD_LIBRARY_PATH`... Oh God. It's used to map the linked libraries from C to
  be used in Python. Even tho I'm using Polars, the writing to a database
  directly from the dataframe requires Pandas. I'm using `manylinux` as was
  recommended in the NixOS Matrix room.
- This _works_ in 23.05. If I update I start getting a mismatch between GLIB
  needed and available, so I'll have to make do. I think I didn't come across
  this problem now because I'm not using Numpy/Pandas directly?

### Google Cloud

- I'm creating a GCE Image using the flake found in `nixpkgs`. I can build it
  using
  ````
  nix build --no-link ".#nixosConfigurations.vm.config.system.build.googleComputeImage" -o gce ```
  ````
- I'm deploying the configuration using `deploy-rs`, using as base nixosSystem
  from nixpkgs for GCE images (same as the flake for the build).
- I'm deploying the OCI-Image using the native module from NixOS.
- The command to forward ports is
  `ssh -L 5432:localhost:5432 REMOTE_USER@REMOTE_IP`
- There is more information in
  [Nix, NixOS and reproducibility](../../nix/README.md), but in conclusion, I
  get the full system using Nix and deploying with two commands
  (terraform+deploy). I can connect to Postgres using pgcli, and the same with
  the ingestion script.
