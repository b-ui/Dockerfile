import sys

import logbook
from logbook import StreamHandler, LogRecord


class MyLogger(logbook.Logger):
    def __init__(self, name=None, level=0):
        super(MyLogger, self).__init__(name, level)

    def debug(self, *args, **kwargs):
        try:
            super(MyLogger, self).debug(*args, frame_correction=4, **kwargs)
        except Exception as e:
            print(e)

    def info(self, *args, **kwargs):
        try:
            super(MyLogger, self).info(*args, frame_correction=4, **kwargs)
        except Exception as e:
            print(e)

    def warn(self, *args, **kwargs):
        try:
            super(MyLogger, self).warn(*args, frame_correction=4, **kwargs)
        except Exception as e:
            print(e)

    def error(self, *args, **kwargs):
        try:
            super(MyLogger, self).error(*args, frame_correction=4, **kwargs)
        except Exception as e:
            print(e)

    def critical(self, *args, **kwargs):
        try:
            super(MyLogger, self).critical(*args, frame_correction=4, **kwargs)
        except Exception as e:
            print(e)

    def make_record_and_handle(self, level, msg, args, kwargs, exc_info,
                               extra, frame_correction):
        channel = None
        if not self.suppress_dispatcher:
            channel = self

        elapsed = kwargs.pop('elapsed') if 'elapsed' in kwargs else None
        fn_name = kwargs.pop('fn_name') if 'fn_name' in kwargs else None
        module_name = kwargs.pop('module_name') if 'module_name' in kwargs else None
        filename = kwargs.pop('filename') if 'filename' in kwargs else None
        context = kwargs.pop('context') if 'context' in kwargs else None
        record = LogRecord(self.name, level, msg, args, kwargs, exc_info,
                           extra, None, channel, frame_correction)

        record.extra.update(elapsed=elapsed)
        if fn_name:
            record.func_name = fn_name
        if module_name:
            record.module = module_name
        if filename:
            record.filename = filename
        record.extra.update(context=context)

        try:
            self.handle(record)
        finally:
            record.late = True
            if not record.keep_open:
                record.close()


logger = MyLogger('app')

format_app = u'''
------------------------------------------------------
Time:               {record.time:%Y-%m-%d %H:%M:%S.%f}
Message type:       {record.level_name}
Location:           {record.filename}:{record.lineno}
Module:             {record.module}
Function:           {record.func_name}
Message:            {record.message}
'''

format_str = '{record.time:%Y-%m-%d %H:%M:%S.%f} {record.level_name} {record.module}' \
             ' {record.func_name} - {record.message}'

stream_handler = StreamHandler(sys.stdout, format_string=format_str, bubble=True)

