Розширити логгер з попередньої задачі так, щоб його можна було використовувати наступним чином:
out_stream = sys.stderr
time_formatter = ‘%Y-%m-%d %H:%M:%S’
logger = Logger(out_stream, time_formatter)
... // десь в коді:
	logger.log(‘message for logging’)

