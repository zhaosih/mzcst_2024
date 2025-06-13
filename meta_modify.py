import tomli

if __name__ == "__main__":
    with open("pyproject.toml", "rb") as f:
        meta = tomli.load(f)
    pass
