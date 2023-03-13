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
    file_name,
    file_type,
    hash_type="SHA1",
    min_sec=5,
    max_sec=30,
    recur=True,
    progress_bar=False,
):
    os.chdir(destination_path)
    file_type_ = "." + file_type.lower()

    file_list = glob.glob(
        f"{source_path}/**/{file_name}{file_type_}", recursive={recur}
    )
    total_file_list = len(file_list)

    mode = input("Enter Mode (l:list or c:copy): ")

    for i, old_file in enumerate(file_list):
        file_size = os.stat(old_file).st_size
        pct = i / total_file_list

        old_name = os.path.basename(old_file).replace(file_type_, "")
        hash_text = make_hash(filename=old_file, hashtype=hash_type)
        short_hash_text = hash_text[0:7]
        new_file = ("_n_" + short_hash_text + file_type_).upper()
        new_full_path = destination_path + "\\" + new_file

        try:
            clip = VideoFileClip(old_file)
            duration_sec = clip.duration

        except:
            print(
                f"          Skip {i}. NO TIME {pct:.0%} of {total_file_list:>} | Size: {file_size} | File: {old_file}"
            )
            duration_sec = 0

        if min_sec <= duration_sec <= max_sec:  # min_size < file_size < max_size and
            # print(file_size)

            if mode == "l":
                mode_flag = "List"
            elif mode == "c":
                mode_flag = "Copy"
                try:
                    shutil.copy(old_file, new_full_path)
                except:
                    print(f"File: {new_file} already exists. Skip it")

            if progress_bar:
                print(f"\r {pct:.0%} " + round(pct * 10) * "**", end="")
            else:
                print(
                    f"{mode_flag} {i}. {pct:.0%} of {total_file_list:,>} | {hash_type:>}: {hash_text[0:7]} | New: {new_file:>} | Old: {old_name} | Size: {file_size:,} | {old_file} | Sec: {duration_sec:0.0f} "
                )


if __name__ == "__main__":
    pass
