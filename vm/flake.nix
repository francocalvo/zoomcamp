{
  description = "Basic GCE Image";

  inputs = { nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.05"; };

  outputs = { self, nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in {

      nixosConfigurations.vm = nixpkgs.lib.nixosSystem {
        inherit system;
        modules = [ ./configuration.nix ];
      };

      devShell.${system} = pkgs.mkShell {
        nativeBuildInputs = with pkgs; [ jq terraform google-cloud-sdk ];

        PROJECT_ID = "zc-gcp-2024";
      };
    };
}
