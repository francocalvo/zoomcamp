# `zoomcamp`

Zoomcamp repo for cohort 2024. Notes are taken by module.

**Main course repo:**
[link](https://github.com/DataTalksClub/data-engineering-zoomcamp)

## Comments

The `flake.nix` and `flake.lock` should encompass all dependencies for this
project to work. It ensures I have complete reproducibility of the project. It
might present a steeper learning curve, but well worth it in my opinion.

System configuration is not in the scope for this flake, so things like
virtualization, permissions, editing tools and more are not handled here.

## Modules

- [Module 1: Intro to Docker and Terraform](./src/m1_module/README.md)

## VM Connection

Use the following command:

```
gcloud compute ssh --zone "southamerica-west1-b" "zc--base-vm" --project "zc-gcp-2024"
```

Also, in the first boot, run this from [#3962](https://github.com/alacritty/alacritty/issues/3962) to improve terminal
compatibility.

```
curl -sSL https://raw.githubusercontent.com/alacritty/alacritty/master/extra/alacritty.info | tic -x -
```
