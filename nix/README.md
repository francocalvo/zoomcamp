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

### Image registration

The current way I got to register the image is a extract from the script in
nixpkgs:

```bash
#!/usr/bin/env nix-shell
#! nix-shell -i bash -p google-cloud-sdk

set -euo pipefail

BUCKET_NAME="${BUCKET_NAME:-nixos-cloud-images}"
TIMESTAMP="$(date +%Y%m%d%H%M)"
export TIMESTAMP

img_path=$(echo gce/*.tar.gz)
img_name=${IMAGE_NAME:-$(basename "$img_path")}
img_id=$(echo "$img_name" | sed 's|.raw.tar.gz$||;s|\.|-|g;s|_|-|g')
img_family=$(echo "$img_id" | cut -d - -f1-4)

if ! gsutil ls "gs://${BUCKET_NAME}/$img_name"; then
  gsutil cp "$img_path" "gs://${BUCKET_NAME}/$img_name"
  gsutil acl ch -u AllUsers:R "gs://${BUCKET_NAME}/$img_name"

  gcloud compute images create \
    "$img_id" \
    --source-uri "gs://${BUCKET_NAME}/$img_name" \
    --family="$img_family"

  gcloud compute images add-iam-policy-binding \
    "$img_id" \
    --member='allAuthenticatedUsers' \
    --role='roles/compute.imageUser'
fi
```

There are sometimes problems where even tho the configuration that creates the
image changes, the image hash doesn't. My quick and dirt solution is to delete
files from the bucket and de-register manually.
