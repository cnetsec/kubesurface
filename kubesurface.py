import requests
import re

# Função para verificar o provedor de nuvem
def verificar_provedor_nuvem(url):
    if re.match(r"(http|https)://[a-zA-Z0-9.-]+.eks.amazonaws.com", url):
        return "AWS EKS"
    elif re.match(r"(http|https)://[a-zA-Z0-9.-]+.azurecontainer.io", url):
        return "Azure AKS"
    elif re.match(r"(http|https)://[a-zA-Z0-9.-]+.container.googleapis.com", url):
        return "GCP GKE"
    else:
        return "Kubernetes Cluster Próprio"

# Função para verificar se é um endpoint EKS API público
def verificar_endpoint_eks_publico(url):
    if re.match(r"(http|https)://[a-zA-Z0-9.-]+.eks.amazonaws.com", url):
        return True
    else:
        return False

# Função de enumeração de endpoints
def enumerar_endpoints(api_url, cloud_provider):
    print("KubeSurface results:")
    print(f"Cenário: {cloud_provider}")
    print("Enumeração dos Endpoints:")

    endpoints = [
        ("/api/v1/namespaces/default/pods", "Endpoint de Pods"),
        ("/api/v1/namespaces/default/secrets", "Endpoint de Secrets"),
        ("/apis/extensions/v1beta1/namespaces/default/deployments", "Endpoint de Deployments"),
        ("/apis/extensions/v1beta1/namespaces/default/daemonsets", "Endpoint de DaemonSets")
    ]

    for endpoint, descricao in endpoints:
        url = f"{api_url}{endpoint}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f" - {descricao}: Acessível")
            else:
                print(f" - {descricao}: Não acessível")
        except requests.exceptions.RequestException:
            print(f" - {descricao}: Não foi possível conectar")

# Função de enumeração do cluster
def enumerar_cluster(master_url, cloud_provider):
    print(f"\nKubeSurface results:")
    print(f"Cenário: {cloud_provider}")
    print("Enumeração do Cluster Kubernetes:")
    ports = [
        ("80", "HTTP"),
        ("443", "HTTPS"),
        ("8080", "Custom Port 8080"),
        ("9090", "Custom Port 9090"),
        ("9100", "Custom Port 9100"),
        ("9093", "Custom Port 9093"),
        ("4001", "Custom Port 4001"),
        ("6782-6784", "Custom Ports 6782-6784"),
        ("6443", "Kubernetes API Server"),
        ("8443", "Custom Port 8443"),
        ("9099", "Custom Port 9099"),
        ("10250", "Kubelet API"),
        ("10255", "Kubelet Read-Only API"),
        ("2379-2380", "etcd Server Client API")
    ]

    print("Portas abertas:")

    for port, descricao in ports:
        url = f"http://{master_url}:{port}/"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f" - {port} ({descricao}): Aberta")
            else:
                print(f" - {port} ({descricao}): Fechada")
        except requests.exceptions.RequestException:
            print(f" - {port} ({descricao}): Não foi possível conectar")

# Captura do input do usuário
url = input("Digite o endereço do cluster ou do endpoint da API: ")

# Verificação do tipo de URL inserida
cloud_provider = verificar_provedor_nuvem(url)

if verificar_endpoint_eks_publico(url):
    print("\nKubeSurface results:")
    print("Endpoint EKS API identificado. Este endpoint é público e não deve ser exposto diretamente.")
else:
    enumerar_endpoints(url, cloud_provider)
    enumerar_cluster(url, cloud_provider)
