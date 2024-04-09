"""Logger config module."""


from logging import DEBUG, INFO, getLogger, basicConfig

LOG = getLogger(__name__)

basicConfig(level=DEBUG,
            format='%(levelname)s: %(module)s.py: %(funcName)s(): %(message)s')
