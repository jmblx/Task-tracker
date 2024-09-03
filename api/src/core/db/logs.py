import logging
import time

from sqlalchemy import Engine, event

from core.logs.log_conf import configure_logging

# Создайте собственный логгер
logger = logging.getLogger(__name__)

configure_logging()


@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(
    conn, cursor, statement, parameters, context, executemany
):
    conn.info.setdefault("query_start_time", []).append(time.time())
    logger.info("Start Query: %s", statement)
    logger.info("Parameters: %s", parameters)
    context._query_start_time = time.time()


@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(
    conn, cursor, statement, parameters, context, executemany
):
    total = time.time() - context._query_start_time
    logger.info("Query Complete!")
    logger.info("Total Time: %f", total)


@event.listens_for(Engine, "handle_error")
def handle_error(context):
    logger.error("An exception occurred: %s", context.original_exception)
