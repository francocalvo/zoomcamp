{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs?ref=nixos-23.05";

    # flake-utils
    systems.url = "github:nix-systems/x86_64-linux";
    flake-utils.url = "github:numtide/flake-utils";
    flake-utils.inputs.systems.follows = "systems";

    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
      inputs.flake-utils.follows = "flake-utils";
    };
  };

  outputs = { self, nixpkgs, systems, flake-utils, poetry2nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true; # Propietary software
        };
        python = pkgs.python311;
        app = pkgs.poetry2nix.mkPoetryApplication {
          inherit python;
          preferWheels = true;
          projectDir = ./.;
        };
      in {
        packages = let
          zc-images-m1 = pkgs.dockerTools.buildImage {
            name = "zc-images";
            tag = "m1";
            fromImage = pkgs.dockerTools.pullImage {
              imageName = "python";
              imageDigest =
                "sha256:6aa46819a8ff43850e52f5ac59545b50c6d37ebd3430080421582af362afec97";
              finalImageName = "python";
              finalImageTag = "3.11.7-alpine";
              sha256 = "sha256-kg5x67Toe4Y6sDrO1yHa9qOEUw+qz478JaHvm1MRHfM=";
              os = "linux";
              arch = "x86_64";
            };

            copyToRoot = pkgs.buildEnv {
              name = "m1_module";
              paths = [ app ];
            };

            config = { Entrypoint = [ "m1_module" ]; };
          };

        in {
          default = app;
          zc-images-m1 = zc-images-m1;
        };

        devShells.default = pkgs.mkShell {
          nativeBuildInputs = [ python ]
            ++ (with python.pkgs; [ black pip pytest pytest-cov ])
            ++ (with pkgs; [
              engage
              nixpkgs-fmt
              poetry
              pyright
              ruff
              docker
              cargo
            ]) ++ (with pkgs.nodePackages; [ markdownlint-cli ]);

          NIX_PYTHON_SITE_PACKAGES = python.sitePackages;
        };

        checks = {
          packagesDefault = self.packages.${system}.default;
          devShellsDefault = self.devShells.${system}.default;
        };
      });
}
