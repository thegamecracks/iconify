import argparse
import logging
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError

log = logging.getLogger(__name__)

NAME_RESAMPLING = {
    "nearest": Image.Resampling.NEAREST,
    "box": Image.Resampling.BOX,
    "bilinear": Image.Resampling.BILINEAR,
    "hamming": Image.Resampling.HAMMING,
    "bicubic": Image.Resampling.BICUBIC,
    "lanczos": Image.Resampling.LANCZOS,
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase logging verbosity",
    )
    parser.add_argument(
        "-s",
        "--size",
        default="64x64",
        help="The icon size to output (default: 64x64)",
        type=parse_size,
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Overwrite existing icons if necessary",
    )
    parser.add_argument(
        "-m",
        "--method",
        default="lanczos",
        help="Resampling algorithm to use (default: lanczos)",
        type=parse_resampler,
    )
    parser.add_argument(
        "input_dir",
        help="The directory to read images from (default: .)",
        nargs="?",
        type=Path,
    )
    parser.add_argument(
        "output_dir",
        help="The directory to output icons to (default: {input-dir}/icons)",
        nargs="?",
        type=Path,
    )

    args = parser.parse_args()
    verbose: int = args.verbose
    size: tuple[int, int] = args.size
    force: bool = args.force
    method: int = args.method
    input_dir: Path | None = args.input_dir
    output_dir: Path | None = args.output_dir

    if input_dir is None:
        input_dir = Path()
    if output_dir is None:
        output_dir = input_dir / "icons"

    configure_logging(verbose)

    n_resized = generate_icons(
        input_dir,
        output_dir,
        size=size,
        ignore_existing=not force,
        resampler=method,
    )
    print(n_resized, "icon(s) generated")


def parse_size(s: str) -> tuple[int, int]:
    x, _, y = s.lower().partition("x")
    x, y = x.strip(), y.strip()

    x = int(x)
    if x < 0:
        raise ValueError(f"x-size must be positive, not {x}")

    try:
        y = int(y)
    except ValueError:
        return x, x

    if y < 0:
        raise ValueError(f"y-size must be positive, not {x}")

    return x, y


def parse_resampler(s: str) -> int:
    s = s.lower().strip()
    try:
        return NAME_RESAMPLING[s]
    except KeyError:
        raise ValueError(f"Invalid resampling algorithm {s!r}") from None


def configure_logging(verbose: int) -> None:
    if verbose >= 2:
        level = logging.DEBUG
    elif verbose >= 1:
        level = logging.INFO
    else:
        level = logging.WARNING

    logging.basicConfig(level=level)


def generate_icons(
    input_dir: Path,
    output_dir: Path,
    *,
    size: tuple[int, int],
    ignore_existing: bool,
    resampler: int,
) -> int:
    output_dir.mkdir(exist_ok=True, parents=True)

    n_resized = 0
    for source_path in input_dir.iterdir():
        if not source_path.is_file():
            continue

        output_path = output_dir / source_path.name
        if ignore_existing and output_path.is_file():
            log.info("Ignoring file %s, icon already exists", source_path.name)
            continue

        try:
            source_image = Image.open(source_path)
        except UnidentifiedImageError:
            log.info("Ignoring file %s", source_path.name)
            continue

        with source_image:
            resized = ImageOps.fit(source_image, size, method=resampler)

        resized.save(output_path)
        log.info("Written icon for %s", source_path.name)
        n_resized += 1

    return n_resized


if __name__ == "__main__":
    main()
