#!/usr/local/bin/python3

import argparse
import urllib.request
import urllib.error
import json
import os

def writeJSON(data, filename):
    try:
        with open(file=os.path.abspath(path=filename), mode="w") as jsonFile:
            json.dump(obj=data, fp=jsonFile, indent=4)
        print(f'Wrote json file {filename}')
    except IOError as e:
        print(f'Error while writing JSON file: {e}')
    
def callApi(apiUrl, apiKey):
    try:
        head = { 'Content-Type': 'application/vnd.api+json', 'Authorization': f"ApiKey {apiKey}" }
        req = urllib.request.Request(apiUrl, headers=head, method='GET')

        print(f'''\n\n
Querying the Cloud One Conformity API.\n
    Api:\t{req.full_url}
    Method:\t{req.method}\n\n''')

        with urllib.request.urlopen(req) as response:
            responseData = response.read()
            data = json.loads(responseData)
            return data
    except urllib.error.HTTPError as e:
        error = json.loads(e.read())
        print(f'''
\n\nHTTP error code:\t{e.code}\n
{json.dumps(error, indent=4)}\n\n
''')
        raise e
    except urllib.error.URLError as e:
        print(f'\n\nCould not reach the API: {e.reason}\n\n')
        raise e
    except json.JSONDecodeError as e:
        print(f'''
\n\nError while parsing API response.\n
Line:\t{e.lineno}
Column:\t{e.colno}
Message:\t{e.msg}
Response:\n{e.doc}\n\n''')
        raise e
    except Exception as e:
        print(f'An error occurred: {e.reason}')
        raise e
    
parser = argparse.ArgumentParser(
    description='''
get-services
Queries the services API and stores the results in a file.
See the API documentation for more details at https://cloudone.trendmicro.com/docs/conformity/api-reference/tag/Services
Use the -h or --help switch for running this command.
''')
parser.add_argument('--region', type=str, required=True, choices=[
                    'us-1', 'in-1', 'gb-1', 'jp-1', 'de-1', 'au-1', 'ca-1', 'sg-1', 'trend-us-1'], help='Cloud One Service Region')
parser.add_argument('--apiKey', type=str, required=True,
                    help='Cloud One API Key with administration rights')
parser.add_argument('--filename', type=str, required=True, help='Name the file that will be created')
args = parser.parse_args()

conformityEndpoint = f"https://conformity.{args.region}.cloudone.trendmicro.com/api/services"

response = callApi(apiUrl=conformityEndpoint, apiKey=args.apiKey)

writeJSON(data=response, filename=args.filename)
