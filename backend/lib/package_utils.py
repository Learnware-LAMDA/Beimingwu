from typing import List, Tuple
import subprocess
import yaml
import os
import time


def try_to_run(args, timeout=5, retry=5):
    sucess = False
    for i in range(retry):
        try:
            subprocess.check_call(args=args, timeout=timeout)
            sucess = True
            break
        except subprocess.TimeoutExpired as e:
            pass
        pass

    if not sucess:
        raise subprocess.TimeoutExpired(args, timeout)
    pass


def parse_pip_requirement(line: str):
    """parse pip requirement line to package name"""
    line = line.strip()

    if len(line) == 0:
        return None

    if line[0] in ("#", "-"):
        return None

    package_str = line
    for split_ch in ("=", ">", "<", "!", "~", " "):
        split_ch_index = package_str.find(split_ch)
        if split_ch_index != -1:
            package_str = package_str[:split_ch_index]
            pass
        pass

    return package_str


def read_pip_packages_from_requirements(requirements_file: str) -> List[str]:
    """read requiremnts.txt and parse it to list"""

    packages = []
    lines = []
    with open(requirements_file, "r") as fin:
        for line in fin:
            package_str = parse_pip_requirement(line)
            packages.append(package_str)
            lines.append(line)
            pass

    return packages, lines


def filter_nonexist_pip_packages(packages: list) -> Tuple[List[str], List[str]]:
    """filter non-exist pip requirements

    Returns:
        exist_packages: list of exist packages
        nonexist_packages: list of non-exist packages
    """

    exist_packages = []
    nonexist_packages = []
    for package in packages:
        if package is None:
            continue

        try:
            # os.system("python3 -m pip index versions {0}".format(package))
            print("check package existence: {0}".format(package))
            try_to_run(args=["python3", "-m", "pip", "index", "versions", package], timeout=5)
            exist_packages.append(package)
        except Exception as e:
            print(e)
            nonexist_packages.append(package)
            pass
        pass

    return exist_packages, nonexist_packages


def filter_nonexist_conda_packages(packages: list) -> Tuple[List[str], List[str]]:
    """filter non-exist conda requirements

    Returns:
        exist_packages: list of exist packages
        nonexist_packages: list of non-exist packages
    """

    exist_packages = []
    nonexist_packages = []
    for package in packages:
        try:
            try_to_run(args=["conda", "search", package], timeout=5)
            exist_packages.append(package)
        except Exception as e:
            nonexist_packages.append(package)
            pass
        pass

    return exist_packages, nonexist_packages


def read_conda_packages_from_dict(env_desc: dict) -> Tuple[List[str], List[str]]:
    """

    :param env_desc: dict of environment description

    :return conda packages: list of conda packages
    :return pip packages: list of pip packages
    """

    conda_packages = env_desc.get("dependencies")
    if conda_packages is None:
        conda_packages = []
        pip_packages = []
        pass
    else:
        pip_packages = []
        conda_packages_ = []
        for package in conda_packages:
            if isinstance(package, dict) and "pip" in package:
                pip_packages = package["pip"]
                pip_packages = [parse_pip_requirement(line) for line in pip_packages]
                pass
            elif isinstance(package, str):
                conda_packages_.append(package)
                pass
            pass

        conda_packages = conda_packages_
        pass

    return conda_packages, pip_packages
    pass


def filter_nonexist_conda_packages_file(yaml_file: str, output_yaml_file: str):
    with open(yaml_file, "r") as fin:
        env_desc = yaml.safe_load(fin)
        pass

    conda_packages, pip_packages = read_conda_packages_from_dict(env_desc)

    conda_packages, nonexist_conda_packages = filter_nonexist_conda_packages(conda_packages)
    pip_packages, nonexist_pip_packages = filter_nonexist_pip_packages(pip_packages)

    env_desc["dependencies"] = conda_packages
    if len(pip_packages) > 0:
        env_desc["dependencies"].append({"pip": pip_packages})
        pass

    with open(output_yaml_file, "w") as fout:
        yaml.safe_dump(env_desc, fout)
        pass

    return conda_packages, pip_packages, nonexist_conda_packages, nonexist_pip_packages
    pass


def filter_nonexist_pip_packages_file(requirements_file: str, output_file: str):

    packages, lines = read_pip_packages_from_requirements(requirements_file)

    exist_packages, nonexist_packages = filter_nonexist_pip_packages(packages)

    exist_packages = set(exist_packages)

    with open(output_file, "w") as fout:
        for package, line in zip(packages, lines):
            if package is not None and package in exist_packages:
                fout.write(line + "\n")
                pass
            pass
        pass
    pass

    print(f"exist packages: {packages}")
    return exist_packages, nonexist_packages
    pass
