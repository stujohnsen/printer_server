import flask, time, requests, sys
from flask import Flask, request, Response, make_response, abort, url_for, json, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy

from app import app


printer_id_dict = {
    '0' : {
        "X-Api-Key" : '6D31E17927814F3CB1DB8C1D89AE883A',
        "ip_address" : "http://155.97.12.120:5000"
        },#
    '1' : {
        "X-Api-Key" : 'octopi1key',
        "ip_address" : "http://155.97.12.121"
        },
    '2' : {
        "X-Api-Key" : '0200628F557F4FF8B6FE08697140284F',
        "ip_address" : "http://155.97.12.122"
        },
    '3' : {
        "X-Api-Key" : '55909A86E92C49B6BF8FBAB5C61726C3',
        "ip_address" : "http://155.97.12.123"
        },
    '4' : {
        "X-Api-Key" : 'octopi4apikey',
        "ip_address" : "http://155.97.12.124"
        },
    '5' : {
        "X-Api-Key" : 'C87CDC97239244C0BF2711B5103974C8',
        "ip_address" : "http://155.97.12.125"
        }
}


# migrate = Migrate(app, db)

@app.route('/printer', methods = ['POST'])

def parse_request():

    print request.form

    status_code = ''
    build_resp = {
        'status' : '',
        'message' : '',
        'payload' : {}
    }

    try:
        r = request.json
        printer_id = r['printer_id']
        commands_to_interpret = r['commands']

    #    print "c\n"

        if not printer_id:
            build_resp['status'] = 'error'
            build_resp['message'] = 'No printer ID given.'
            status_code = '400'
        elif printer_id not in printer_id_dict:
            build_resp['status'] = 'error'
            build_resp['message'] = 'Invalid printer ID: ' + printer_id + '.'
            status_code = '400'
        elif not commands_to_interpret:
            build_resp['status'] = 'error'
            build_resp['message'] = 'No request specified.'
        else:
            build_resp['status'] = 'ok'
            build_resp['message'] = 'Returning request from printer ' + printer_id + '.'
            status_code = '200'
            url = get_printer_address(printer_id)
            header = {'X-Api-Key' : get_printer_api_key(printer_id)}
            printer_received_dict = requests.get((url+"/api/printer"),headers=header).json()
            # print printer_received_dict
            job_received_dict = requests.get((url+"/api/job"),headers=header).json()
            # print commands_to_interpret
            for x in commands_to_interpret:
                build_resp['payload'].update({ x : get_info_from_command(x, printer_received_dict, job_received_dict) })
            #build_resp['payload'] = received
            status_code = '200'

    except ValueError, e:
        print "value error"
        #print "Error: Printer has Disconnected", sys.exc_info()[0]
        build_resp['status'] = 'Printer Error'
        build_resp['message'] = 'Error encountered while querying data from printer ' + printer_id + ': ' + str(e)
        status_code = '409'
    except TypeError, e:
        print "type error"
        build_resp['status'] = 'Type Error'
        build_resp['message'] = 'Error when parsing request: ' + str(e)
        status_code = '400'
    except requests.exceptions.ConnectionError, e:
        print "connection error"
        build_resp['status'] = 'Connection Error'
        build_resp['message'] = 'Error encountered while connecting to printer ' + printer_id + ': ' + str(e)
        status_code = '409'
    except LookupError, e:
        print "lookup error"
        build_resp['status'] = 'Command Error'
        build_resp['message'] = 'Invalid Command: ' + str(e)
        status_code = '400'

    response_str = json.dumps(build_resp, sort_keys=False)
    response = make_response(response_str, status_code)
    return response

def get_printer_api_key(printer_id):
    return printer_id_dict[printer_id]["X-Api-Key"]

def get_printer_address(printer_id):
    return printer_id_dict[printer_id]["ip_address"]

def get_info_from_command(command, printer_received_dict, job_received_dict):
    #print command + '\n'
    if command == 'job_name':
        return job_received_dict['job']['file']['name']
    elif command == 'time_remaining':
        return job_received_dict['progress']['printTimeLeft']
    elif command == 'progress':
        return job_received_dict['progress']
    elif command == 'bed_temp':
        return printer_received_dict['temperature']['bed']
    elif command == 'extruder_temps':
        result = printer_received_dict['temperature'].copy() # need to try this on a multiple-extruder printer.
        del result['bed']
        return result
    else:
        #print "failed on: " + command
        raise LookupError(command)