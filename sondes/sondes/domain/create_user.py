from typing import Dict


def create_user(user_model: Dict) -> Dict:

    user_json = {
        "auditHeader": None,
        "proposedSnapshot": {
            "com.linkedin.pegasus2avro.metadata.snapshot.CorpUserSnapshot": {
                "urn": "urn:li:corpuser:jcvd",
                "aspects": [
                    {
                        "com.linkedin.pegasus2avro.identity.CorpUserInfo": {
                            "active": True,
                            "displayName": {
                                "string": user_model['first_name'] + ' ' + user_model['last_name']
                            },
                            "email": "jcvd@jcvd.jcvd",
                            "title": {
                                "string": "who knows?"
                            },
                            "managerUrn": None,
                            "departmentId": user_model['departmentId'],
                            "departmentName": "Exploration Production",
                            "firstName": user_model['first_name'],
                            "lastName": user_model['last_name'],
                            "fullName": {
                                "string": user_model['first_name'] + ' ' + user_model['last_name']
                            },
                            "countryCode": "BE"
                        }
                    }
                ]
            }
        },
        "proposedDelta": None
    }

    return user_json
