set -x
cd flask_app
python3 -m venv venv
source venv/bin/activate
cd venv
cd bin
python $1
