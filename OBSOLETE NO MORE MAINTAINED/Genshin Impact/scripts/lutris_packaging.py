"""
MIT License

Copyright (c) 2023 zeroday0619 <zeroday0619_dev@outlook.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
__version__ = 360

import os
import zipfile
import logging
from shutil import copyfile, copy

logging.basicConfig(format=logging.BASIC_FORMAT, level=logging.INFO)
logger = logging.getLogger("lutris_packaging.py")




def opener(path, flags):
    return os.open(path, flags, 0o777)

class CreateDirFaild(OSError):
    pass


work_dir = os.getcwd()
gi_patch_root_dir = f"{work_dir}/gi_patch_{__version__}"
patch_files_dir = f"{gi_patch_root_dir}/patch_files"


def mkdir_gi_patch():
    try:
        if not os.path.exists(gi_patch_root_dir):
            logger.info(f"create dir -> {gi_patch_root_dir}")
            os.makedirs(gi_patch_root_dir)
        else:
            logger.warning(f"already exist -> {gi_patch_root_dir}")

        if not os.path.exists(patch_files_dir):
            logger.info(f"create dir -> {patch_files_dir}")
            os.makedirs(patch_files_dir)
        else:
            logger.warning(f"already exist -> {patch_files_dir}")
    except OSError:
        raise CreateDirFaild()


user_patch_root_dir = f"{work_dir}/{__version__}"
user_patch_files_dir = f"{user_patch_root_dir}/patch_files"


def copy_gi_patch():
    if not os.path.exists(user_patch_root_dir):
        logger.error(f"Directory is not found -> {user_patch_root_dir}")
        raise NotADirectoryError()

    logger.info(f"copy {user_patch_root_dir}/patch.sh -> {gi_patch_root_dir}/patch.sh")
    copyfile(f"{user_patch_root_dir}/patch.sh", f"{gi_patch_root_dir}/patch.sh")

    logger.info(f"copy {user_patch_root_dir}/patch_anti_logincrash.sh -> {gi_patch_root_dir}/patch_anti_logincrash.sh")
    copyfile(f"{user_patch_root_dir}/patch_anti_logincrash.sh", f"{gi_patch_root_dir}/patch_anti_logincrash.sh")

    logger.info(f"copy {user_patch_root_dir}/patch_revert.sh -> {gi_patch_root_dir}/patch_revert.sh")
    copyfile(f"{user_patch_root_dir}/patch_revert.sh", f"{gi_patch_root_dir}/patch_revert.sh")

    src_files = os.listdir(user_patch_files_dir)
    for file_name in src_files:
        full_file_name = os.path.join(user_patch_files_dir, file_name)
        if os.path.isfile(full_file_name):
            logger.info(f"copy {full_file_name} -> {patch_files_dir}/{file_name}")
            copy(full_file_name, patch_files_dir)


def create_scripts():
    os.umask(0)
    if not os.path.exists(f'{gi_patch_root_dir}/ex_apatch.sh'):
        logger.info(f"create scripts -> {gi_patch_root_dir}/ex_apatch.sh")
        with open(f'{gi_patch_root_dir}/ex_apatch.sh', 'a', opener=opener) as ex_apatch:
            ex_apatch.write('\n#!/bin/bash')
            ex_apatch.write('\ncurrent_path=$(pwd)')
            ex_apatch.write('\ncd "$current_path"')
            ex_apatch.write('\ncd "../Program Files/Genshin Impact/Genshin Impact game/"')
            ex_apatch.write('\nbash ../../../gi_patch/patch.sh')
            ex_apatch.write('\nbash ../../../gi_patch/patch_anti_logincrash.sh')
            ex_apatch.write('\necho "Press enter to close this window..."')
            ex_apatch.write('\nread a')
    else:
        logger.warning(f"already exist -> {gi_patch_root_dir}/ex_apatch.sh")

    if not os.path.exists(f'{gi_patch_root_dir}/ex_rpatch.sh'):
        logger.info(f"create scripts -> {gi_patch_root_dir}/ex_rpatch.sh")
        with open(f'{gi_patch_root_dir}/ex_rpatch.sh', 'a', opener=opener) as ex_rpatch:
            ex_rpatch.write('\n#!/bin/bash')
            ex_rpatch.write('\ncurrent_path=$(pwd)')
            ex_rpatch.write('\ncd "$current_path"')
            ex_rpatch.write('\ncd "../Program Files/Genshin Impact/Genshin Impact game/"')
            ex_rpatch.write('\nbash ../../../gi_patch/patch_revert.sh')
            ex_rpatch.write('\necho "Press enter to close this window..."')
            ex_rpatch.write('\nread a')
    else:
        logger.warning(f"already exist -> {gi_patch_root_dir}/ex_rpatch.sh")


def compression():
    logger.info("Compression start")
    zip_f = zipfile.ZipFile(f"gi_patch_{__version__}.zip", "w")
    os.chdir(gi_patch_root_dir)
    for (path, dir, files) in os.walk(gi_patch_root_dir):
        for file in files:
            logger.info(f"ADD -> {os.path.relpath(path, gi_patch_root_dir)}/{file}")
            zip_f.write(os.path.join(os.path.relpath(path, gi_patch_root_dir), file), compress_type=zipfile.ZIP_DEFLATED)
    zip_f.close()
    logger.info(f"Compression complete: gi_patch_{__version__}.zip")


mkdir_gi_patch()
copy_gi_patch()
create_scripts()
compression()
