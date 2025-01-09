# devopsallstars-day02-notifications
Email/SMS serverless notification app that sends game info periodically throughout the day.
Full project breakdown by Ifeanyi Otuonye [here](https://youtu.be/09WfkKc0x_Q?si=7UpN56Ye6H3aTdny).
## Requirements

### IAM
- Configure roles/policies for Lambda/SNS/EventBridge

### SNS
- Create subscription topic

### Lambda
- API Call
    - Make api call to sportsdata.io
    - Manipulate data to a user-friendly format
- SNS
    - Publish message to SNS topic

### EventBridge
- Create cronjob to trigger Lambda function
