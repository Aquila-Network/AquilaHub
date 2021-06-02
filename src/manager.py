import logging

import fasttext
from utils import downloader
import hashlib
import base58
import json

import os

# Maintain a model directory
data_dir = os.environ["DATA_STORE_LOCATION"]
model_dir = data_dir + "models/"
model_dict = None
hash_dict = None

def write_json_file (file, data):
    with open(file, 'w') as outfile:
        json.dump(data, outfile)

def read_json_file (file):
    with open(file) as json_file:
        return json.load(json_file)

def get_url (schema):
    """
    Get model url from a schema
    """
    
    if schema.get("encoder") != None:
        return schema["encoder"]
    else:
        return None

def get_url_hash (url):
    hash_ = hashlib.sha256(url.encode('utf-8'))
    b58c_ = base58.b58encode(hash_.digest())
    return b58c_.decode('utf-8')

def download_model (url, directory, file_name):
    """
    Download a model from a URL
    """

    # cleanup url - get rid of `ftxt:` in the beginning
    if url.split(":")[0] == "ftxt":
        url = ":".join(url.split(":")[1:])
    
        if url.split(":")[0] == "http" or url.split(":")[0] == "https":
            return downloader.http_download(url, directory, file_name)

        elif url.split(":")[0] == "ipfs":
            return downloader.ipfs_download(url, directory, file_name)
    else:
        logging.error("Invalid encoder URL. Follow this format 'ftxt:<http | ipfs>://<LOCATION | IPFS CID>' ")
        return None

def memload_model (model_filename):
    """
    Load a model from disk
    """

    if model_filename:
        logging.debug("loading model into memory..")
        return fasttext.load_model(model_filename)
    else:
        return None

def preload_model (database_name, json_schema):
    """
    Download a model and load it into memory
    """

    # prefill model & hash dictionary
    global model_dict
    global hash_dict
    if model_dict == None or hash_dict == None:
        try:
            model_dict = read_json_file(data_dir + 'hub_model_dict.json')
            hash_dict = read_json_file(data_dir + 'hub_hash_dict.json')
        except Exception as e:
            logging.error("model & hash dict json read error")
            logging.error(e)
            model_dict = {}
            hash_dict = {}
    
    try:
        # keep reference to model hash from database (DB - hash map)
        if not hash_dict.get(database_name):
            hash_dict[database_name] = get_url_hash(get_url(json_schema))

        # keep reference to model memory from hash (hash - mem model map)
        if not model_dict.get(hash_dict[database_name]):
            model_dict[hash_dict[database_name]] = memload_model(download_model(get_url(json_schema), model_dir, database_name))
            if model_dict[hash_dict[database_name]]:
                logging.debug("Model loaded for database: "+database_name)

                # persist to disk
                try:
                    write_json_file(data_dir + 'hub_model_dict.json', model_dict)
                    write_json_file(data_dir + 'hub_hash_dict.json', hash_dict)
                except Exception as e:
                    logging.error("model & hash dict json write error")
                    logging.error(e)
                return True
            else:
                logging.error("Model loading failed for database: "+database_name)
                # reser DB - hash map
                hash_dict[database_name] = None
                return False
    except Exception as e:
        logging.error(e)
        return False

def compress_data (database_name, texts):
    """
    Load an already existing database 
    """

    # prefill model & hash dictionary
    global model_dict
    global hash_dict
    if model_dict == None or hash_dict == None:
        try:
            model_dict = read_json_file(data_dir + 'hub_model_dict.json')
            hash_dict = read_json_file(data_dir + 'hub_hash_dict.json')
        except Exception as e:
            logging.error("model & hash dict json read error")
            logging.error(e)
            model_dict = {}
            hash_dict = {}

    if not hash_dict.get(database_name):
        logging.error("Model not pre-loaded for database: "+database_name)
        return []
    if not model_dict.get(hash_dict[database_name]):
        logging.error("Model not mem-loaded for database: "+database_name)
        return []
    
    result = []
    try:
        for text in texts:
            result.append(model_dict[hash_dict[database_name]].get_sentence_vector(text).tolist())

        return result
    except Exception as e:
        logging.error(e)
        logging.error("Model prediction error for database: "+database_name)
        return []
