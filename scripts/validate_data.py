""" Python script to validate data

Run as:

    python3 scripts/validate_data.py
"""

from pathlib import Path
import hashlib


def file_hash(filename):
    """Get byte contents of file `filename`, return SHA1 hash

    Parameters
    ----------
    filename : str
        Name of file to read

    Returns
    -------
    hash : str
        SHA1 hexadecimal hash string for contents of `filename`.
    """
    # make hasher
    hasher = hashlib.sha1()

    # Open the file, read contents as bytes.
    with open(filename, "rb") as f:
        # update the hasher
        hasher.update(f.read())

    # Calculate, return SHA1 has on the bytes from the file.
    return hasher.hexdigest()


def validate_data(data_directory):
    """Read ``data_hashes.txt`` file in `data_directory`, check hashes

    Parameters
    ----------
    data_directory : str
        Directory containing data and ``data_hashes.txt`` file.

    Returns
    -------
    None

    Raises
    ------
    ValueError:
        If hash value for any file is different from hash value recorded in
        ``data_hashes.txt`` file.
    """
    # Read lines from ``data_hashes.txt`` file.
    data_hashes = Path(data_directory) / "hash_list.txt"
    with open(str(data_hashes), "r") as f:
        lines = [l.strip() for l in f.readlines()]

    # Split into SHA1 hash and filename
    for l in lines:
        saved_file_hash, file_path = l.split(" ")
        # Calculate actual hash for given filename.
        computed_file_hash = file_hash(str(Path(data_directory).parent / file_path))
        # If hash for filename is not the same as the one in the file, raise
        # ValueError
        if saved_file_hash != computed_file_hash:
            raise ValueError(f"Hash does not match for {file_path}.")


def main():
    # This function (main) called when this file run as a script.
    group_directory = Path(__file__).parent.parent / "data"
    groups = list(group_directory.glob("group-??"))
    if len(groups) == 0:
        raise RuntimeError("No group directory in data directory: " "have you downloaded and unpacked the data?")

    if len(groups) > 1:
        raise RuntimeError("Too many group directories in data directory")
    # Call function to validate data in data directory
    validate_data(groups[0])


if __name__ == "__main__":
    # Python is running this file as a script, not importing it.
    main()
