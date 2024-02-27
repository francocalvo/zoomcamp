{ config, lib, pkgs, modulesPath, ... }:

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
  environment.systemPackages = with pkgs; [ vim git neovim hello ];
  virtualisation.docker = {
    enable = true;
    enableOnBoot = true;
    autoPrune.enable = true;
  };
}
