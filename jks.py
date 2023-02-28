import re
import shutil
from pathlib import Path

jks_main_dir = Path("[Hyouuma] JK Tights (42-1)")


def get_jk_paths():
    jk_pattern = re.compile(r"JKタイツ\.(?P<jk>\d{2})")
    return {m["jk"]: p for p in Path.cwd().iterdir() if (m := jk_pattern.match(p.name))}


def clean_jk_png_names():
    for jk, jk_path in get_jk_paths().items():
        for png in jk_path.iterdir():
            png_pattern = re.compile(jk + r"_\d{2}")
            if not png_pattern.match(png.stem):
                png.rename(png.with_name(f"{jk}_{int(png.stem):02d}{png.suffix}"))


def generate_jks_from_main():
    png_pattern = re.compile(r"(?P<index>\d{3})_(?P<jk>\d{2})_(?P<page>\d{2})")
    png_matches = {
        m: png for png in jks_main_dir.iterdir() if (m := png_pattern.match(png.stem))
    }

    for match, png in png_matches.items():
        jk = Path.cwd() / f'JKタイツ.{match["jk"]}'
        if not jk.exists():
            Path.mkdir(jk)
        new_png = jk / f'{match["jk"]}_{match["page"]}{png.suffix}'
        if not new_png.exists():
            shutil.copy(png, new_png)


def generate_main_from_jks():
    png_pattern = re.compile(r"(?P<jk>\d{2})_(?P<page>\d{2})")
    pngs = {
        png_pattern.match(png.stem): png
        for jk, jk_path in get_jk_paths().items()
        for png in jk_path.iterdir()
    }
    sorted_pngs = list(
        sorted(
            pngs.items(),
            key=lambda entry: (-int(entry[0]["jk"]), int(entry[0]["page"])),
        )
    )
    for index, (_, png) in enumerate(sorted_pngs, start=1):
        new_png = jks_main_dir / f"{index:03d}_{png.name}"
        if not new_png.exists():
            shutil.copy(png, new_png)


clean_jk_png_names()
generate_main_from_jks()
