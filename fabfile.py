#!/usr/bin/env python
from invoke import UnexpectedExit
from fabric import task
from utils import formatStdout

@task
def checkupSystemUptime(context, args):
    logger = args["logger"]
    try:
        logger.info("Running: uptime")
        result = context.run("uptime")
    except UnexpectedExit as error:
        logger.info("Interrupted!")
        logger.info(error)
        logger.info("Exiting!")
    else:
        formatStdout(result, logger)
        logger.info("Completed: uptime")

@task
def rsyncFolder(context, args):
    logger = args["logger"]
    try:
        logger.info("Running: rsync "+args["rsync"].format_map(args))
        result = context.run("rsync "+args["rsync"].format_map(args))
    except UnexpectedExit as error:
        logger.info("Interrupted!")
        logger.info(error)
        logger.info("Exiting!")
    else:
        formatStdout(result, logger)
        logger.info("Completed: rsync "+args["rsync"].format_map(args))
