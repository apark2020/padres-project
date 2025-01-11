# Baseball Research App
This app allows the user to interact, filter, and visualize pitch data in a variety of different ways.

### Installation Steps:
1. Clone the repo ``git@github.com:apark2020/padres-project.git``
2. ``cd`` into the directory, and, while not a requirement, consider using a virtual environment to rid of unnecessary package conflicts.

```
python3 -m venv venv
source venv/bin/activate
```
3. Use the ``requirements.txt`` file (found in the root directory of the repo) to install all necessary Python packages.
```
pip install -r requirements.txt
```
4. ``cd`` into ``/client``, and run ``npm install`` to download all node packages/dependencies.
5. ``cd ..`` back to the root folder and run the flask app
```
python -m flask run
```
6. In a new terminal window, navigate to ``padres-project/client`` and run ``npm run autobuild``.

The web app should now run locally, and you should have full access to its contents.