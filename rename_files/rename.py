from pathlib import Path

def rename_files_with_counter(folder, prefix="", extension=None):
    folder = Path(folder)

    files = sorted(f for f in folder.iterdir() if f.is_file())

    for index, file_path in enumerate(files, start=1):

        if file_path.name[:4].isdigit():
            continue

        if extension and file_path.suffix != extension:
            continue

        new_name = f"{index:03d}_{file_path.name}"
        new_path = file_path.with_name(new_name)

        if new_path.exists():
            print(f"Skipped (exists): {new_name}")
            continue

        file_path.rename(new_path)
        print(f"Renamed: {file_path.name} → {new_name}")
