import sip

API_NAMES = ['QDate', 'QDateTime', 'QString', 'QTextStream', 'QTime', 'QUrl', 'QVariant']
API_VERSION = 2
for name in API_NAMES:
    sip.setapi(name, API_VERSION)
