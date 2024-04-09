# CITS3403 PROJECT - Music Recommendation and Review Board

## About

This website will be a request board where users can post music recommendations and then other users can reply with their own rating/review of the music. It would be similar to websites like [Rate Your Music](https://rateyourmusic.com/) and [Album of The Year](https://www.albumoftheyear.org/), but in the style of a user request board instead of a database that has singular pages for each album. Some potential features would be embedding music links from streaming services, having a dedicated rating element, users being able to like/dislike others posts, searching for posts, tags for artists/genres, user pages, and featured posts.

## Installation

The following software should be downloaded prior to installation
 * [Git](https://git-scm.com/downloads)
 * [Python - 3.12.0](https://www.python.org/downloads/)
 * An IDE - [Visual Studio Code](https://code.visualstudio.com/download) Recommended

#### 1. Check your Python version
In a terminal run:
 * `python` / `python3` to check your python version (can run `exit()`) to close python terminal
 * `python -m pip` or `pip` to confirm pip is funtioning
 * `python -m venv` to check python's inbuilt environment manager is functioning

#### 2. Clone the Repository
The simplest way to clone the repo is using VSCode, in the IDE on the "welcome" page there is an option to "Clone Git Repository",
Click it and then paste in the link for the repo: `https://github.com/bass64/cits3403project.git`, then you'll be prompted to sign into you github account.

#### 3. Create and Activate Your Virtual Environment with venv
 1. Run `python3 -m venv venv` in the terminal to create your virtual environment. 
 2. Activate your venv using `.\venv\Scripts\activate` for windows or with `source venv/bin/activate` if using a linux based command line - you will need to activate the environment whenever you plan to run code within the project.
 3. Install any packages in the virtual environment:
     * On initial setup dependancies can be installed from the `requirements.txt` file by executing `pip install -r requirements.txt` __within the virtual environment__ - `(venv)` should be visible in your command line
     * If another package needs to be installed use `pip install` as normal within the venv, then once any changes are made save them by updating the requirements.txt file using `pip freeze > requirements.txt`

#### 4. Run the Flask Application
Now that all the setup is completed you are ready to code and to run the application. This can be done with `flask run` in the terminal

## Group Members:

__Cooper Thompson__ (23621342) \
Email: 23621342@student.uwa.edu.au \
GitHub: bass64 

__Alexander Nichols__ (23411868) \
Email: 23411868@student.uwa.edu.au \
GitHub: torinn-64

__Sibi Moothedan__ (23615908) \
Email: 23615908@student.uwa.edu.au \
GitHub: sibi12325

__Daniel Le__ (23625105) \
Email: 23625105@student.uwa.edu.au \
GitHub: dhq-Le
