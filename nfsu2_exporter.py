import sys
from pathlib import Path
from PIL import Image

MAGAZINE_WIDTH = 512
MAGAZINE_HEIGHT = 512

def transform_raw_image(img_bytes, shift_left_padding=False, preserve_alpha=False):
    img_bytearray = bytearray(img_bytes)

    for i in range(0, len(img_bytearray), 4):
        if i + 3 >= len(img_bytearray):
            break

        img_bytearray[i], img_bytearray[i+2] = img_bytearray[i+2], img_bytearray[i]

        if not preserve_alpha:
            img_bytearray[i+3] = 0xFF

    if shift_left_padding:
        img_bytearray = img_bytearray[36:] + img_bytearray[:36]

    return img_bytearray

def export_dvd_or_magazine(file_path, output_dir):
    print(f"Processing: {file_path.parent.name}/{file_path.name}")
    try:
        with open(file_path, 'rb') as f:
            magazine_data = f.read()
    except IOError:
        print(f"  ERROR: Failed to load file: {file_path}")
        return False

    header_size = 0x24
    img_data = magazine_data[header_size:]

    transformed_data = transform_raw_image(img_data, shift_left_padding=True, preserve_alpha=False)

    try:
        img = Image.frombytes('RGBA', (MAGAZINE_WIDTH, MAGAZINE_HEIGHT), bytes(transformed_data))

        out_path = output_dir / file_path.with_suffix('.png').name
        img.save(out_path)
        print(f"  Saved: {out_path}")
        return True
    except Exception as e:
        print(f"  ERROR: Failed to process/save image. ({e})")
        return False

def main():
    source_folder = "NFS Underground 2"
    base_path = Path(source_folder)

    export_base = Path("NFSU2 Export")
    dvd_dir = export_base / "DVDs"
    mag_dir = export_base / "Magazines"

    print(f"Looking for folder: '{source_folder}'...")

    if not base_path.exists() or not base_path.is_dir():
        print(f"ERROR: Folder '{source_folder}' was not found next to the script.")
        sys.exit(1)

    dvd_dir.mkdir(parents=True, exist_ok=True)
    mag_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output folders ready: '{dvd_dir}' and '{mag_dir}'")
    print()

    success_count = 0

    for subfolder in sorted(base_path.iterdir()):
        if not subfolder.is_dir():
            continue

        sub_name_upper = subfolder.name.upper()

        if "DVD" in sub_name_upper:
            target_out_dir = dvd_dir
        elif "MAGAZINE" in sub_name_upper:
            target_out_dir = mag_dir
        else:
            print(f"WARNING: Skipping folder '{subfolder.name}' (name contains neither 'DVD' nor 'Magazine').")
            continue

        files = [f for f in subfolder.iterdir() if f.is_file() and f.suffix.lower() != '.png']

        if len(files) == 1:
            if export_dvd_or_magazine(files[0], target_out_dir):
                success_count += 1
        elif len(files) > 1:
            print(f"WARNING: Folder '{subfolder.name}' contains more than 1 source file. Skipping.")
        else:
            print(f"WARNING: Folder '{subfolder.name}' contains no source files.")

    print()
    print(f"Batch export complete. Successfully exported: {success_count} file(s).")

if __name__ == '__main__':
    main()