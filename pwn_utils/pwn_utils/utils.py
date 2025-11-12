import logging
import traceback
import asyncio
import concurrent.futures
from asyncio import StreamReader, StreamWriter

log = logging.getLogger(__name__)


def log_error(e, client_writer: StreamWriter):
    if hasattr(e.__traceback__, 'tb_lineno'):
        line = f'Line {e.__traceback__.tb_lineno}'
        traceback.print_tb(e.__traceback__)
    else:
        line = 'no traceback'

    log.error(f'EXCEPTION (handle connection): {e} ({type(e)}) {line}')
    try:
        error = 'Something went wrong with your previous message! '
        error += f'Error: {e} \n'

        client_writer.write(error.encode())
    except Exception as s:
        log.error(f'Exception while handling exception: {s}')
        return


async def read_line_safe(client_reader: StreamReader, client_id=None):
    try:
        if client_reader.at_eof():
            if client_id:
                log.info(f'Client {client_id} terminated')
            else:
                log.info('Client terminated')
            return None
        try:
            data = await asyncio.wait_for(client_reader.readline(), timeout=30.0)
        except concurrent.futures.TimeoutError:
            return None

        if data is None:
            if client_id:
                log.warning(f'Client {client_id} received no data')
            else:
                log.warning('Received no data')
            return None

        if not data.endswith(b'\n'):
            log.warning(f"read partial data:`{data}'")
            return None

        data = data.decode().rstrip()
        if not data:
            log.warning('no data')
            data = ''

        return data
    except Exception as e:
        log.error(f'EXCEPTION (read_line_safe): {e} ({type(e)})')
        return None


async def read_byte_safe(client_reader: StreamReader, client_id):
    try:
        if client_reader.at_eof():
            log.info(f'[{client_id}] client terminated')
            return None

        try:
            data = await asyncio.wait_for(client_reader.read(1), timeout=30.0)
        except asyncio.TimeoutError:
            return None

        if data is None:
            log.warning(f'[{client_id}] received no data')
            return None

        return data

    except Exception:
        log.exception('read_byte_safe failed')
        return None
