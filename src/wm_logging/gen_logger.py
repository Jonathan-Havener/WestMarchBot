from pathlib import Path
import logging
from datetime import datetime

this_file = Path(__file__).parent.resolve()

# Create a logger
gen_logger = logging.getLogger('multi_output_logger')
gen_logger.setLevel(logging.DEBUG)  # Set the base level to DEBUG to capture all levels

# Create handlers
console_handler = logging.StreamHandler()  # Handler to output to console
console_handler.setLevel(logging.DEBUG)    # Send DEBUG and above to the console

# Handler to write DEBUG and above to a file
execution_date = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
file_handler = logging.FileHandler(this_file.parent.parent / 'logs' / f'general-{execution_date}.log')
file_handler.setLevel(logging.DEBUG)

# Create formatters and add them to the handlers
console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

console_handler.setFormatter(console_format)
file_handler.setFormatter(file_format)

# Add handlers to the logger
gen_logger.addHandler(console_handler)
gen_logger.addHandler(file_handler)

# Example log messages
# gen_logger.debug("This is a debug message")
# gen_logger.info("This is an info message")
# gen_logger.warning("This is a warning message")
# gen_logger.error("This is an error message")
# gen_logger.critical("This is a critical message")
