import functools
import glob
import os

from pydub import AudioSegment

from src.volume_adjuster.type_checker import TypeChecker


class VolumeAdjuster:
    """Volume adjuster class"""

    def __init__(self, input_dir_path: str, extensions: list[str], target_dbfs: float, 
                 output_dir_path: str):
        """Initialise the member variables.

        :param str input_dir_path: a path to a target input directory
        :param list[str] extensions: a list of a target extensions
        :param float target_dbfs: a target decibel relative to the maximum possible loudness
        :param str output_dir_path: a path to a target output directory
        """
        # Create TypeChecker object.
        self.__type_checker = TypeChecker()

        # Check the types of the arguments.
        self.__type_checker.validate_basic_type("input_dir_path", input_dir_path, str)
        self.__type_checker.validate_basic_type("extensions", extensions, list)
        self.__type_checker.validate_basic_type("target_dbfs", target_dbfs, float)
        self.__type_checker.validate_basic_type("output_dir_path", output_dir_path, str)
        self.__type_checker.validate_list_elements_type("extensions", extensions, str)

        # Initialise member variables.
        self.__input_dir_path: str = input_dir_path
        self.__extensions: list[str] = list(map(
            # Add if there is no "." at the top of the extension
            lambda x: x if x[0] == "." else "." + x, extensions
        ))
        self.__target_dbfs: float = target_dbfs
        self.__output_dir_path: str = output_dir_path

        self.__target_file_paths: list[str] = []
        self.__target_data: list[AudioSegment] = []
        self.__adjusted_data: list[AudioSegment] = []
    
    @property
    def input_dir_path(self) -> str:
        return self.__input_dir_path
    
    @property
    def extensions(self) -> list[str]:
        return self.__extensions
    
    @property
    def target_dbfs(self) -> float:
        return self.__target_dbfs
    
    @property
    def output_dir_path(self) -> str:
        return self.__output_dir_path
    
    @property
    def target_file_paths(self) -> list[str]:
        return self.__target_file_paths
    
    @property
    def target_data(self) -> list[AudioSegment]:
        return self.__target_data
    
    @property
    def adjusted_data(self) -> list[AudioSegment]:
        return self.__adjusted_data

    def __set_all_targets(self):
        """Set all target file paths to self.__target_file_paths."""
        # Get all file paths under the target directory.
        all_file_paths: list[str] = glob.glob(os.path.join(self.__input_dir_path, "*"))

        # Extract only file paths whose extension is in self.__extensions.
        self.__target_file_paths = list(filter(
            lambda x: os.path.splitext(x)[1] in self.__extensions, all_file_paths
        ))

        # Open all target files.
        self.__target_data = list(map(
            AudioSegment.from_file, 
            self.__target_file_paths
        ))

    @staticmethod
    def adjust(audio_data: AudioSegment, target_dbfs: float) -> AudioSegment:
        """Adjust the volume of the audio data by the given target decibel relative to the maximum possible loudness.

        :param AudioSegment audio_data: a target audio data
        :param float target_dbfs: a target decibel relative to the maximum possible loudness
        :return AudioSegment: the adjusted audio data
        """
        diff_dbfs = audio_data.dBFS - target_dbfs
        return audio_data - diff_dbfs

    def __adjust_all_targets(self):
        """Adjust the volumes of all target audio data.
        """
        adjust_of_fixed_target_dbfs = functools.partial(self.adjust, target_dbfs=self.__target_dbfs)
        self.__adjusted_data = list(
            map(
                adjust_of_fixed_target_dbfs,
                self.__target_data,
            )
        )

    def __save_adjusted_data(self):
        """Save all adjusted target audio data.
        """
        for target_file_path, adjusted_data in zip(
            self.__target_file_paths, self.__adjusted_data
        ):
            # Create the output file_path.
            pre_output_file_path = os.path.join(self.__output_dir_path, os.path.basename(target_file_path))
            output_file_basename, _ = os.path.splitext(pre_output_file_path)
            output_file_path = output_file_basename + ".mp3"
            
            # Save the audio data.
            adjusted_data.export(
                output_file_path, format="mp3"
            )

    def run(self):
        """Load all target audio data, adjust the volumes and save them.
        """
        print("Obtaining target files => ", end="", flush=True)
        self.__set_all_targets()
        print("DONE", flush=True)
        print("Adjusting volumes => ", end="", flush=True)
        self.__adjust_all_targets()
        print("DONE", flush=True)
        print("Saving files => ", end="", flush=True)
        self.__save_adjusted_data()
        print("DONE", flush=True)
