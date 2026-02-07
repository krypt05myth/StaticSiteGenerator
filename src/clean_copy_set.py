import os
import sys
import shutil
"""
    SITE ASSET PIPELINE: STATIC TO PUBLIC MIRRORING
    This module manages the fresh-start build process by nuking the 'public' 
    canvas and recursively mirroring the 'static' source with strict path 
    security boundaries to prevent accidental filesystem leakage.
"""
## With statically set filepath parameters, build path, delete path, remake path 
def reset_dir():#working_dir: str, dir: str):
    base_dir = "/home/knix/Coding/Boot.dev/StaticSiteGenerator/"
    dir = "docs" # was "public"
    base_path = os.path.abspath(base_dir)
    full_path = os.path.abspath(os.path.join(base_dir, dir))
    # Security Barrier: Only allow deletion if the target is within our project and specifically named 'docs' but was coded to be 'public'
    if not full_path.startswith(base_path) or "docs" not in full_path:
        return f"ERROR: {dir} is not 'docs/' and not in {base_path}. Cannot delete outside the designated full path."
    # The Nuke: Includes utility to guarantee a zero-state rebuild
    if os.path.exists(full_path):
        print(f"Beginning cleanup of {full_path}, before rebuilding it afresh .....")
        shutil.rmtree(full_path) #course recommended this utility specifically, which is meant to nuke the whole folder before the rebuild
    print(f"Rebuilding the full empty path at: {full_path} .....")
    os.mkdir(full_path)

def recursed_copy_path_checker_helper():
    """
    PATH VALIDATION LAYER
    Primary security boundary for the recursive worker. 
    Verifies that paths exist within the base directory and 
    adhere to the 'static' to 'docs' (formerly'public') mapping schema.
    """
    base_dir = "/home/knix/Coding/Boot.dev/StaticSiteGenerator/"
    source_dir = "static"
    target_dir = "docs"
    base_path = os.path.abspath(base_dir)
    source_path = os.path.abspath(os.path.join(base_dir, source_dir))
    target_path = os.path.abspath(os.path.join(base_dir, target_dir))
    # Guardrail: Verify both paths are localized and correctly labeled
    if (
        not (source_path.startswith(base_path)
        or target_path.startswith(base_path)) 
        or "static" not in source_path
        or "docs" not in target_path
    ):
        return f"ERROR: {source_dir} not 'static/' or {target_dir} not 'docs/', or either not in {base_path}."
    # Handshake: Transition to the recursive worker
    _recursed_copy(source_path, target_path)

def _recursed_copy(curr_src, curr_tgt):
    """
    RECURSIVE WORKER
    Dives through the directory tree, ensuring folders are 
    created at the destination before files are mirrored [cite: 2025-11-25].
    """
    # Ensure the current directory depth exists in the target
    if not os.path.exists(curr_tgt): 
        os.mkdir(curr_tgt)
    # Iterate through current level contents    
    curr_src_contents = os.listdir(curr_src)
    for ea in curr_src_contents:
        new_src = os.path.join(curr_src, ea)
        new_tgt = os.path.join(curr_tgt, ea)
        print(f"Copying {new_src} --> {new_tgt}")
        # Maximal efficiency: Check file status before attempting a recursive dive
        if os.path.isfile(new_src):
            shutil.copy(new_src, new_tgt)
        elif os.path.isdir(new_src):
            _recursed_copy(new_src, new_tgt) 