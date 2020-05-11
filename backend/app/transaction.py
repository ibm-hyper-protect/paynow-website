"""This module will serve the api request."""
##############################################################################
# Copyright 2019 IBM Corp. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
##############################################################################

from config import DATABASE
from app import app
from bson.json_util import dumps
from flask import request, jsonify
import json
import ast
import imp


# Import the helpers module
helper_module = imp.load_source('*', './app/helpers.py')

# Select the database
db = DATABASE
# Select the collection
collection = db.transactions

@app.route("/")
@app.route("/api")
def get_initial_response():
    """Welcome message for the API."""
    # Message to the trandaction
    message = {
        'apiVersion': 'v1.0',
        'status': '200',
        'message': 'Welcome to the Disaster Funding API'
    }
    # Making the message looks good
    resp = jsonify(message)
    # Returning the object
    return resp


@app.route("/api/v1/transactions", methods=['POST'])
def create_transaction():
    """
       Function to create new transaction.
       """
    try:
        # Create new transaction
        print("Inside Post");
        try:
            print(json.dumps(request.get_json()))
            body = ast.literal_eval(json.dumps(request.get_json()))
            print(body)
        except:
            # Bad request as request body is not available
            return "", 400

        record_created = collection.insert(body)

        # Prepare the response
        if isinstance(record_created, list):
            # Return list of Id of the newly created item
            return jsonify([str(v) for v in record_created]), 201
        else:
            # Return Id of the newly created item
            return jsonify(str(record_created)), 201
    except:
        # Error while trying to create the resource
        # Add message for debugging purpose
        return "boop", 500

@app.route("/api/v1/transactions_summary", methods=['GET'])
def transaction_summary():
    """
       Function to summarize transactions.
       """
    try:
        # Summary of transaction (TODO: validate user input)
        agr = [ {'$group': {'_id': 1, 'contributors': { '$sum': 1}, 'contributions': { '$sum': '$contribution' } } } ]
        #agr = [ {'$group': {'_id': 1, 'contributions': { '$sum': '$contribution' } } } ]
        result = list(collection.aggregate(agr))

        print('Total Contributions {}'.format(result[0]['contributions']))
        print('Total Contributors {}'.format(result[0]['contributors']))

        #record_created = collection.aggregate([ { "$group": { "_id": "$name", total_contributions: { "$sum": "$contribution" } } } ] )
        #print(record_created)

        # Prepare the response
        if isinstance(result, list):
            # Return list of Id of the newly created item
            print("Result is a list")
            return jsonify([str(v) for v in result]), 201
        else:
            # Return Id of the newly created item
            return jsonify(str(result)), 201
    except:
        # Error while trying to create the resource
        # Add message for debugging purpose
        return "", 500

@app.route("/api/v1/transactions_summary/<event>", methods=['GET'])
def transaction_summary_byEvent(event):
    """
       Function to summarize transactions.
       """
    try:
        # Summary of transaction (TODO: validate user input)
        agr = [ {"$match": { 'fundraising_event' :event } }, {'$group': {'_id': 1, 'contributors': { '$sum': 1}, 'contributions': { '$sum': '$contribution' } } } ]
        #agr = [ {'$group': {'_id': 1, 'contributions': { '$sum': '$contribution' } } } ]
        result = list(collection.aggregate(agr))

        print('Total Contributions {}'.format(result[0]['contributions']))
        print('Total Contributors {}'.format(result[0]['contributors']))

        # Prepare the response
        if isinstance(result, list):
            # Return list of Id of the newly created item
            print("Result is a list")
            return jsonify([str(v) for v in result]), 201
        else:
            # Return Id of the newly created item
            return jsonify(str(result)), 201
    except:
        # Error while trying to create the resource
        # Add message for debugging purpose
        return "", 500

