import argparse
import sys
import time

import tomli
import tomli_w


def version(tag: str = "test") -> str:
    match tag:
        case "test":
            current_time = time.localtime()
            time_str_ = f"{current_time.tm_year:04d}.{current_time.tm_mon:02d}.{current_time.tm_mday:02d}.{current_time.tm_hour:02d}{current_time.tm_min:02d}"
            version_name = time_str_
        case "official":
            current_time = time.localtime()
            version_name = "0.1.0"
        case _:
            raise ValueError(f"Unknown tag: {tag}, expected 'test' or 'official'.")
    return version_name


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--channel",
        help="选择上传通道（test 或 official，默认为 test）",
        default="test",
    )

    args = parser.parse_args()

    current_version = version(args.channel)
    with open("pyproject.toml", "rb") as f:
        meta = tomli.load(f)
        meta["project"]["version"] = current_version

    with open("pyproject.toml", "wb") as f2:
        tomli_w.dump(meta, f2)

    print(f"Version updated to {current_version} in pyproject.toml")
    pass
