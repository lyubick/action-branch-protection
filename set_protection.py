import json
import logging
import sys

import requests

PROTECTION_URL = "https://api.github.com/repos/{repository}/branches/{branch}/protection"


def get_auth_headers(access_token: str):
    return {
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'Authorization': f'Bearer {access_token}'
    }


def set_branch_lock(
        access_token: str,
        repository_name: str,
        branch_name: str,
        lock: bool
):
    """
    This is the function to set the 'lock branch' protection rule on a given GitHub repository branch.

    :param access_token: The token to authorize the GitHub API request.
    :param repository_name: The name of the repository in format of 'username/repo'.
    :param branch_name: The name of the branch in the repository where the protection rules needs to be set.
    :param lock: A boolean value to represent whether the protection needs to be enabled (True) or disabled (False).
    :returns: It returns the HTTP status code of the PUT request to update the protection rules.
    """

    headers = get_auth_headers(access_token=access_token)

    # Perform GET requests towards branches/*/protection endpoint
    response = requests.get(
        url=PROTECTION_URL.format(repository=repository_name, branch=branch_name),
        headers=headers
    )

    # Get response - protection settings or error message
    protection_rules = response.json()

    if response.status_code != 200:
        logging.error(f'GET request returned status code: {response.status_code}, with message: {protection_rules}')
        return response.status_code

    # Convert GET response JSON into PUT expected JSON
    for key in protection_rules:
        if 'enabled' in protection_rules[key]:
            protection_rules[key] = protection_rules[key]['enabled']

    if 'restrictions' not in protection_rules:
        protection_rules['restrictions'] = None

    if 'required_status_checks' not in protection_rules:
        protection_rules['required_status_checks'] = None
    elif 'contexts' in protection_rules['required_status_checks']:
        # Remove obsolete setting returned by GET request
        protection_rules['required_status_checks'].pop('contexts', None)

    # Alter `lock branch` setting in branch protection rules
    protection_rules['lock_branch'] = lock

    # Perform POST request towards branches/*/protection endpoint
    response = requests.put(
        url=PROTECTION_URL.format(repository=repository_name, branch=branch_name),
        headers=headers,
        data=json.dumps(protection_rules)
    )

    if response.status_code != 200:
        logging.error(f'PUT request returned status code: {response.status_code}, with message: {response.json()}')

    return response.status_code


if __name__ == '__main__':
    args = sys.argv[1:]

    rc = set_branch_lock(
        access_token=args[0],
        repository_name=args[1],
        branch_name=args[2],
        lock=args[3].lower() == 'true'
    )

    exit(rc) if rc != 200 else exit(0)
