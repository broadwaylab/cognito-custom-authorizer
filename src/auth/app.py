import json
import requests
import os

def generate_policy_document(effect, method_arn):
	if effect == None or method_arn == None:
		return None

	policy_document = {
		'Version': '2012-10-17',
		'Statement': [{
			'Action': ['execute-api:Invoke'],
			'Effect': effect,
			'Resource': method_arn
		}]
	}

	print("Policy Document:")
	print(policy_document)
	return policy_document

def generate_auth_response(principal_id, effect, method_arn):
	policy_document = generate_policy_document(effect, method_arn)
	return {
		"principalId": principal_id,
		"policyDocument": policy_document
	}
	return policy_document


def lambda_handler(event, context):
	print(event)
	arn = event['methodArn']
	
	auth_token = event['headers']['Authorization']

	# Make make request to reviewpush endpoint
	response = requests.get(os.environ['AUTH_URL'], headers={'Authorization': auth_token})
	print(response)
	print(response.text)

	if response.status_code == 200:
		return generate_auth_response('user', 'Allow', arn)
	else:
		return generate_auth_response('user', 'Deny', arn)