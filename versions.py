#!/usr/bin/env python
import sys, os, json, requests
from dateutil import parser
from datetime import timedelta
import datetime
from colorama import *
import argparse
import yaml

login_template = "https://auth.docker.io/token?service=registry.docker.io&scope=repository:{repository}:pull"
get_manifest_template = "https://registry.hub.docker.com/v2/{repository}/manifests/{tag}"
get_tags_template = "https://registry.hub.docker.com/v2/repositories/{repository}/tags/?page=1&page_size=250"

def pretty_print(d):
    print(json.dumps(d, indent=2))

def get_auth_token(repo):
    response = requests.get(login_template.format(repository=repo), json=True)
    response_json = response.json()
    return response_json["token"]

def download_manifest_for_repo(repo, tag, token):
    """
    repo: string, repository (e.g. 'library/fedora')
    tag:  string, tag of the repository (e.g. 'latest')
    """
    response = requests.get(
        get_manifest_template.format(repository=repo, tag=tag),
        headers={"Authorization": "Bearer {}".format(token)},
        json=True
    )
    manifest = response.json()
    if not response.status_code == requests.codes.ok:
        pretty_print(dict(response.headers))
    return manifest

def download_tags_for_repository(repo):
    response = requests.get(
        get_tags_template.format(repository=repo),
        json=True
    )
    tags = response.json()
    #if not response.status_code == requests.codes.ok:
    #    pretty_print(dict(response.headers))
    return tags

def dump_details_for_tag(repo, version, exclude):
    global config
    try:
        s = download_tags_for_repository(repo)["results"]
    except :
        # print("no repo found for {} ").format(repo)
        return

    # filter out any provided exclusions, such as 'latest', 'alpine'
    if repo in config:
        str = [ x for x in s if x['name'] not in config[repo]['exclude'] ]
    else:
        str = s

    # step through array and return index of requested version
    i = next(index for (index, d) in enumerate(str) if d["name"] == version)

    installed_date = datetime.date.today() - parser.parse(str[i]["last_updated"]).date()
    latest_date = datetime.date.today() - parser.parse(str[0]["last_updated"]).date()


    # highlight if installed version is older than "latest"
    # TODO: really should check image sha for version difference too
    display = "{:<30}\t Latest: {:>15}, {:>3} days old\tRunning: {:>15}, {:>3} days old".format(repo, str[0]["name"], latest_date.days, version, installed_date.days)

    if installed_date.days > latest_date.days:
        print(Fore.RED + Style.BRIGHT + display)
    else:
        print(Fore.WHITE + Style.NORMAL + display)


def main():
    global config
    config = ""

    searchpaths = [ os.environ['HOME'] + '/.container-versions.yaml' , os.path.dirname(os.path.realpath(__file__)) + '/config.yaml']
    for path in searchpaths:
        if os.path.isfile(path):
            with open(path, 'r') as ymlfile:
                config = yaml.load(ymlfile)
                break

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', dest='verbose', action='store_true')
    # TODO: is there a better way of handling single "version" versions?
    parser.add_argument('-x', '--exclude',
        action='append',
        default=['latest', 'dev', 'canary', 'alpine', 'master'],
        help='exclude tag from repository check')
    parser.add_argument('repos', nargs='+', help="[namespace/]repository[:tag]")
    args = parser.parse_args()

    init()
    for repo_tag in args.repos:
        if ":" in repo_tag:
            repo, tag = repo_tag.split(":")
        else:
            repo, tag = repo_tag, "latest"
        if "/" not in repo:
            repo = "library/" + repo
        token = get_auth_token(repo)
        dump_details_for_tag(repo, tag, args.exclude)
    return 0


if __name__ == "__main__":
    main()
