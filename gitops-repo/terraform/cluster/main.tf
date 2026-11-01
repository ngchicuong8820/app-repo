terraform {
  required_providers {
    kind = {
      source  = "tehcyx/kind"
      version = "~> 0.4.0"
    }
  }
}

provider "kind" {}

resource "kind_cluster" "lab1_cluster" {
  name           = "lab1-cluster"
  wait_for_ready = true

  kind_config {
    kind        = "Cluster"
    api_version = "kind.x-k8s.io/v1alpha4"

    # Node 1: Control Plane (Đảm nhiệm Ingress)
    node {
      role = "control-plane"
      
      kubeadm_config_patches = [
        "kind: InitConfiguration\nnodeRegistration:\n  kubeletExtraArgs:\n    node-labels: \"ingress-ready=true\"\n"
      ]

      extra_port_mappings {
        container_port = 80
        host_port      = 80
        protocol       = "TCP"
      }
      extra_port_mappings {
        container_port = 443
        host_port      = 443
        protocol       = "TCP"
      }
    }

    # Node 2: Worker Node 1
    node {
      role = "worker"
    }

    # Node 3: Worker Node 2
    node {
      role = "worker"
    }
  }
}