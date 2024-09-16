#Embedded file name: I:/bag/tmp/tw2/res/entities\common/pg_protect_test.o
import pg_protect
from pg_protect import BLOCK_SIZE
encrypted_md5_bin = pg_protect.CreateMd5('entities.pg')
plain_text_md5 = pg_protect.VerifyMd5(encrypted_md5_bin)
assert plain_text_md5 is not None
file = open('entities.pg', 'rb')
whole_file = file.read()
file.close()
block_count = (len(whole_file) - 1) / BLOCK_SIZE + 1
for block_num in xrange(block_count):
    buff = whole_file[block_num * BLOCK_SIZE:block_num * BLOCK_SIZE + BLOCK_SIZE]
    assert pg_protect.ChecksumMd5(buff, block_num, plain_text_md5) is True

print 'all pass'
