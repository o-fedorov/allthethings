import toml


def get_config():
    return toml.load(".allthethings.toml")
