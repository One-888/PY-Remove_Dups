import hashlib
import glob
import shutil
import os


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

    for old_file in glob.glob(f"{source_path}/**/*{file_type_}", recursive=True):
        file_size = os.stat(old_file).st_size

        if min_size < file_size < max_size:
            old_name = os.path.basename(old_file).replace(file_type_, "")
            hash_text = make_hash(filename=old_file, hashtype=hash_type)

            short_hash_text = hash_text[0:7]
            new_file = ("_n_" + short_hash_text + file_type_).upper()
            # print(file_size)

            print(
                f"HASH {hash_type}: {hash_text[0:7]}  - New File: {new_file}  - Old File: {old_name}  - Size: {file_size}"
            )

            try:
                shutil.copy(old_file, new_file)
            except:
                print(print(f"File: {new_file} already exists. Skip it"))


if __name__ == "__main__":
    pass
