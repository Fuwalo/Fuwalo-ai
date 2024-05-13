from datetime import timedelta
import traceback
# For exceptions
from couchbase.exceptions import CouchbaseException
# Required for any cluster connection
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
# Required for options -- cluster, timeout, SQL++ (N1QL) query, etc.
from couchbase.options import ClusterOptions
import uuid

def generate_random_id():
    """
    Generate a random UUID (Universally Unique Identifier).

    Returns:
        str: Random UUID.
    """
    return str(uuid.uuid4())


endpoint = "couchbases://cb.kgwdsceo9opxyqm.cloud.couchbase.com" # Replace this with Connection String
username = "the4strange@gmail.com" # Replace this with username from database access credentials
password = "Fuwalo2004@" # Replace this with password from database access credentials
bucket_name = "travel-sample"
scope_name = "_default"
collection_name = "midi_data"
# Sample airline document

# Key will equal: "airline_8091"
# User Input ends here.
# Connect options - authentication
auth = PasswordAuthenticator(username, password)
# Get a reference to our cluster
options = ClusterOptions(auth)
# Use the pre-configured profile below to avoid latency issues with your connection.
options.apply_profile("wan_development")
try:
	cluster = Cluster(endpoint, options)
	# Wait until the cluster is ready for use.
	cluster.wait_until_ready(timedelta(seconds=5))
	# Get a reference to our bucket
	cb = cluster.bucket(bucket_name)
	# Get a reference to our collection
	cb_coll = cb.scope(scope_name).collection(collection_name)
except Exception as e:
  traceback.print_exc()
	# Simple K-V operation - to create a document with specific ID
def savemidi(result):
      try:
        key = generate_random_id()
        print("Random ID:", key)
        result = cb_coll.insert(key, result)
        print("\nCreate document success. CAS: ", result.cas)
      except CouchbaseException as e:
        print(e)
      except Exception as e:
        traceback.print_exc()
