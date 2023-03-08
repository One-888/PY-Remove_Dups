import hashlib
import glob
import shutil
import os
from moviepy.editor import VideoFileClip


def make_hash(filename, hashtype):
    hashtype = hashtype.upper()
    BLOCKSIZE = 65536

    if hashtype == "MD5":
        hasher = hashlib.md5()
    elif hashtype == "SHA1":
        hasher = hashlib.sha1()
    elif hashtype == "SHA256":
        hasher = hashlib.sha256()

    with open(filename, "rb") as f:
        buf = f.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(BLOCKSIZE)
    return hasher.hexdigest()


def main(
    source_path,
    destination_path,
    file_type,
    hash_type="SHA1",
    min_size=1_000_000,
    max_size=10_000_000,
):
    os.chdir(destination_path)
    file_type_ = "." + file_type.lower()

    file_list = glob.glob(f"{source_path}/**/*{file_type_}", recursive=True)
    total_file_list = len(file_list)

    mode = input("Enter Mode(list or copy): ")

    for i, old_file in enumerate(file_list):
        file_size = os.stat(old_file).st_size
        pct = (i / total_file_list) * 100

        clip = VideoFileClip(old_file)
        duration_sec = clip.duration

        if min_size < file_size < max_size and 5 < duration_sec < 60:
            old_name = os.path.basename(old_file).replace(file_type_, "")
            hash_text = make_hash(filename=old_file, hashtype=hash_type)

            short_hash_text = hash_text[0:7]
            new_file = ("_n_" + short_hash_text + file_type_).upper()
            # print(file_size)

            if mode == "list":
                print(
                    f"List: {i}. {pct:.0f}pct of {total_file_list} HASH | {hash_type}: {hash_text[0:7]} | Second: {duration_sec} | New: {new_file} | Old: {old_name} | Size: {file_size}"
                )
            else:
                print(
                    f"Copy: {i}. {pct:.0f}pct of {total_file_list} HASH | {hash_type}: {hash_text[0:7]} | Second: {duration_sec} | New: {new_file} | Old: {old_name} | Size: {file_size}"
                )

                try:
                    shutil.copy(old_file, new_file)
                except:
                    print(print(f"File: {new_file} already exists. Skip it"))


if __name__ == "__main__":
    pass
