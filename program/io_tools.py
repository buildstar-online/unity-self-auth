import os                       # system file paths
import json                     # json formatting
import dictor                   # json formatting
import shutil                   # deletes directories
import subprocess               # system commands
from logging import debug       # json data
from datetime import datetime   # timestamps
from deepdiff import DeepDiff   # pip3 install deepdiff
from pygments import highlight  # tools for colorizing the json output
from pygments.lexers.web import JsonLexer                          # tools for colorizing the json output
from pygments.formatters.terminal import TerminalFormatter         # tools for colorizing the json output

def get_timestamp():                                               # returns a timestamp in DD:MMM:YYYY (HH:MM:SS.f) format
    now = datetime.now()
    timestamp = now.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    return timestamp

def read_file(path: str):                                          # reads json file from <path>: returns <json object>
    print_pretty("trying to read: " + path)
    try:
        with open(path, 'r', encoding='utf-8') as cache_file:
            raw = cache_file.read()
            data = json.loads(raw)
            print_pretty("successfully read: " + path)
    except:
        print_pretty("failed to read: " + path, False)
        print_pretty("deleting " + path, False)
        os.remove(path)
        data = False

    return data

def azure_auto_install():                                          # attempts to force azure cli to auto-install cost management module

    data = subprocess.run([
    'az','config',
    'set','extension.use_dynamic_install=yes_without_prompt'
    ], capture_output=True)

    #print(data.stdout)
    print(data.stderr)

def print_pretty(data, debug: bool = False):                       # prettified json console output: returns <string>
    # Generate JSON
    json_data = {}
    try:
        json_data = validate_json_object(data)
    except:
        try:
            json_data = validate_json_file(data)
        except:
            if debug:
                name = input("Any key to continue")

    if json_data['readable'] != False:
        try:
            colorize_json(json_data['path'], debug)
        except:
            print(f"Well shit, i cant parse this: {json_data}")
            if debug:
                name = input("Any key to continue")

def colorize_json(json_data, debug):                               # prints colorful json
    # Colorize it
    colorful = highlight(
        json_data,
        lexer=JsonLexer(),
        formatter=TerminalFormatter(),
    )

    if debug == True:
        print(colorful)
    else:
        log = {}
        log['time'] = get_timestamp()
        log['data'] = colorful
        (log, True)

def validate_json_file(path: str, debug=False):                    # takes a <file_path>, returns query{dict(<string>,<string>)}
    query = {}
    query['path'] = path
    if read_file(path) == False:
        query['readable'] = False
    else:
        query['readable'] = True
        print_pretty("file is valid json :" + path, debug)

    return query

def validate_json_object(object, debug=False):                     # takes a <file_path>, returns query{dict(<string>,<string>)}
    query = {}
    try:
        # is it already json?
        is_json = json.loads(object)
        query['readable'] = True
        query['path'] = object
    except:
        try:
            # can I make it json?
            raw_json = json.dumps(object, indent='\t', separators=(',', ': '), sort_keys=True, skipkeys=True)
            query['readable'] = True
            query['path'] = raw_json
        except:
            # not json :(
            print_pretty("NOT A VALID JSON OBJECT", debug)
            query['readable'] = False
            if debug:
                name = input("Any key to continue")

    return query

def write_file(path: str, payload: str, debug = False):            # attempt to save <payload> to disk at <path> as json file
    if not os.path.isfile(path):
        try:
            print_pretty("trying to write file: " + path, debug)
            with open(path, "w", encoding='utf-8') as save_file:
                save_file.write(json.dumps(payload, indent=4, sort_keys=True))
        except:
            print_pretty("failed to save: " + path, debug)
            if debug:
                name = input("Any key to continue")
    else:
        try:
            print_pretty("####################################################################################################", debug)
            print_pretty("# " + path, debug)
            print_pretty("# file already exists. " + path, debug)
            print_pretty("# if you dont want to delete the contents of the file on write, use the update_file() function", debug)
            print_pretty("# clearing file... " + path, debug)
            print_pretty("####################################################################################################", debug)
            os.remove(path)
            write_file(path, payload, debug)
        except:
            print_pretty("failed to save: " + path, debug)
            if debug:
                name = input("Any key to continue")

    validate_json_file(path, debug)

def update_file(path: str, payload: str, debug = False):           # update an existing file on disk
    if os.path.isfile(path):
        try:
            print_pretty("trying to update file: " + path, debug)
            with open(path, "a+", encoding='utf-8') as save_file:
                save_file.write(json.dumps(payload, indent=4, sort_keys=True))
        except:
            print_pretty("failed to update: " + path, debug)
    else:
        write_file(path, payload, debug)

    validate_json_file(path, debug)

def make_dir(path: str, clear: bool = False, debug: bool = False): # makes/deletes directory
    if not os.path.isdir(path):
        print_pretty('directory is not present. Creating ' + path, debug)
        try:
            os.makedirs(path)
        except:
            print_pretty("unable to create dir at " + path, debug)
            if debug:
                name = input("Any key to continue")
    else:
        if not clear:
            print_pretty('directory is present. ' + path, debug)
        else:
            print_pretty('directory is present. ' + path)
            print_pretty('clearing...', debug)
            try:
                shutil.rmtree(path)
                os.makedirs(path)
            except:
                print_pretty("failed to clear directory. " + path)
                if debug:
                    name = input("Any key to continue")

class Datastore(dict):                                             # datastore class object for extensibility
     def __setitem__(self, key, value):
        super().__setitem__(key, value)

class Variables(object):                                           # variables class object provides an abstraction for state observation w/ a cache

    def __init__(self, settings, debug=False, go_steppy=False):  # reconstrusts the json object as a dict

        self.change_value("debug", debug, debug)
        self.change_value("go_steppy", go_steppy, debug)

        for section in settings:
            if len(section) == 1:
                key = section
                value = settings[section]
                self.change_value(key, value, debug)
            else:
                key = section
                value = {}
                for item in settings[section]:
                    value[item] = settings[section][item]

                self.change_value(key, value, debug)

    def change_value(self, key, value, debug=False):  # changes the value of settings and logs the change using deepdiff
        diff = self.diff_values(key, value, debug)
        print_pretty(f"Diff for {key}:", debug)
        print_pretty(f"{self.get_current_value(key, value)} ==> {value}", debug)
        print_pretty(diff, debug)

        if "go_steppy" in self.settings:
            if self.settings['go_steppy']:
                name = input("Any key to continue")

        self.settings[key] = value

    def get_current_value(self, key, value, debug=False): # returns the current value of a key
        current_value = None

        for section in self.settings:
            if section == key:
                current_value = self.settings[section]
            for item in section:
                if item == key:
                    current_value = self.settings[section][item]

        return current_value

    def diff_values(self, key, value, debug=False): # returns a diff between current and proposed state
        #try to find the current value if it exists
        #opitmization needed
        current_value = self.get_current_value(key, value, debug)

        # actually do the diff
        try:
            data = DeepDiff(current_value, value).to_json(indent='\t', separators=(',', ': '), sort_keys=True, skipkeys=True)
        except:
            data = "Unable to diff"

        return data

    @property
    def settings(self):
      return (self.__dict__)

    @settings.setter
    def settings(self, settings):
        self.settings = settings
