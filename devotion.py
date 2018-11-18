import bible
import time


if __name__ == '__main__':

    try:
        # send daily devotion
        bible.get_kenneth()

        # send 2 hourly verses
        for t in list(range(8)):
            bible.main()
            time.sleep(10800)

    except Exception as e:
        raise e


