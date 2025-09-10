# File Organize Tool

## Description
File Organize Tool is a Python CLI application for managing tasks and basic file operations. The program allows you to add, view, edit, and delete tasks, sort files by type or modification date, read text and binary files, and delete files or directories. Tasks are persistently stored in a binary file `tasks.bin`, and all user actions are logged in `app.log` and displayed in the console with colored logging levels.

## Features
- Add new tasks with a title, creation timestamp, and initial status "in progress".
- View all tasks with ID, title, creation date, and status.
- Edit task title or status ("in progress", "done", "paused").
- Delete tasks with automatic sequential renumbering.
- Sort files in a directory by type or date.
- Read text, log, or binary files.
- Delete files or directories (with optional recursive deletion).
- Input validation to prevent duplicates or empty tasks.
- Modular code structure for reusability.

## Project Structure
- `main.py` — main entry point with CLI menu.
- `app/organize/organize.py` — task management (CRUD operations).
- `app/file_parse/file_parse.py` — file and folder operations.
- `app/logs/logger.py` — logging configuration.
- `utils/helpers.py` — helper functions (input validation, menu selection).
- `app/organize/tasks.bin` — binary file storing tasks.
- `app/logs/app.log` — log file.

## Installation
1. Clone the repository: `git clone https://github.com/ProstoMishutka/file-organize-tool.git`
2. Run the program: `python main.py`

## Usage Example
- Adding a task: `Enter the description of your task: Buy groceries` → `Task added successfully: Buy groceries.`
- Viewing tasks:  
`Task 1:`  
`  Title       : Buy groceries`  
`  Created at  : 2025-09-10 21:00:00`  
`  Status      : in progress`
- Editing a task: `Enter the number of the task you want to edit: 1` → `Enter the new title of the task: Buy groceries and drinks` → `Task successfully updated.`

## Logging
- All user actions are logged in `app.log`.

## Supported OS
- Windows  
- Linux  
- macOS

## Requirements
- Python 3.10+  

## Author
Misha Patserkovskyi
