python3 update_version.py

pip3 install setuptools wheel
python3 setup.py sdist bdist_wheel

pip3 install twine

# shellcheck disable=SC2162
read -p "Enter username: " user
# shellcheck disable=SC2162
read -p "Enter password: " pass

twine upload --repository pypi dist/* -u "${user}" -p "${pass}"

rm -rf build dist MacroRecorder.egg-info