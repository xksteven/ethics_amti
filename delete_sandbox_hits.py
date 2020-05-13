import boto3
from datetime import datetime

#aws_access_key_id = AKIA333YAU62YPA7EBN4
#aws_secret_access_key = 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

# Get the MTurk client
mturk=boto3.client('mturk',
        aws_access_key_id="AKIA333YAU62YPA7EBN4",
        aws_secret_access_key="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",
        region_name='us-east-1',
        endpoint_url="https://mturk-requester-sandbox.us-east-1.amazonaws.com",
        #endpoint_url="https://mturk-requester.us-east-1.amazonaws.com",
    )

# Delete HITs
#for item in mturk.list_hits()['HITs']:
for item in mturk.list_hits_for_qualification_type(
        QualificationTypeId="3YCLOEER7R8VN46A6TMH6U0503ROBY")['HITs']:
    hit_id=item['HITId']
    print('HITId:', hit_id)

    # Get HIT status
    status=mturk.get_hit(HITId=hit_id)['HIT']['HITStatus']
    print('HITStatus:', status)

    # If HIT is active then set it to expire immediately
    if status=='Assignable':
        response = mturk.update_expiration_for_hit(
            HITId=hit_id,
            ExpireAt=datetime(2015, 1, 1)
        )        

    # Get a list of the Assignments that have been submitted
    assignmentsList = mturk.list_assignments_for_hit(
        HITId=hit_id,
        AssignmentStatuses=['Submitted', 'Approved'],
        MaxResults=10
    )
    assignments = assignmentsList['Assignments']
    item['assignments_submitted_count'] = len(assignments)
    answers = []
    print(assignments)
    #for assignment in assignments:
    #
    #    # Retreive the attributes for each Assignment
    #    worker_id = assignment['WorkerId']
    #    assignment_id = assignment['AssignmentId']
    #    try:
    #        response = mturk.approve_assignment(
    #                AssignmentId=assignment_id,
    #                   RequesterFeedback='string',
    #                   OverrideRejection=True,
    #                        )
    #    except:
    #        print("didn't approve")
    #        pass

    ## Delete the HIT
    #try:
    #    mturk.delete_hit(HITId=hit_id)
    #except:
    #    print('Not deleted')
    #else:
    #    print('Deleted')
