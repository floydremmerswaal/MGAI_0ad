"""
    This script wraps the rllib rollout command but uses the custom environment.
"""
from ray.rllib.evaluate import create_parser
from ray.rllib.rollout import run
from ray.tune.registry import register_env
from .env import register_envs
from pcg.main import *

import pathlib
import os
import sys
import zipfile
import shutil
import glob


def update_env_map(env: str, pcg: bool, setup: bool = False):
    if sys.platform == 'win32':
        path = os.path.join(pathlib.Path.home(), "Documents", "My Games", "0ad", "mods", "user", "maps", "scenarios")
    elif sys.platform == 'darwin':
        path = os.path.join(pathlib.Path.home(), "Library", "Application Support", "0ad", "mods", "rl-scenarios")
        toor = os.path.join(pathlib.Path.home(), "Library", "Application Support", "0ad", "mods", "rl-scenarios")
        unzipped_path = os.path.join(path, "rl-scenarios")
        zip_path = os.path.join(path, "rl-scenarios.zip")
    elif sys.platform == 'linux':
        raise ValueError("NOT SUPPORTED")

    if sys.platform == 'darwin':
        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall(unzipped_path)
            path = os.path.join(unzipped_path, "maps", "scenarios")

    if setup: # only required if they installed the mod from online resource and not the one we provided
        # duplicate .pmp file for CavalryVsInfantryMaze.xml
        pmp_file = glob.glob(os.path.join(path, "CavalryVsInfantry.pmp"))[0]
        shutil.copy(pmp_file, os.path.join(path, "CavalryVsInfantryMaze.pmp"))
        # copy city .pmp file from project location
        shutil.copy("pcg/templates/CavalryVsInfantryCity.pmp", os.path.join(path, "CavalryVsInfantryCity.pmp"))


    if "Maze" in env:
        cavalryVsInfantryMaze(filename=os.path.join(path, "CavalryVsInfantryMaze.xml"))
    elif "City" in env:
        cavalryVsInfantryCity(os.path.join(path, "CavalryVsInfantryCity.xml"))

    if sys.platform == 'darwin':
        files_to_zip, roots_to_zip = [], []
        for root, _, files in os.walk(unzipped_path):
            for f in files:
                roots_to_zip.append(os.path.join(root[len(unzipped_path):], f))
                files_to_zip.append(os.path.join(root, f))

        with zipfile.ZipFile(zip_path, 'w') as z:
            for f, r in zip(files_to_zip, roots_to_zip):
                z.write(f, r)
            shutil.rmtree(unzipped_path)


if __name__ == '__main__':
    parser = create_parser()

    parser.add_argument("--pcg", help="whether to use PCG and create a new map.", action="store_true")
    parser.add_argument("--pmp_setup", help="this setup is required if you did not install the .zip folder containing our predefined environments.", action="store_true")

    parser.set_defaults(env='CavalryVsInfantry', no_render=True, pcg=False)

    args = parser.parse_args()

    if args.pcg:
        update_env_map(args.env, args.pcg, args.pmp_setup)

    register_envs()

    if not args.pmp_setup:
        run(args, parser)
