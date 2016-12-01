# Must follow this first
# http://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html

import boto3
import os

def encrypt_data(key,data):
    encrypted = kms.encrypt(KeyId=key, Plaintext=data)
    print('Encrypted Text: ',encrypted['CiphertextBlob'])
    Encrpyted_Data = encrypted['CiphertextBlob']
    return Encrpyted_Data

def decrypt_data(encrypted_data):
    decrypted = kms.decrypt(CiphertextBlob=encrypted_data)
    print('Decrypted Text: ',decrypted['Plaintext'])


if __name__ == "__main__":
    try:
        kms = boto3.client('kms')
        boto_master_key_id = os.environ['AWSKMSKEYID']

        #I request a data key using the master key I created for boto
        data_key = kms.generate_data_key(KeyId=boto_master_key_id,KeySpec='AES_256') #I use the boto key's id
        Encrypted_Data_Key = data_key['CiphertextBlob']
        Plaintext_Data_Key = data_key['Plaintext']

        #KMS sends both Encrypted_Data_Key and Plaintext_Data_Key
        print('Encrypted Data Key: ', Encrypted_Data_Key)
        print('Plaintext Data Key: ', Plaintext_Data_Key)

        message = os.environ['MESSAGETOENCRYPT']

        #I encrypt my message using boto_master_key_id
        my_encrypted_data = encrypt_data(boto_master_key_id,message)

        #I decrypt my message using KMS
        decrypt_data(my_encrypted_data)
    except:
        raise
