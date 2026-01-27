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

def recursed_copy_path_checker_helper():
    base_dir = "/home/knix/Coding/Boot.dev/StaticSiteGenerator/"
    source_dir = "static"
    target_dir = "public"
    base_path = os.path.abspath(base_dir)
    source_path = os.path.abspath(os.path.join(base_dir, source_dir))
    target_path = os.path.abspath(os.path.join(base_dir, target_dir))
    if (
        not (source_path.startswith(base_path)
        or target_path.startswith(base_path)) 
        or "static" not in source_path
        or "public" not in target_path
    ):
        return f"ERROR: {source_dir} not 'static/' or {target_dir} not 'public', or either not in {base_path}."
    _recursed_copy(source_path, target_path)

def _recursed_copy(curr_src, curr_tgt):
    if not os.path.exists(curr_tgt): 
        os.mkdir(curr_tgt)    
    curr_src_contents = os.listdir(curr_src)
    for ea in curr_src_contents:
        new_src = os.path.join(curr_src, ea)
        new_tgt = os.path.join(curr_tgt, ea)
        print(f"Copying {new_src} --> {new_tgt}")
        if os.path.isfile(new_src):
            shutil.copy(new_src, new_tgt)
        elif os.path.isdir(new_src):
            _recursed_copy(new_src, new_tgt) 