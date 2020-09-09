# Code
This sub directory includes all the code and libraries that were built or extended as part of my MSc project. This includes the robots / TOS parser, the OpenWPM cookie banner extension and all the sanitisation / normalisation scripts. 

## Framework
The project does not rely on a particular framework (such as Django). However, it is primarily written in Python 3 and therefore, knowledge of that is required for anyone to understand and extend this project.

## Installation
Firstly, install OpenWPM and its dependencies. You can `cd OpenWPM` and follow the installation instructions on their [page](https://github.com/mozilla/OpenWPM).

Install the dependencies on the `msc_cookies_env.yaml`. If you are using Conda then use that environment and you are ready to go. 

That's about it! You can run each script by simply running the Python command as such:

```sh
python3 step0a_create_db.py
```

Look at each script for its parameter list (e.g if you want to change the output directory)

![](https://media.giphy.com/media/ny7UCd6JETnmE/giphy.gif)