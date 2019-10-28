from pathlib import Path


def get_base_dir():
    """Returns base (root) directory of project
    """
    return Path(__file__).parent.parent.parent.parent
