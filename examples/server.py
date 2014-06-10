from diffengine.config import Configuration
from diffengine.server import Daemon

CONFIG_PATH = "~/.diffengine/config.yaml"

config = Configuration.from_file(CONFIG_PATH)

server_daemon = Server.from_config(config)
server_daemon.start()
