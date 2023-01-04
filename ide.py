from abc import ABC, abstractmethod
from exceptions import InvalidChoiceError
import csv
import requests
import pandas as pd
from pathlib2 import Path, PurePosixPath


class IDE(ABC):
    def __init__(self, level: str, directory: str, topics: list):
        self.level = level
        self.directory = directory
        self.topics = topics
        # Checking if there are CSV files to be used for games
        p = Path(directory).glob('**/*')
        files = [x for x in p if x.is_file()]
        if len(files) == 0:
            self.get_shortcuts()

    @abstractmethod
    def command_dictionary(self) -> None:
        pass

    @abstractmethod
    def get_shortcuts(self) -> None:
        pass

    @property
    def level(self) -> str:
        return self._level

    @level.setter
    def level(self, level) -> None:
        if level.lower() not in ["junior", "senior", "executive"]:
            raise InvalidChoiceError("Invalid Level call from class")
        self._level = level

    @abstractmethod
    def directory(self) -> None:
        """Folder where CSVs reside."""
        pass

    @abstractmethod
    def topics(self) -> None:
        """A list of the topics according to the IDE chosen"""
        pass


class IntelliJ(IDE):
    topics = [
        "top shortcuts",
        "build projects",
        "basic editing",
        "caret navigation",
        "select text",
        "code folding",
        "multiple carets and selection ranges",
        "coding assistance",
        "context navigation",
        "find everything",
        "navigate from symbols",
        "code analysis",
        "run and debug",
        "refactorings",
        "global vcs actions",
        "differences viewer",
        "tool windows",
    ]

    directory = Path("shortcut_csvs/intellij_shortcut_csvs")

    def __init__(
            self, level: str, directory: str = directory, topics: list = topics
    ) -> None:
        super().__init__(level, directory, topics)
        # self.topic = topic
        self.commands = self.command_dictionary()

    def command_dictionary(self) -> dict:
        # Predefine dictionary
        commands = {}
        # Looping through the files and topic list at the same time
        p = self.directory.glob('**/*')
        files = [x for x in p]
        for topic, file in zip(self.topics, files):
            # Predefine a dictionary to hold task:key_press commands
            topic_commands = {}
            with open(file) as rfile:
                reader = csv.reader(rfile)
                # Loop over file
                for row in reader:
                    task, key_press = row
                    topic_commands[task.lower()] = key_press.lower()
                commands[topic] = topic_commands
                topic_commands = {}
        return commands

    def get_shortcuts(self) -> None:
        """Gets CSV files from Jetbrains for IntelliJ shortcuts for Windows."""

        url = "https://www.jetbrains.com/help/idea/reference-keymap-win-default.html"
        html = requests.get(url).content
        df_list = pd.read_html(html)
        df = df_list
        # Though the tables are separated thanks to pandas, a separate index is being used so that file names do not
        # repeat
        for i, df in enumerate(df_list):
            df.to_csv(
                PurePosixPath('shortcut_csvs/intellij_shortcut_csvs').joinpath(f'intellij{i:02}.csv'),
                index=False,
                header=None,
            )


class AndroidStudio(IDE):
    topics = []
    system = 1  # If system == Windows/Linux, this is 1, else

    directory = Path("shortcut_csvs/android_studio_shortcut_csvs")

    def __init__(
            self, level: str, system: str, directory: str = directory, topics: list = topics
    ) -> None:
        super().__init__(level, directory, topics)
        self.system = system
        self.topics, self.commands = self.command_dictionary()

    def command_dictionary(self, system=system) -> tuple:
        commands = {}
        topics = []
        # Loop through the files
        p = Path(self.directory).glob('**/*')
        files = [x for x in p if x.is_file()]
        for file_index, file in enumerate(files):
            """if file_index == 0:
            continue"""
            # Predefine a dictionary to hold task:key_press commands
            topic_commands = {}
            with open(file) as rfile:
                reader = csv.reader(rfile)
                # Loop over file
                for topic_index, row in enumerate(reader):
                    if topic_index == 0:
                        # Add topic to topics list
                        topics.append(row[0].lower())
                        continue
                    topic_commands[row[0]] = row[system].lower()
                commands[topics[file_index]] = topic_commands
                topic_commands = {}
        return topics, commands

    def get_shortcuts(self) -> None:
        """Gets CSV files from Android Developers for Android Studio shortcuts for Windows/Linux and Mac."""

        # https://stackoverflow.com/questions/10556048/how-to-extract-tables-from-websites-in-python
        url = "https://developer.android.com/studio/intro/keyboard-shortcuts"
        html = requests.get(url).content
        df_list = pd.read_html(html)
        # Get the last dataframe in the list since lists do not have a "to_csv" attribute
        df = df_list[-1]
        path_name = "shortcut_csvs/parent_shortcuts/"
        parent_file_name = "android_shortcuts00.csv"
        joined = PurePosixPath(path_name).joinpath(parent_file_name)
        df.to_csv(joined, index=False)
        with open(joined) as all_file:
            reader = csv.reader(all_file)
            # Predefine a list so that lines can be added to another CSV later
            commands = []
            # Using a file count so that it can be used when naming each separate file even though it is the same loop
            file_count = 0
            for values in reader:
                # https://stackoverflow.com/questions/37376516/check-if-multiple-variables-have-the-same-value The
                # tables are not separated when using pandas, but the tell to see where a separate topic is being
                # used is when it shows up in each column
                if all(v == values[0] for v in values):
                    with open(
                            f"shortcut_csvs/android_studio_shortcut_csvs/android_shortcuts{file_count:02}.csv",
                            "w",
                            newline=''
                    ) as wfile:
                        writer = csv.writer(wfile)
                        writer.writerows(commands)
                    # Reset list so that new topic does not have a repeat of commands from other topics
                    commands = []
                    file_count += 1
                commands.append(values)
            remove = Path("shortcut_csvs/android_studio_shortcut_csvs/android_shortcuts00.csv")
            remove.unlink()

    @property
    def system(self) -> int:
        return self._system

    @system.setter
    def system(self, system) -> None:
        system = system.lower()
        if system not in ["windows", "linux", "mac"]:
            raise InvalidChoiceError("Invalid system")
        match system:
            case "windows" | "linux":
                self._system = 1
            case "mac":
                self._system = 2