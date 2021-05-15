import os
import shutil
from pathlib import Path
from uuid import uuid4

from wikidict import gen_dict


def test_simple():
    output = Path(os.getenv("CWD", "")) / str(uuid4())
    output.mkdir()
    try:
        ret = gen_dict.main("fr", "logiciel", output)
        assert ret == 0
    finally:
        shutil.rmtree(output)


def test_multiple():
    output = Path(os.getenv("CWD", "")) / str(uuid4())
    output.mkdir()
    try:
        ret = gen_dict.main("fr", "base,logiciel", output)
        assert ret == 0
    finally:
        shutil.rmtree(output)
