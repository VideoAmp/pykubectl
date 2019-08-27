#!/usr/bin/env python

from colorama import Fore, Style

import argparse
import boto3
import kubernetes
import logging
import os


def do_parse_args():
    parser = argparse.ArgumentParser(
        description='Check EKS clusters for role-based access.')

    parser.add_argument(
        '-g', '--git_repo_path',
        default='/Users/michael/src/git/videoamp/k8s-cluster-configs',
        help='Path to local root of k8s-cluster-configs repo')

    parser.add_argument(
        '-v', '--verbose',
        default=False,
        help='Enable verbose logging')

    parser.add_argument(
        '-p', '--profile',
        default='avenger',
        help='Profile to assume when accessing clusters')

    parser.add_argument(
        '-r', '--role',
        default='arn:aws:iam::914375995788:role/TheAvengers',
        help='ARN of the role to check for')

    return parser.parse_args()


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
    """ Does role/TheAvenger appear in the mapRoles section of aws-auth? """
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
                if args.role in mapRoles:
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
    args = do_parse_args()
    os.environ['AWS_PROFILE'] = args.profile
    os.chdir(args.git_repo_path)
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        # kubernetes calls to api endpoint gives verbose ERROR, squelch here
        logging.basicConfig(level=logging.CRITICAL)
    main()
