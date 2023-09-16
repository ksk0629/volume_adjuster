import functools
import glob
import os

from pydub import AudioSegment

from .type_checker import TypeChecker


class VolumeAdjuster:
    """Volume adjuster class"""

    def __init__(self, dir_path: str, extensions: list[str], target_dbfs: float):
        """Initialise the member variables.

        :param str dir_path: a path to a target directory
        :param list[str] extensions: a list of a target extensions
        :param float target_dbfs: a target decibel relative to the maximum possible loudness
        """
        # Create TypeChecker object.
        self.__type_checker = TypeChecker()

        # Check the types of the arguments.
        self.__type_checker.validate_basic_type("dir_path", dir_path, str)
        self.__type_checker.validate_basic_type("extensions", extensions, list)
        self.__type_checker.validate_basic_type("dir_path", dir_path, str)
        self.__type_checker.validate_list_elements_type("extensions", extensions, str)

        # Initialise member variables.
        self.__dir_path: str = dir_path
        self.__extensions: list[str] = map(
            # Add if there is no "." at the top of the extension
            lambda x: x if x[0] == "." else "." + x, extensions
        )
        self.__target_dbfs: float = target_dbfs

        self.__target_file_paths: list[str] = []
        self.__target_data: list[AudioSegment] = []
        self.__adjusted_data: list[AudioSegment] = []

    def __set_all_targets(self):
        """Set all target file paths to self.__target_file_paths."""
        # Get all file paths under the target directory.
        all_file_paths: list[str] = glob.glob(os.path.join(self.__dir_path, "*"))

        # Extract only file paths whose extension is in self.__extensions.
        self.__target_file_paths = filter(
            lambda x: os.path.splitext(x)[1] in self.__extensions, all_file_paths
        )

        # Open all target files.
        self.__target_data = list(map(AudioSegment, self.__target_file_paths))

    @staticmethod
    def adjust(audio_data: AudioSegment, target_dbfs: float) -> AudioSegment:
        """Adjust the volume of the audio data by the given target decibel relative to the maximum possible loudness.

        :param AudioSegment audio_data: a target audio data
        :param float target_dbfs: a target decibel relative to the maximum possible loudness
        :return AudioSegment: the adjusted audio data
        """
        diff_dbfs = audio_data - target_dbfs
        return audio_data - diff_dbfs

    def __adjust_all_targets(self):
        """Adjust the volumes of all target audio data.
        """
        self.__adjusted_data = list(
            map(
                functools.partial(self.adjust, target_dbfs=self.__target_dbfs),
                self.__target_data,
            )
        )

    def __save_adjusted_data(self):
        """Save all adjusted target audio data.
        """
        for target_file_path, adjusted_data in zip(
            self.__target_file_paths, self.__adjusted_data
        ):
            adjusted_data.export(
                target_file_path, format=os.path.splitext(target_file_path)[1][1:]
            )

    def run(self):
        """Load all target audio data, adjust the volumes and save them.
        """
        self.__set_all_targets()
        self.__adjust_all_targets()
        self.__save_adjusted_data()