@app.route("/api/v1/transactions_by_location", methods=['GET'])
def transaction_by_location():
    """
       Function to summarize transactions.
       """
    try:
        # Summary of transaction (TODO: validate user input)
        agr = [ {'$group': {'_id': "$location", 'contributions': { '$sum': '$contribution' } } } ]
        #agr = [ {'$group': {'_id': 1, 'contributions': { '$sum': '$contribution' } } } ]
        result = list(collection.aggregate(agr))

        print('Total Contributions {}'.format(result[0]['contributions']))

        #record_created = collection.aggregate([ { "$group": { "_id": "$name", total_contributions: { "$sum": "$contribution" } } } ] )
        #print(record_created)

        # Prepare the response
        if isinstance(result, list):
            # Return list of Id of the newly created item
            print("Result is a list")
            return jsonify([str(v) for v in result]), 201
        else:
            # Return Id of the newly created item
            return jsonify(str(result)), 201
    except:
        # Error while trying to create the resource
        # Add message for debugging purpose
        return "", 500

#need to enable authentication to view all transactions
@app.route("/api/v1/transactions", methods=['GET'])
def fetch_transactions():
    """
       Function to fetch the transactions.
       """
    print(request.query_string)
    try:
        # Call the function to get the query params
        # Check if query_string is not empty
        if request.query_string:
            query_params = helper_module.parse_query_params(request.query_string)

            # Try to convert the value to int
            #query = {k: int(v) if isinstance(v, str) and v.isdigit() else v for k, v in query_params.items()}
            #query = dict((k, int(v)) for k, v in query_params.items())
            query = dict((str(k,'utf-8'), str(v,'utf-8')) for k, v in query_params.items())
            print(query)

            # Fetch all the record(s)
            records_fetched = collection.find(query)
            print(records_fetched)
            # Check if the records are found
            if records_fetched.count() > 0:
                # Prepare the response
                return dumps(records_fetched)
            else:
                # No records are found
                return "", 404

        # If dictionary is empty
        else:
            print("string is empty")
            # Return all the records as query string parameters are not available
            records_fetched = collection.find()
            print(records_fetched)
            if records_fetched.count()>0:
                # Prepare response if the transactions are found
                print(records_fetched)
                return dumps(records_fetched)
            else:
                # Return empty array if no transactions are found
                return jsonify([])
    except:
        # Error while trying to fetch the resource
        # Add message for debugging purpose
        return "", 500


#Should not be able to update transactions
#@app.route("/api/v1/transactions/<email>", methods=['POST'])
def update_transaction(email):
    """
       Function to update the transaction.
       """
    try:
        # Get the value which needs to be updated
        try:
            body = ast.literal_eval(json.dumps(request.get_json()))
        except:
            # Bad request as the request body is not available
            # Add message for debugging purpose
            return "", 400

        # Updating the transaction
        records_updated = collection.update_one({"email": email}, body)

        # Check if resource is updated
        if records_updated.modified_count > 0:
            # Prepare the response as resource is updated successfully
            return "", 200
        else:
            # Bad request as the resource is not available to update
            # Add message for debugging purpose
            return "", 404
    except:
        # Error while trying to update the resource
        # Add message for debugging purpose
        return "", 500


#Should not be able to delete transactions
#@app.route("/api/v1/transactions/<email>", methods=['DELETE'])
def remove_transaction(email):
    """
       Function to remove the transaction.
       """
    try:
        # Delete the transaction
        delete_transaction = collection.delete_one({"email": email})

        if delete_transaction.deleted_count > 0 :
            # Prepare the response
            return "", 204
        else:
            # Resource Not found
            return "", 404
    except:
        # Error while trying to delete the resource
        # Add message for debugging purpose
        return "", 500


@app.errorhandler(404)
def page_not_found(e):
    """Send message to the user with notFound 404 status."""
    # Message to the user
    message = {
        "err":
            {
                "msg": "This route is currently not supported. Please refer API documentation."
            }
    }
    # Making the message looks good
    resp = jsonify(message)
    # Sending OK response
    resp.status_code = 404
    # Returning the object
    return resp
