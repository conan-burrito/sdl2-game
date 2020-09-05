import os


if not os.path.exists('_build'):
    os.makedirs('_build')

os.chdir('_build')
os.system('conan install ..')
os.system('conan build ..')
