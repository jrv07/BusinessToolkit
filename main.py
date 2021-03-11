import argparse
import yaml
import extra_functions as fun
from Configuration import Configuration
from module_misc.ConfigurationOptions import ConfigurationOptions


def parse_settings(filename):
    with open(filename, 'r') as f:
        content = f.read() + "\n"
    return yaml.load(content, Loader=yaml.FullLoader)


def main():
    fun.setup_logger()
    parser = argparse.ArgumentParser()
    parser.add_argument('settings', help='analysis settings file')
    args = parser.parse_args()
    settings = parse_settings(args.settings)
    options = ConfigurationOptions()
    fun.create_directories()
    fun.read_current_system()

    config = Configuration(settings, options=options)
    config.generate()


if __name__ == "__main__":
    main()
