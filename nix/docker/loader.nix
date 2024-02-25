{ pkgs, app, system ? "x86_64-linux", ... }:

pkgs.dockerTools.buildImage {
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

  config = {
    # Entrypoint = [ "${pkgs.bash}/bin/bash" ];
    Entrypoint = [ "m1_module" "--type=postgres" ];
  };
}
