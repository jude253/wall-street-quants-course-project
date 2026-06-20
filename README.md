# wall-street-quants-course-project

This repo contains project code for a Wall Street Quants Course.  The 
aim of it is to find profitable crypto statistical arbitrage strategies
with a Sharpe Ratio of 2+ using techniques learned in the course.  Full
project description is in [ClassProject.md](./ClassProject.md).

It is still in progress currently, and in the end there will be a more
comprehensive doc outlining overall learnings and strategies.

The dependencies of this project are in the `pyproject.toml` a long with
useful build/development related scripts, and there is a convenience
script at `bin/build.sh` as well with easier to type syntax for common
build related tasks.

The code itself for the project is under `src/wall_street_quants_course_project`, and in progress analyses are at `src/wall_street_quants_course_project/analysis`.

The only tool requirement to run this project that is not downloaded by this project itself is the build tool recommended by offically by the Python Packaging Authority (PyPa): [Hatch](https://hatch.pypa.io/latest/). Everything else for this project is downloaded and installed using that build tool.


## Philosophy

My personal development/research philosophy is to try to make all my 
code/analyses as self-documenting and readable as well as encouraging
quick development/analysis feedback loops to be efficient with my time.
This means efficient with both writing the code and reading the code
later-- I want it to take very little cognitive effort and time to make
incremental updates to the project with minimal effort to get back up to
speed, so it can easily be a regular, low-effort routine.

For example, ideally after every development session, I will have some
new piece of code/analysis that is connected into the larger project
ecosystem of resources/references/examples/well-documented code where I
am able to make simple ties to it during my session, and in the
future (and after forgetting many specifics), and have an easy enough
time picking up where I left off before by following those links.  A
specific example of this philosophy in this repo is typing/validating 
Pandas DataFrames with Pandera in `models.py`.  This allows me to easily
document important notes about the DataFrame such as expected columns,
data types and link relevant additional information there, so if I forget
something about a particular dataframe, I can ctrl + click to the typing
of it and read more to get back up to speed easily.

### Development

This analysis in this project is done primarily with jupyter lab and the
command for this is in the `pyproject.toml` (it's not listed here as
there are more details there and it is subject to change over time).