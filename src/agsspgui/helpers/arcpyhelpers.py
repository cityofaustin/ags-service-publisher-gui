from ags_service_publisher.logging_io import setup_logger

log = setup_logger(__name__)


def get_install_info():
    log.debug('Importing arcpy...')
    try:
        import arcpy
    except:
        log.exception('An error occurred importing arcpy')
        raise
    log.debug('Successfully imported arcpy')
    log.debug('Getting install info')
    return arcpy.GetInstallInfo()
