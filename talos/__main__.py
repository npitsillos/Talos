import logging

from talos.bot import launch

logger = logging.getLogger(__name__)

def run_bot():
    logger.info("Talos is becoming self-aware...")
    launch()

if __name__ == "__main__":
    run_bot()