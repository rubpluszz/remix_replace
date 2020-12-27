import json
from flask_babel import _
from flask import current_app
import translators as ts

def translate(text, source_language, dest_language):
    """Функція для перекладу повідомлень заснованана бібліотеці translator"""
    r = ts.bing(text, from_language=source_language, to_language=dest_language, if_use_cn_host=False)
    if r == 'UNKNOWN' or None:
        return _('Error: the translation service failed.')
    return r