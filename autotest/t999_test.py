import os
import config


def test_teardown():

    success = config.get_success()

    if success:
        if os.path.isfile(config.target_dict[config.program]):
            print("Removing " + config.target)
            os.remove(config.target_dict[config.program])

    return


if __name__ == "__main__":
    test_teardown()
