from functools import partial

import loguru

logger = loguru.logger.opt(colors=False)
logger.opt = partial(logger.opt, colors=False)
