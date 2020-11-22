from src.com.stock.common.import_lib import *
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
print(ROOT_DIR)
config = {
    "version" :1,
    "formatters":{
        "simple": {"format": "[%(name)s] %(message)s"},
        "complex": {
            "format": "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "complex",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "error.log",
            "formatter": "complex"
        },
        "TR_1206": {
            "class": "logging.FileHandler",
            "filename": ROOT_DIR+"/TR_1206.log",
            "formatter": "complex",
            "encoding": "utf-8"
        },
        "upjong_code_mst": {
            "class": "logging.FileHandler",
            "filename": ROOT_DIR+"/upjong_code_mst.log",
            "formatter": "complex",
            "encoding": "utf-8"
        }

    },
    #"root": {"handlers": ["console", "file"], "level": "WARNING"},
    "loggers": {"parent": {"level": "INFO"}, "parent.child": {"level": "DEBUG"}, "myLogger":{"handlers": [ "console", "file"], "level" :"DEBUG"},
                "TR_1206":{"handlers": [ "console", "file","TR_1206"], "level" :"DEBUG"}, "upjong_code_mst":{"handlers": [ "console", "file","upjong_code_mst"], "level" :"DEBUG"}},

}
logging.config.dictConfig(config)
if __name__ == "__main__":
    myLogger = logging.getLogger("TR_1206")
    myLogger.debug("TR_1206")
    #myLogger.debug("test2")

