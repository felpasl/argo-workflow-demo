# install
## install argo workflows:

https://github.com/argoproj/argo-helm/tree/main/charts/argo-workflows

```bash
helm repo add argo https://argoproj.github.io/argo-helm

helm repo update

helm upgrade -n argo argo-workflows argo/argo-workflows -f values.yaml --install --create-namespace
```

## install argo cli

https://github.com/argoproj/argo-workflows/releases

```bash
# Download the binary
curl -sLO https://github.com/argoproj/argo-workflows/releases/download/v3.4.10/argo-darwin-amd64.gz

# Unzip
gunzip argo-darwin-amd64.gz

# Make binary executable
chmod +x argo-darwin-amd64

# Move binary to path
sudo mv ./argo-darwin-amd64 /usr/local/bin/argo

# Test installation
argo version
```
# Walk Through
https://argoproj.github.io/argo-workflows/quick-start/

# Yaml Field Reference:
https://argoproj.github.io/argo-workflows/fields/

# samples
./workflows

# database manipulation
./workflows-postgresql-python