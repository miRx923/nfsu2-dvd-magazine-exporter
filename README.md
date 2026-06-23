# NFSU2 DVDs/Magazines Export Tool

A Python port of the [hkAlice/nfsu2-magazine-worker](https://github.com/hkAlice/nfsu2-magazine-worker). Batch exports DVD cover and magazine image files from **Need for Speed: Underground 2** to standard PNG format.

---

## Description

Need for Speed: Underground 2 stores in-game DVD cover and magazine images in a custom binary format with a 36-byte header and raw BGRA pixel data at a fixed resolution of 512×512. This script scans your game asset folder, converts every image file to PNG, and automatically sorts the output into `DVDs/` and `Magazines/` subdirectories based on the source folder name.

---

## Requirements

- Python 3.7+
- [Pillow](https://pypi.org/project/pillow/)

Install the dependency with:

```bash
pip install pillow
```

---

## Usage

Place `nfsu2_exporter.py` next to your `NFS Underground 2/` folder:

```
nfsu2_exporter.py
NFS Underground 2/
    DVD Cover 1/
        DVDFile
    DVD Cover 2/
        DVDFile
    Magazine 1/
        magazine
    ...
```
`Folder with the DVDs/Magazines can be found at location: (Users/your_name/AppData/Local/NFS Underground 2)`

Run the script:

```bash
python nfsu2_dvd_and_magazines_export.py
```

The script will:

1. Create an `NFSU2 Export/` folder with two subdirectories — `DVDs/` and `Magazines/`
2. Scan every subfolder inside `NFS Underground 2/`
3. Export each image file to PNG
4. Route the output to `DVDs/` if the subfolder name contains `DVD`, or to `Magazines/` if it contains `Magazine`
5. Skip any subfolder whose name matches neither keyword

Output structure:

```
NFSU2 Export/
    DVDs/
        dvd.png
        ...
    Magazines/
        magazine.png
        ...
```

---

## How It Works

Each source file begins with a 36-byte (`0x24`) header followed by raw pixel data in **BGRA** format at 512×512 resolution.

During export, the script:

1. Reads the raw file and skips the header
2. Swaps the **B** and **R** channels on every pixel (BGRA → RGBA)
3. Forces the alpha channel to `0xFF` (fully opaque)
4. Performs a circular left-rotate of the first 36 bytes of pixel data to correct a padding alignment quirk present in the game renderer
5. Saves the result as a standard RGBA PNG

---

## Credits

Original C++ implementation - [hkAlice/nfsu2-magazine-worker](https://github.com/hkAlice/nfsu2-magazine-worker).  
Python port based on the original source code.
