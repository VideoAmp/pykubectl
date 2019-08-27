#!/usr/bin/env python

from colorama import Fore, Style

import boto3
import kubernetes
import logging
import os


def transform_cluster_name(cluster):
    """ Transform EKS name to match name as exists in Git path """
    remapped_cluster_names = {
        'eks-cicd': 'cicd',
        'eks-cicd-test': 'cicd-test',
    }
    if cluster in remapped_cluster_names:
        return remapped_cluster_names[cluster]
    else:
        return cluster


def find_avenger_role(cluster):
    AOK = f'{Fore.GREEN}✓{Style.RESET_ALL}'
    NOK = f'{Fore.RED}✗{Style.RESET_ALL}'
    UNK = f'{Fore.YELLOW}?{Style.RESET_ALL}'

    cluster = transform_cluster_name(cluster)
    status = NOK

    kubeconfig = os.path.join(os.getcwd(), 'prod-use1', cluster, 'config')
    logging.debug(kubeconfig)
    try:
        kubernetes.config.load_kube_config(config_file=kubeconfig)
        k8s_client = kubernetes.client.CoreV1Api()
        try:
            aws_auth = k8s_client.list_config_map_for_all_namespaces(
                field_selector='metadata.name=aws-auth')
            if aws_auth and len(aws_auth.items) > 0:
                mapRoles = aws_auth.items[0].data['mapRoles']
                if "arn:aws:iam::914375995788:role/TheAvengers" in mapRoles:
                    status = AOK
        except Exception as e:
            logging.error(e)
    except Exception:
        status = UNK
    print(f'{cluster:20} {status}')


def main():
    """ Loop through all EKS clusters reported by AWS via Boto """
    boto = boto3.client('eks', region_name='us-east-1')
    for cluster in boto.list_clusters()['clusters']:
        find_avenger_role(cluster)


if __name__ == "__main__":
    os.environ['AWS_PROFILE'] = 'avenger'
    os.chdir('/Users/michael/src/git/videoamp/k8s-cluster-configs')
    logging.basicConfig(level=logging.CRITICAL)
    main()
