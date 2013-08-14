import os

def cron_manager(method):
    def wrapped(*args, **kwargs):
        error_file = os.path.join(os.getenv("HOME"),
                                  method.__name__+"_error.log")
        touch(error_file)
        error_msgs = get_error_msgs(error_file)
        prior_errors = len(error_msgs)
        try:
            method(*args, **kwargs)
        except Exception as e:
            # log the error
            with open(error_file, 'a') as f:
                f.write("%s\n"%e.__repr__())
            if prior_errors:   # dont email if you are repeatedly failing
                pass
            else:
                # but send an email if it's a new error
                msg = "Cronjob %s failed!\n%s"%(method.__name__,e.__repr__())
                raise(Exception(msg))
        else:
            # it worked!
            clear_log_file(error_file)
            if prior_errors:
                msg = "Cronjob %s worked, after failing "%method.__name__
                msg += "%s times.\n\n\n%s"%(prior_errors,
                                            "\n".join(error_msgs))
                raise(Exception(msg))

    wrapped.__name__ = method.__name__
    return wrapped

def get_error_msgs(file_name):
    with open(file_name, "r") as f:
        out = f.readlines()
    return out

def clear_log_file(file_name):
    with open(file_name, 'w') as f:
        f.write("") 

def touch(file_name):
    ''' pythonic equivalent of unix touch '''
    with open(file_name, 'a') as f:
        f.write("") 

##### Testing ####

def threw_error(method, arg):
    try:
        method(arg)
    except Exception as e:
        return e

    return False

@cron_manager
def _is_zero(i):
    assert i==0

def test():
    error_file = os.path.join(os.getenv("HOME"),
                              _is_zero.__name__+"_error.log")
    clear_log_file(error_file)

    _is_zero(0) # no errors thrown, because it worked
    assert not get_error_msgs(error_file) # no error msgs either

    out = threw_error(_is_zero, 1) # first time break, it should throw an exception
    assert type(out) is Exception
    assert out.__str__() == "Cronjob _is_zero failed!\nAssertionError()"

    assert get_error_msgs(error_file) # and log the error

    _is_zero(1) # this should not raise an error, but should log it

    out = threw_error(_is_zero, 0) # now that it's working again, throw an error
    assert type(out) is Exception 
    assert not get_error_msgs(error_file) # and clean up the log file so it's empty

    _is_zero(0) # this should not raise any more exceptions

if __name__ == "__main__":
    test()
