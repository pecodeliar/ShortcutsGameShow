from ide import AndroidStudio, IntelliJ
import random
from pyfiglet import Figlet
from tabulate import tabulate
from exceptions import InvalidChoiceError, InvalidCommandLineUsageError
import sys
import argparse


def main() -> None:

    mode = None

    if len(sys.argv) == 1:
        welcome_message()
        ide = ask_user_ide().lower()
        level = ask_user_level()
        if ide == "android studio" or ide == "android":
            system = ask_user_system()
            mode = game_settings(ide, level, system)
        else:
            mode = game_settings(ide, level)
    else:
        parse_args()
        # Slicing away both the file name
        mode = command_line_ide(sys.argv[1:])
        welcome_message()

    try:
        rounds, questions = quiz_settings(mode.level)
        correct = 0

        while rounds > 0:
            topics_display(mode.topics)
            topic = input("Choose a topic: ").lower()

            if topic not in mode.topics:
                topic = random.choice(mode.topics)
                print(f"A random topic has been picked! It is: {topic}.")

            for _ in range(2):
                question, command = question_generator(
                    list(mode.commands[topic].items())
                )
                print(f"Answer for video demo: {command}")
                print(question)
                answer = input().lower().replace(" ", "").strip()
                if answer == command.strip():
                    print("You got it!")
                    correct += 1
                else:
                    print(f"Not quite. The answer was: {command}")
            rounds -= 1

        print(f"\nGame over! You got {correct}/{questions} correct.\n")
    except KeyboardInterrupt:
        print("\n")
        print("You have ended the game. Bye bye!\n")
        sys.exit()


def parse_args():
    """User has defined some command line arguments to start the game more quickly."""
    # https://stackoverflow.com/questions/18160078/how-do-you-write-tests-for-the-argparse-portion-of-a-python-module

    parser = argparse.ArgumentParser(
        description="Sets the game settings as quick start"
    )
    parser.add_argument(
        "ide", help="IDE to be quizzed on:  Android or IntelliJ", type=str
    )
    parser.add_argument(
        "level", help="Level for quiz that determines the amount of rounds. ", type=str
    )
    parser.add_argument(
        "-s",
        "--system",
        default=None,
        help="If using Android Studio, the operating system being used needs to be specified.",
    )

    args = parser.parse_args()

    try:
        if args.ide.lower() == "android" and args.system is None:
            raise InvalidCommandLineUsageError(
                "Usage for android: project.py [-s SYSTEM] ide level"
            )
    except InvalidCommandLineUsageError as e:
        print(e)
        sys.exit()

    return parser.parse_args()


def welcome_message() -> None:
    """Displays welcome message using ASCII art and gets IDE choice from user."""

    text = "Welcome to 'Are You Smarter than a Junior Developer?'!"
    figlet = Figlet()
    figlet.setFont(font="drpepper")
    print(figlet.renderText(text))


def command_line_ide(args: list):
    """Return instance object of IDE with information supplied by command line."""
    ide = ""

    if "android" in args:
        ide = args[2]
    elif "intellij" in args:
        ide = args[0]

    try:
        match ide:
            case "android":
                return AndroidStudio(args[3], args[1])
            case "intellij":
                return IntelliJ(args[1])
            case _:
                raise InvalidCommandLineUsageError("Not a valid IDE choice.")
    except InvalidCommandLineUsageError as e:
        print(e)
        sys.exit()


def game_settings(ide: str, level: str, system: str = "") -> AndroidStudio | IntelliJ:
    """
    Gets the mode of how the user would like to continue the game from parameters provided.
    Will return an instance of the class object of the chosen IDE.
    """

    match ide.lower():
        case "android studio" | "android":
            return AndroidStudio(level, system)
        case "intellij":
            return IntelliJ(level)


def ask_user_ide() -> str:
    """Ask user for settings when command line arguments are not provided."""

    while True:
        try:
            ide_choice = input(
                "Which of the following IDEs would you like to be tested on? Android Studio or IntelliJ? "
            )
            if ide_choice.lower() not in ["android studio", "intellij", "android"]:
                raise InvalidChoiceError("Not an IDE choice")
            return ide_choice
        except InvalidChoiceError as e:
            print(e)
            pass


def ask_user_level() -> str:

    while True:
        try:
            print(
                "There are three game levels. Junior which is one round, Senior which is three rounds and Executive "
                "which is five rounds. "
            )
            level = input("Please pick a level: ")
            if level.lower() not in ["junior", "senior", "executive"]:
                raise InvalidChoiceError("Invalid Level call from function")
            return level
        except InvalidChoiceError as e:
            print(e)
            pass


def ask_user_system() -> str:
    """Get and system from user because no command line argument was provided."""

    while True:
        try:
            system = input(
                "Which system would you like to be tested on? Windows, Mac or Linux? "
            )
            if system not in ["windows", "linux", "mac"]:
                raise InvalidChoiceError("Invalid system")
            return system
        except InvalidChoiceError as e:
            print(e)
            pass


def topics_display(topics) -> None:
    """Displays topics in a grid format."""

    topics_row = []
    # For every topic in list, add topic to row until 5, then print row and reset
    for i, topic in enumerate(topics):
        topics_row.append(topic.title())
        if i % 5 == 3:
            print(tabulate([topics_row], tablefmt="grid"))
            topics_row = []
    if len(topics_row) > 0:
        print(tabulate([topics_row], tablefmt="grid"))


def quiz_settings(level: str) -> tuple:
    match level.lower():
        case "junior":
            return 1, 2
        case "senior":
            return 2, 4
        case "executive":
            return 3, 6
        case _:
            raise InvalidChoiceError(
                "Invalid level. Please select junior, senior or executive."
            )


def question_generator(commands: list) -> tuple:
    """Returns a question and answer from given commands."""

    task, command = random.choice(commands)
    return f"What is the command for {task}?", command


if __name__ == "__main__":
    main()