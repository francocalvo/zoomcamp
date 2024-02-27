{ nixpkgs, pkgs, deploy-rs, system ? "x86_64-linux" }:

let
  deployPkgs = import nixpkgs {
    inherit system;
    overlays = [
      deploy-rs.overlay
      (self: super: {
        deploy-rs = {
          inherit (pkgs) deploy-rs;
          lib = super.deploy-rs.lib;
        };
      })
    ];
  };

  # Define the NixOS configuration
  nixosConfiguration = nixpkgs.lib.nixosSystem {
    inherit system;
    modules = [ ./configuration.nix ]; # Adjust path as needed
  };

in {
  hostname = "35.208.188.66";
  remoteBuild = true;
  profiles.system = {
    user = "root";
    sshUser = "calvo";
    path = deployPkgs.deploy-rs.lib.activate.nixos nixosConfiguration;
  };
}
