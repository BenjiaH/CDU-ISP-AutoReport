import os

from common import service
from common.logger import logger

logo = r"""
   _____ _____  _    _      _____  _____ _____                    _        _____                       _   
  / ____|  __ \| |  | |    |_   _|/ ____|  __ \        /\        | |      |  __ \                     | |  
 | |    | |  | | |  | |______| | | (___ | |__) ______ /  \  _   _| |_ ___ | |__) |___ _ __   ___  _ __| |_ 
 | |    | |  | | |  | |______| |  \___ \|  ___|______/ /\ \| | | | __/ _ \|  _  // _ | '_ \ / _ \| '__| __|
 | |____| |__| | |__| |     _| |_ ____) | |         / ____ | |_| | || (_) | | \ |  __| |_) | (_) | |  | |_ 
  \_____|_____/ \____/     |_____|_____/|_|        /_/    \_\__,_|\__\___/|_|  \_\___| .__/ \___/|_|   \__|
                                                                                     | |                   
                                                                                     |_|                   
"""
print(logo)
stage = "beta"
version = (os.popen('git rev-parse --short HEAD').read()).replace("\n", "")
logger.info("Version:{version}.".format(version=stage + "." + version))
report_service = service.ReportService()
report_service.start()
