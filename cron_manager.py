import os

def touch(file_name):
    ''' pythonic equivalent of unix touch '''
    with open(file_name, 'a') as f:
        f.write("") 

def cron_manager(method):
    def wrapped():
        error_file = os.path.join(os.getenv("HOME"),
                                  method.__name__+"_error.log")
        touch(error_file)
        with open(error_file, "r") as f:
            error_msgs = f.readlines()
            prior_errors = len(error_msgs)
        try:
            method()
        except Exception as e:
            # log the error
            with open(error_file, 'a') as f:
                f.write("%s\n"%e)
            if prior_errors>0:   # dont email if you are repeatedly failing
                pass
            else:
                # but send an email if it's a new error
                raise("Cronjob %s failed!\n%s"%(method.__name__,str(e)))
        else:
            # it worked!
            with open(error_file, 'w') as f:
                f.write("")
            if prior_errors:
                msg = "Cronjob %s worked, after failing "%method.__name__
                msg += "%s times.\n\n\n%s"%(prior_errors,
                                            "\n".join(error_msgs))
                raise(Exception(msg))
    return wrapped
