# Are You Smarter than a Junior Developer?

#### Video Demo:  https://youtu.be/xA8oOBV6XGU

## Language and IDE Used
<p align="center">
    <img src="https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge"> <img src="https://img.shields.io/badge/Visual_Studio_Code-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white" alt="VSCode Badge">
</p>

## Table of Contents
1. [Packages Used](#packages-used)
2. [Overview](#overview)
3. [Installation](#installation)
4. [Game Customization](#game-customization)
5. [Game Start](#game-start)
    - [No Additional Command Line Arguments](#no-additional-command-line-arguments)
    - [With Additional Command Line Arguments](#with-additional-command-line-arguments)

## Overview

This project is a play on the American game show, [Are You Smarter than a 5th Grader?](https://en.wikipedia.org/wiki/Are_You_Smarter_than_a_5th_Grader%3F) My desire for making this project was to gameify learning IDE shortcuts so that I stop relying on the GUI ~~or Google~~ and get faster by using keyboard shortcuts instead. This project for now is incomplete as I would like to be able to have the users use the actual shortcuts rather than having to type what the shortcut is.

## Packages Used

| Package                                           | Use for Project                                                                     |
|---------------------------------------------------|-------------------------------------------------------------------------------------|
| [pandas](https://pandas.pydata.org/)              | Helped with converting documented shortcuts for IDEs to CSV files                   |
| [lxml](https://lxml.de/)                          | A support for pandas when process the HTML of the IDE doc websites                  |
| [tabulate](https://pypi.org/project/tabulate/)    | Displays topics that are generated in a game show sign-like manner.                 |
| [figlet](http://www.figlet.org/)                  | Displays a graphic for the start of the game (program).                             |
| [black](https://black.readthedocs.io/en/stable/#) | Formatted the code for better readability and adherence to pythonic code structure. |
| [pytest](https://docs.pytest.org/en/7.2.x/)       | Unit testing in ```test_project.py```.                                              |

## Installation

If you would still like to install, follow the below steps:
1. Click the **Code** button.
2. Once you see a menu popup, click the **Download Zip** button. This will save the project to your computer.
3. Once the download is complete, find the file and unzip the content (you can do this by double-clicking or right-clicking and pressing Extract Files).

## Game Customization

You can customize the game to your liking in the ```project.py``` file. Go to the game settings function that should look like the below:

```python
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
```
- The first integer in the tuple represent how many times you would be prompted to pick a topic (rounds).
 - The second integer in the represents how many questions you would be asked in total.

 For example, with the senior round, you would be asked a total of 4 questions. Questions are divided by round so in this case, you would have 2 questions per round since 4 / 2 = 2.

 *Make sure you save your file changes!*

## Game Start

First you must have the packages in ```requirements.txt``` installed first. You can then run the file either with no additional command line arguments or do a quick start with command line arguments.

### __No Additional Command Line Arguments__
Run ```python project.py``` in your terminal. You will then be prompted with questions to help set the settings for the game.

### __With Additional Command Line Arguments__
You must know your IDE and level beforehand.

IDEs:
- Android Studio
- IntelliJ

Levels:
- Junior
- Senior
- Executive

***IntelliJ Quick Start Example***
```
python project.py intellij executive
```

***Android Quick Start Example***

If you are using Android, you must also know the operating system as well and then must be your first argument, following the use of ```-s``` or ```-system```. After the IDE, you must put only ```android```. **Do not include studio**. Then your level of choice.

Operating systems:
- Mac
- Windows
- Linux

```
python project.py -s linux android junior
```