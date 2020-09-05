from conans import ConanFile, CMake, tools

import os


class Recipe(ConanFile):
    name = 'sdl-game'
    version = '0.0.1'

    description = 'Simple SDL2 game recipe'
    settings = 'os', 'arch', 'compiler', 'build_type'

    generators = 'cmake'

    requires = [
        'SDL2/2.0.12@conan-burrito/stable'
    ]

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()


    def imports(self):
        # Copy generated Java sources
        if self.settings.os == 'Android':
            script_path = os.path.dirname(os.path.abspath(__file__))
            target = os.path.join(script_path, 'android', 'app', 'src', 'main', 'generated', 'java')
            source = os.path.join('share', 'java')
            if not os.path.exists(target):
                os.makedirs(target)

            self.copy('*.java', target, source)
