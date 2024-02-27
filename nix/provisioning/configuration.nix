{ lib, pkgs, modulesPath, ... }:

{
  imports = [ (modulesPath + "/virtualisation/google-compute-image.nix") ];

  system.stateVersion = "23.05";
  services.openssh = {
    enable = true;
    settings = {
      PasswordAuthentication = lib.mkForce false;
      PermitRootLogin = lib.mkForce "no";
    };
    allowSFTP = false;
  };

  nix.settings.trusted-users = [ "calvo" "admin" ];
  environment.systemPackages = with pkgs; [
    vim
    git
    neovim
    arion
    docker-client
  ];

  virtualisation = {
    docker = {
      enable = true;
      autoPrune.enable = true;
    };

    oci-containers = {
      backend = "docker";
      containers = {
        postgres = {
          image = "postgres:15";
          autoStart = true;
          volumes = [ "/db:/var/lib/postgresql/data" ];
          ports = [ "5432:5432" ];
          environment = {
            POSTGES_USER = "postgres";
            POSTGRES_PASSWORD = "postgres";
            POSTGRES_DB = "ny_taxi";
          };
        };
      };
    };
  };

}
