import os
import sys
import shutil

def reset_dir():#working_dir: str, dir: str):
    base_dir = "/home/knix/Coding/Boot.dev/StaticSiteGenerator/"
    dir = "public"
    base_path = os.path.abspath(base_dir)
    full_path = os.path.abspath(os.path.join(base_dir, dir))
    if not full_path.startswith(base_path) or "public" not in full_path:
        return f"ERROR: {dir} is not 'public/' and not in {base_path}. Cannot delete outside the designated full path."
    if os.path.exists(full_path):
        print(f"Beginning cleanup of {full_path}, before rebuilding it afresh .....")
        shutil.rmtree(full_path) #course recommended this utility specifically, which is meant to nuke the whole folder before the rebuild
    print(f"Rebuilding the full empty path at: {full_path} .....")
    os.mkdir(full_path)