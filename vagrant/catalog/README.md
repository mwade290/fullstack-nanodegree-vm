# Item Catalog Project

Displays a catalog of country highlights using Flask and SQLAlchemy in Python.

# Install

Python (v3.5+)

Python libraries (see pg_config.sh)

VirtualBox (https://www.virtualbox.org/)

Vagrant (https://www.vagrantup.com/)

Flask (http://flask.pocoo.org/)

# Usage

## How to run the code
1. In a bash terminal, cd into the "/vagrant/catalog" directory on your local machine
2. Type "vagrant up"
3. Type "vagrant ssh"
4. cd into "/vagrant/catalog" again (this is the virtual directory)
5. On first startup, run "python database_setup.py" followed by "python populate_database.py"
6. Run "python application.py" (this starts the server)
7. Open a web browser and navigate to "http://localhost:8000"
