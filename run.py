import argparse
import asyncio
import pathlib

from demo import config, server, runner

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--environment", type=str, default="DEVELOPMENT",
        help="Provide the environment (LIVE/DEVELOPMENT)")
    args = parser.parse_args()
    # Imagine we are retrieving the secret from another service
    config.init(args.environment, pathlib.Path("secret.txt").read_text())
    config.server_config()
    server.start_server()
    event_handler = runner.EventHandler.get_instance()
    asyncio.get_event_loop().create_task(event_handler.run_until_crash())
    asyncio.get_event_loop().run_forever()
