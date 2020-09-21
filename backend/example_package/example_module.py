from tamr_unify_client.client import Client
from typing import List


def get_all_project_names(client: Client) -> List[str]:
    """
    Get all project names.

    Args:
        client: A  Tamr Client object

    Returns:
        List of project names as strings
    """
    return [x.name for x in client.projects]


def get_all_dataset_names(client: Client) -> List[str]:
    """
    Get all dataset names.

    Args:
        client: A Tamr Client object

    Returns:
        List of dataset names as strings

    """
    return [x.name for x in client.datasets]