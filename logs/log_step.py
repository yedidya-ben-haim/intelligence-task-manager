import logging



def step_log():

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s | %(levelname)s | %(message)s",
                        handlers=[logging.FileHandler
                                  (filename=r"C:\python\tests\PythonProject\intelligence-task-manager\logs\app.log",
                                   encoding='utf-8')])


    return logging .getLogger("intelligence_loger")


app_logger = step_log()

