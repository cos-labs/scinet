import json
import boto

from boto.s3.key import Key 

def _connect():
    """connects to s3 DB"""
    try:
        connection = boto.connect_s3()
        return connection
    except NoAuthHandlerFound:
        print 'Authorization error, check yout /etc/boto.cfg or ~/.boto'

def store_file(desired_bucket, filename, payload):
    """adds a file to a specified S3 bucket
        
    :param bucket: destination bucket
    :param filename: desired filename
    :param payload: contents of file

    :return: boolean of success or failure
    """ 
    # instansiate connection with S3
    connection = _connect()

    # grab the desired bucket
    bucket = connection.get_bucket(desired_bucket)
    if bucket is None:
        print 'Bucket does not exist'
        return False

    # create a new key for the bucket
    k = Key(bucket)
    # set the filename
    k.key = filename
    # set the contents of the file
    k.set_contents_from_string(json.dumps(payload, indent=4))

    # return True for acknowledgement
    # @todo: implement try/catches and think of a better return type
    return True

def get_file(bucket, filename):
    """retrieves and returns an s3 key

    :param bucket: bucket file is in
    :param filename: key file is stored in

    :return: key instance
    """
    connection = boto.connect_s3()
    
    # @todo: factor our
    bucket = connection.get_bucket(bucket)
    if bucket is None:
        print 'Bucket does not exist'
        return False

    # check if key is in bucket
    for key in bucket.list():
        if key.key == filename:
            return key
    
    # return None if no key was found
    return None
