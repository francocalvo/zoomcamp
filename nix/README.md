# Nix, NixOS and reproducible development

The idea of this repo is to make the project _durable_, as to be a reference on
how to develop a complete Data Engineering project. For this, we will use Nix.

## Hurdles

The tasks we need to accomplish are:

- Create a VM with a bare NixOS deployed via Terraform. This allows idempotent
  deployments and easy rollback at the infra level.
- Provision the VM with the necessary packages and services to run the project.
  This is done via `deploy-rs` and Nix.
- Create OCI images for the project, keeping versioning and reproducibility in
  mind. Also, I might need to create more than one, so labels are important.

## GCE Image

For this step, first we look at the `create-gce.sh` script in _nixpkgs_. Taking
as reference
[this post](https://discourse.nixos.org/t/nixos-rebuild-on-gce-vm/12301) in the
NixOS Discourse forum, I'm able to create a GCE image with the following
command:

```bash
nix build --no-link  ".#nixosConfigurations.vm.config.system.build.googleComputeImage" -o gce
```

Keep in mind that while it's possible to create a provisioned image, I'd like
more control over the provisioning process. This is why I'm using Terraform to
deploy the VM and then provision it with `deploy-rs`.

This way, I can rollback the configuration using profiles without the need to
recreate, reupload and reregister the image.


