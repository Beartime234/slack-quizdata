import yaml


def load_file(file_path) -> str:
    """Loads a file from a path.

    Args:
        file_path: The full file path

    Returns:
        A string of the files contents
    """
    with open(file_path, 'r') as f:
        file_contents = f.read()
    return file_contents


def load_local_yaml(file_path) -> dict:
    """Loads a yaml file from a full file path

    Args:
        file_path: The full file path

    Returns:
        A dictionary of the files contents
    """
    return yaml.safe_load(load_file(file_path))


def save_local_yaml(file_path, data) -> dict:
    """Saves a yaml file

    Args:
        data: The data you wish to save
        file_path: The full file path

    Returns:
        A dictionary of the files contents
    """
    with open(file_path, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)
