import bible
import time


if __name__ == '__main__':

    try:
        for t in list(range(24)):
            bible.main()
            time.sleep(3600)
    except Exception as e:
        raise e


