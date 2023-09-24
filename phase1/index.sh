rm -rf "$2"
mkdir "$2"
python3 dataReader.py "$1" "$2" "$3"
