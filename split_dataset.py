"""
Script untuk membagi dataset TrashType_Image_Dataset
menjadi folder train dan val.

Struktur dataset asal:
    TrashType_Image_Dataset/
        cardboard/
        glass/
        metal/
        paper/
        plastic/
        trash/

Struktur hasil setelah split:
    TrashType_Image_Dataset/
        train/
            cardboard/
            glass/
            metal/
            paper/
            plastic/
            trash/
        val/
            cardboard/
            glass/
            metal/
            paper/
            plastic/
            trash/
"""

import os
import shutil
import random
from pathlib import Path

# ─────────────────────────────────────────────
# KONFIGURASI
# ─────────────────────────────────────────────
DATASET_DIR   = "TrashType_Image_Dataset"   # path ke folder dataset
TRAIN_RATIO   = 0.8                         # 80% train, 20% val
RANDOM_SEED   = 42                          # untuk hasil yang konsisten
CLASSES       = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]

# ekstensi gambar yang dikenali
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}
# ─────────────────────────────────────────────


def get_image_files(folder: Path) -> list[Path]:
    """Kembalikan daftar file gambar di dalam folder (tidak rekursif)."""
    return [
        f for f in folder.iterdir()
        if f.is_file() and f.suffix.lower() in IMAGE_EXTS
    ]


def split_dataset(
    dataset_dir: str,
    train_ratio: float,
    seed: int,
    classes: list[str],
) -> None:
    base = Path(dataset_dir)

    if not base.exists():
        raise FileNotFoundError(f"Folder dataset tidak ditemukan: {base.resolve()}")

    train_base = base / "train"
    val_base   = base / "val"

    random.seed(seed)

    total_train = 0
    total_val   = 0

    print(f"{'='*55}")
    print(f" Dataset  : {base.resolve()}")
    print(f" Rasio    : train={train_ratio:.0%}  val={1-train_ratio:.0%}")
    print(f" Seed     : {seed}")
    print(f"{'='*55}\n")

    for cls in classes:
        src_dir = base / cls

        if not src_dir.exists():
            print(f"[LEWATI] Folder tidak ditemukan: {src_dir}")
            continue

        images = get_image_files(src_dir)

        if not images:
            print(f"[LEWATI] Tidak ada gambar di: {src_dir}")
            continue

        random.shuffle(images)

        split_idx   = int(len(images) * train_ratio)
        train_files = images[:split_idx]
        val_files   = images[split_idx:]

        # Buat folder tujuan
        (train_base / cls).mkdir(parents=True, exist_ok=True)
        (val_base   / cls).mkdir(parents=True, exist_ok=True)

        # Salin file (tidak memindahkan, agar data asli tetap ada)
        for f in train_files:
            shutil.copy2(f, train_base / cls / f.name)

        for f in val_files:
            shutil.copy2(f, val_base / cls / f.name)

        print(
            f"[{cls:>10}]  total={len(images):>4}  "
            f"train={len(train_files):>4}  val={len(val_files):>4}"
        )

        total_train += len(train_files)
        total_val   += len(val_files)

    print(f"\n{'─'*55}")
    print(
        f"{'TOTAL':>12}  total={total_train+total_val:>4}  "
        f"train={total_train:>4}  val={total_val:>4}"
    )
    print(f"{'─'*55}")
    print(f"\n✅ Split selesai!")
    print(f"   Train → {train_base.resolve()}")
    print(f"   Val   → {val_base.resolve()}")


if __name__ == "__main__":
    split_dataset(
        dataset_dir=DATASET_DIR,
        train_ratio=TRAIN_RATIO,
        seed=RANDOM_SEED,
        classes=CLASSES,
    )