#Embedded file name: I:/bag/tmp/tw2/res/entities\common/pg_protect.o
import hashlib
BLOCK_SIZE = 131072

def VerifyMd5(encrypted_md5_bin):
    """
    VerifyMd5(encrypted_md5_bin) check if the encrypted md5 data is valid
    
    :param encrypted_md5_bin:   encrypted md5 data
    :returns:                   plain text md5 on success, None on error
    """
    try:
        lines = encrypted_md5_bin.split('\n')
        line_count = int(lines[0], 10)
        body = '\n'.join(lines[0:line_count + 1])
        md5 = hashlib.md5()
        md5.update(body + '\n')
        check = md5.hexdigest()
        if check == lines[-1]:
            return encrypted_md5_bin
        return None
    except Exception:
        return None


def ChecksumMd5(buffer, block_num, plain_text_md5):
    """
    ChecksumMd5(buffer, block_num, plain_text_md5) verify the checksum of the specific chunk in the file
    
    :param buffer:          buffer represent the data in this chunk
    :param block_num:       id of the chunk 
    :param plain_text_md5:  plain text md5 data
    :returns:               returns True for success, False for fail
    """
    md5 = hashlib.md5()
    md5.update(buffer)
    file_digest = md5.hexdigest()
    server_digest = plain_text_md5.split('\n')[block_num + 1]
    return server_digest == file_digest


def CreateMd5(filename, block_size = BLOCK_SIZE):
    """
    CreateMd5(filename, block_size = BLOCK_SIZE) split file into chunks, and calc md5 for each chunk
    
    :param filename:    filename to be checked
    :param block_size:  size of each chunk 
    :returns:           encrypted md5 data
    """
    result = ''
    with open(filename, 'rb') as file:
        src = file.read()
        size = len(src)
        block_count = (size - 1) / block_size + 1
        result += str(block_count) + '\n'
        for i in xrange(block_count):
            m2 = hashlib.md5()
            m2.update(src[i * block_size:i * block_size + block_size])
            result += m2.hexdigest() + '\n'

        m3 = hashlib.md5()
        m3.update(result)
        result += m3.hexdigest()
    return result


if __name__ == '__main__':
    print CreateMd5('entities.pg')
