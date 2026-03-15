set -x
python3 -m venv venv
source venv/bin/activate
cd venv
cd bin
python $1
