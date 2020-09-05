import os


if not os.path.exists('_build-emulator'):
    os.makedirs('_build-emulator')

os.chdir('_build-emulator')
os.system('conan install .. -pr ../profiles/ios/emulator')
os.system('CONAN_CMAKE_GENERATOR=Xcode conan build ..')
