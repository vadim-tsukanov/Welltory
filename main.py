import json
import os
from jsonschema import Draft7Validator

events, schemas = [], []
events_names, schemas_names = [], []

cwd = os.getcwd()
try:
    for tmp1, tmp2, files in os.walk(cwd + os.sep + "event"):
        for file in files:
            with open(cwd + os.sep + "event" + os.sep + file) as f:
                events.append(json.load(f))
                events_names.append(file)
    for tmp1, tmp2, files in os.walk(cwd + os.sep + "schema"):
        for file in files:
            with open(cwd + os.sep + "schema" + os.sep + file) as f:
                schemas.append(json.load(f))
                schemas_names.append(file)
except IOError:
    print("Error while reading files, press Enter")
    input()
    quit()

with open(cwd + os.sep + 'log.txt', 'w') as f:
    for schema, schema_name in zip(schemas, schemas_names):
        v = Draft7Validator(schema)
        for event, event_name in zip(events, events_names):
            errors = sorted(v.iter_errors(event), key=lambda e: e.path)
            if len(errors) == 1:
                f.write('Error in file "' + event_name + '" when validating with schema "' +
                        schema_name + '":' + '\n')
            elif len(errors) > 1:
                f.write('Errors in file "' + event_name + '" when validating with schema "' +
                        schema_name + '":' + '\n')
            for error in errors:
                f.write(error.message)
                if 'required property' in error.message:
                    f.write(", but it's missing in the JSON-file." + '\n')
                elif 'not of type' in error.message:
                    f.write('. Use the correct data type in JSON-file.' + '\n')
                else:
                    f.write('\n')
            if len(errors) != 0:
                f.write('\n')
