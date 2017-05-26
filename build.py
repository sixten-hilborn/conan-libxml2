from conan.packager import ConanMultiPackager
import platform


if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.add_common_builds(shared_option_name="libxml2:shared", pure_c=True)

    if platform.system() == "Darwin":
        filtered_builds = []
        for settings, options, env_vars, build_requires in builder.builds:
            # Some isues with OSx and x86 with iconv, I think it could be linking with the system iconv and fails to link.
            if settings["arch"] != "x86":
                filtered_builds.append([settings, options, env_vars, build_requires])
        builder.builds = filtered_builds

    if platform.system() == "Windows":
        filtered_builds = []
        for settings, options, env_vars, build_requires in builder.builds:
            print settings
            if settings["compiler"] != "Visual Studio" or options["libxml2:shared"] == True:
                filtered_builds.append([settings, options, env_vars, build_requires])
        builder.builds = filtered_builds

    builder.run()
