{ modulesPath, ... }: {
  imports =
    [ "${toString modulesPath}/virtualisation/google-compute-image.nix" ];

  users.users.root.openssh.authorizedKeys.keyFiles =
    [ (/. + builtins.getEnv ("HOME") + "/.ssh/id_rsa.pub") ];

  system.stateVersion = "23.05";
}
