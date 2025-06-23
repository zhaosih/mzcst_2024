import time

import tomli
import tomli_w


def version() -> str:
    current_time = time.localtime()
    time_str_ = f"{current_time.tm_year:04d}.{current_time.tm_mon:02d}.{current_time.tm_mday:02d}.{current_time.tm_hour:02d}{current_time.tm_min:02d}"
    return time_str_


if __name__ == "__main__":

    current_version = version()
    with open("pyproject.toml", "rb") as f:
        meta = tomli.load(f)
        meta["project"]["version"] = current_version

    with open("pyproject.toml", "wb") as f2:
        tomli_w.dump(meta, f2)

    print(f"Version updated to {current_version} in pyproject.toml")
    pass
