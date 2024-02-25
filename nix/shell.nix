{ pkgs, python }:

pkgs.mkShell {
  buildInputs = [ pkgs.deploy-rs ];
  nativeBuildInputs = [ python ] ++ (with python.pkgs; [
    # Python dependencies
    black
    pip
    pytest
    pytest-cov
  ]) ++ (with pkgs; [
    # Dev dependencies
    engage
    nixpkgs-fmt
    poetry
    ruff
    docker
    cargo
    wget
    pgcli

    # Zoomcamp dependencies
    libpqxx
    postgresql
    terraform
    docker
    google-cloud-sdk
  ]) ++ (with pkgs.nodePackages;
    [ # NodeJS dependencies
      markdownlint-cli
    ]);

  NIX_PYTHON_SITE_PACKAGES = python.sitePackages;

  # Variables for GCE Image build
  PROJECT_ID = "zc-gcp-2024";
  BUCKET_NAME = "zc-nixos-images";

  shellHook = ''
    export LD_LIBRARY_PATH="${
      pkgs.lib.makeLibraryPath [ pkgs.zlib ]
    }:$LD_LIBRARY_PATH"

    export LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH"
  '';
}
