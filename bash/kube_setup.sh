sudo apt-get update
sudo apt-get install -y kubectl
kubectl version --client

curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash

k3d cluster create -a 2 --no-lb
kubectl config use-context k3d-k3s-default

kubectl cluster-info