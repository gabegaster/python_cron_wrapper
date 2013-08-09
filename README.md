###What###
Import this decorator and cron will only email you when the method first fails and then when it starts working again, giving a report of the number of fails and error logs.

###Why###
Helpful if you do not want to get 58 emails if a site you are scraping is down for 58 minutes.

###It's easy###
Just add the cron_manager decorator, to let cron quietly, smartly and succinctly report errors.

    from cron_manager import cron_manager

    # your code here

    @cron_manager
    def some_cron_script_that_you_wrote(...):
        pass
