import argparse

import yaml

from src.volume_adjuster.volume_adjuster import VolumeAdjuster


def main(config_yaml_path):
    with open(config_yaml_path, "r") as yaml_f:
        config = yaml.safe_load(yaml_f)

    volume_adjuster = VolumeAdjuster(**config)

    volume_adjuster.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Adjust volumes of audio files under a given directory."
    )
    parser.add_argument("-c", "--config_yaml_path", required=True, type=str)
    args = parser.parse_args()

    main(args.config_yaml_path)
