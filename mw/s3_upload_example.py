'''
These are notes from some earliwr work

From python manage.py shell:
   >>> import io
   >>> from django.core.files.base import ContentFile
   >>> from django.core.files.storage import default_storage

   >>> file = default_storage.open('storage_test', 'w')
   >>> file.write('storage contents')
   16
   >>> file.close()
   >>> file = default_storage.open('storage_test.txt', 'w')
   >>> file.write('storage contents')
   16
   >>> file.close()
   >>> 
   >>> output = io.StringIO()
   >>> output.write('First line.\n')
   12
   >>> path = default_storage.save('boo/hoo', ContentFile(output.getvalue()))
   >>> with io.StringIO() as fh:
       ...     fh.write('First line.\n')
       ...     fh.write('Second line.\n')
       ...     path = default_storage.save('boo/hoo.txt', ContentFile(fh.getvalue()))
       ...     print(path)
       ... 
       12
       13
       boo/hoo.txt
   >>> 
datetime.now().strftime('%Y:%b:%d-%H%M%S')
'''
import io
from datetime import datetime
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
#print('{}'.format(dir(default_storage)))
#print('{}'.format(default_storage.__dict__))
#print('{}'.format(default_storage.default_acl))

def write_timestamp():
    now = datetime.now().strftime('%Y-%b-%d-%H%M%S')
    default_storage.default_acl = 'private'
    with io.StringIO() as fh:
        fh.write('{}.\n'.format(now))
        path = default_storage.save('hello-world/{}.txt'.format(now), ContentFile(fh.getvalue()))
