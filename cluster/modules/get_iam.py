class GetIam():
    def get_iam_policy_json(session, cluster,iam_policy_arn):
        global iam_client, iam_policy, policyJson, newiam_policy
        iam_client = session.client('iam')
        iam_policy = iam_client.Policy(iam_policy_arn)
        policyJson = iam_policy.default_version.document
        return policyJson


        def update_iam_policy(iam_policy_arn):
            policyJson['Statement'].update(newPolicyJson)
            newiam_policy = client.create_policy_version(
               PolicyArn= iam_policy_arn,
               PolicyDocument= json.dumps(policyJson),
               SetAsDefault= True
            )
            return newiam_policy
            
