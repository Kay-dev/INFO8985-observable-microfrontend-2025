# cdevops-signoz
## to add signoz to a project

TLDR;

```bash
ansible-playbook up.yaml
```

You may need some pre-requisites

1. Make sure that docker is running by doing `docker ps` until it shows 

```
CONTAINER ID   IMAGE                            COMMAND                  CREATED         STATUS         PORTS                             NAMES

```

2. run `ansible-playbook --version` to see if you have ansible. If not run:

```bash
bash <(curl -Ls https://raw.githubusercontent.com/conestogac-acsit/cdevops-bootstrap/refs/heads/main/bootstrap.sh)
```

3. run `kubectl get ns default` to see if you have a cluster. The expected result is:

```
NAME      STATUS   AGE
default   Active   29m
```

If you have another result try installing a k8s cluster:

```bash
bash <(curl -Ls https://raw.githubusercontent.com//conestogac-acsit/cdevops-bootstrap/refs/heads/main/k8s.sh)
```

or to restart a k3d cluster in a codespace:

```bash
k3d cluster delete k3d-cluster
k3d cluster create k3d-cluster --k3s-arg "--disable=traefik@server:0"
```

When you are happy that signoz is running run:

```bash
nohup kubectl port-forward svc/my-signoz 8080:8080  2>&1 &
nohup kubectl port-forward svc/my-signoz-otel-collector 4317:4317  2>&1 &
```

Then your unit under test should be able to use the otel collector at localhost:4317
