#!/usr/bin/env python

from colorama import Fore, Style

import boto3
import kubernetes
import logging
import os


def find_avenger_role(cluster):
    AOK = Fore.GREEN + '✓' + Style.RESET_ALL
    NOK = Fore.RED + '✗' + Style.RESET_ALL
    UNK = Fore.YELLOW + '✗ (no config found)' + Style.RESET_ALL

    ROLE = "arn:aws:iam::914375995788:role/TheAvengers"

    status = NOK
    kubeconfig = os.path.join(
        os.environ['HOME'],
        'src/git/videoamp/k8s-cluster-configs',
        f'prod-use1/{cluster}/config')
    try:
        kubernetes.config.load_kube_config(config_file=kubeconfig)
        api_instance = kubernetes.client.CoreV1Api()
        try:
            api_response = api_instance.list_config_map_for_all_namespaces(
                field_selector='metadata.name=aws-auth')
            if api_response and len(api_response.items) > 0:
                mapRoles = api_response.items[0].data['mapRoles']
                if ROLE in mapRoles:
                    status = AOK
        except Exception as e:
            logging.error(e)    # some other error
    except Exception:
        status = UNK    # config not found
    print(f'{cluster:20} {status}')


def main():
    """ Loop through all EKS clusters reported by AWS via Boto """
    boto = boto3.client('eks', region_name='us-east-1')
    clusters = boto.list_clusters()['clusters']

    # transform cluster names that are different than their git repo path
    cluster_transforms = {
        'eks-cicd': 'cicd',
        'eks-cicd-test': 'cicd-test',
    }

    for cluster in clusters:
        if cluster in cluster_transforms:
            find_avenger_role(cluster_transforms[cluster])
        else:
            find_avenger_role(cluster)


if __name__ == "__main__":
    os.environ['AWS_PROFILE'] = 'avenger'
    logging.disable()
    main()
