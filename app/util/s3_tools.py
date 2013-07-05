import json
import boto

from boto.s3.key import Key 


def store_file(bucket, filename, payload):
    """adds a file to a specified S3 bucket
        
    :params bucket: destination bucket
    :params filename: desired filename
    :params payload: contents of file

    :returns: boolean of success or failure
    """ 

    # instansiate connection with S3
    try:
        connection = boto.connect_s3()
    except NoAuthHandlerFound:
        print 'Authorization error, check your /etc/boto.cfg or ~/.boto'
        return False

    # grab the desired bucket
    bucket = connection.get_bucket(bucket)
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
