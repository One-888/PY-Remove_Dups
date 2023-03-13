from remove_dups import main


main(
    source_path=r"C:\Downloads\MOV",
    destination_path=r"C:\Downloads\out",
    file_name="*",
    file_type="MOV",
    hash_type="SHA1",
    min_sec=1,
    max_sec=30,
    recur=True,
    progress_bar=False,
)
