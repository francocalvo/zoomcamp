docker container prune -f
docker image prune -f
nix build .#zc-images-m1
docker load < result
