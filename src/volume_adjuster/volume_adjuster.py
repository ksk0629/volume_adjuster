import functools
import glob
import os

from pydub import AudioSegment

from .type_checker import TypeChecker


class VolumeAdjuster:
    """Volume adjuster class"""

    def __init__(self, dir_path: str, extensions: list[str], target_dbfs: float):
        # Create type checker
        self.__type_checker = TypeChecker()

        # Check types
        self.__type_checker.validate_basic_type("dir_path", dir_path, str)
        self.__type_checker.validate_basic_type("extensions", extensions, list)
        self.__type_checker.validate_basic_type("dir_path", dir_path, str)
        self.__type_checker.validate_list_elements_type("extensions", extensions, str)

        # Initialise member variables.
        self.__dir_path: str = dir_path
        self.__extensions: list[str] = map(
            lambda x: x if x[0] == "." else "." + x, extensions
        )
        self.__target_dbfs: float = target_dbfs

        self.__target_file_paths: list[str] = []
        self.__target_data: list[AudioSegment] = []
        self.__adjusted_data: list[AudioSegment] = []

    def __set_all_targets(self):
        """Set all target file paths to self.__target_file_paths."""
        # Get all file paths.
        all_file_paths: list[str] = glob.glob(os.path.join(self.__dir_path, "*"))

        # Extract only file paths whose extension is in self.__extensions.
        self.__target_file_paths = filter(
            lambda x: os.path.splitext(x)[1] in self.__extensions, all_file_paths
        )

        # Open all target files.
        self.__target_data = list(map(AudioSegment, self.__target_file_paths))

    @staticmethod
    def adjust(audio_data: AudioSegment, target_dbfs: float) -> AudioSegment:
        diff_dbfs = audio_data - target_dbfs
        return audio_data - diff_dbfs

    def __adjust_all_targets(self):
        self.__adjusted_data = list(
            map(
                functools.partial(self.adjust, target_dbfs=self.__target_dbfs),
                self.__target_data,
            )
        )

    def __export_adjusted_data(self):
        for target_file_path, adjusted_data in zip(
            self.__target_file_paths, self.__adjusted_data
        ):
            adjusted_data.export(
                target_file_path, format=os.path.splitext(target_file_path)[1][1:]
            )

    def run(self):
        self.__set_all_targets()
        self.__adjust_all_targets()
        self.__export_adjusted_data()
