from src.telegram.client import startClient, getClient

import asyncio, traceback, sys

try:
    import plugins as plugins
except ImportError:
    try:
        from . import plugins
    except ImportError:
        print(traceback.format_exc())
        print('could not load the plugins module', file=sys.stderr)
        exit(1)


async def main():
    bot = await getClient()
    await startClient()
    bot.parse_mode = 'html'

    try:
        await plugins.init(bot)
        await bot.run_until_disconnected()

    except asyncio.CancelledError:
        pass

    except Exception as error:
        print(f'[-] Error (main.py) :-> {error}')
        traceback.print_exc()

    finally:
        await bot.disconnect()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except Exception as error:
        print(f'[-] Error (main.py) :-> {error}')
        traceback.print_exc()
    finally:
        loop.close()
