{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    deploy-rs = {
      url = "github:serokell/deploy-rs";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, poetry2nix, deploy-rs, ... }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs {
        inherit system;
        config.allowUnfree = true; # Propietary software
      };
      python = pkgs.python311;

      # Create app definition using poetry2nix
      inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; })
        mkPoetryApplication;

      app = mkPoetryApplication {
        inherit python;
        preferWheels = true;
        projectDir = self;
      };
    in {

      deploy.nodes = {
        vm =
          import ./nix/provisioning { inherit nixpkgs pkgs deploy-rs system; };
      };

      packages.${system} = {
        default = app;
        zc-images-m1 =
          import ./nix/docker/loader.nix { inherit pkgs app system; };
      };

      devShells.${system} = {
        default = import ./nix/shell.nix { inherit pkgs python; };
      };

      checks = builtins.mapAttrs
        (system: deployLib: deployLib.deployChecks self.deploy) deploy-rs.lib;
    };
}
