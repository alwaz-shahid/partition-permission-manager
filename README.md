# Partition Permission Manager for Linux

A simple Python CLI tool to manage partition permissions on Linux.

## Overview

This tool allows you to interactively manage permissions for mounted partitions on your Linux system. It lists the mounted partitions, displays their current permissions, and lets you change permissions according to your needs.

## Requirements

- Python 3.x
- Administrative privileges (use `sudo` to run the tool)

## Usage

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/partition-permission-manager.git
   cd partition-permission-manager


## Install the virtualenv tool (if not already installed)
```pip install virtualenv```

### Create a virtual environment named 'venv' (you can use a different name)
```virtualenv venv```

### Activate the virtual environment
```
source venv/bin/activate   # On Linux/macOS
venv\Scripts\activate      # On Windows (Command Prompt)
.\venv\Scripts\Activate    # On Windows (PowerShell)
```


### Install the required library:

```pip install -r requirements.txt```

Run the tool using sudo:

```sudo python main.py```

After you're done, deactivate the virtual environment:


```deactivate```   # On Linux/macOS
