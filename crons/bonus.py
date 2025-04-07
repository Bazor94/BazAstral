import services.fleet_service as fleet_service
from logger import logger
import threads
from EP import bonus as bonus_ep

@threads.stoper(threads.stop_threads, threads.running_threads['bonus'])
def promote_cron():
    token, time = bonus_ep.get_promote_timeout()

    if time != None:
        time_sleep = int(time.total_seconds())
        logger.sleep_log("bonus", None, time_sleep)
        threads.stop_threads.wait(time_sleep)

    logger.info(f'visiting websites', extra={"action": "bonus"})
    bonus_ep.visit_all_promotes(token)

@threads.stoper(threads.stop_threads, threads.running_threads['bonus'])
def online_bonus_cron():
    is_present = bonus_ep.is_online_bonus_present()
    
    if is_present:
        logger.info(f'getting online_bonus', extra={"action": "bonus"})
        bonus_ep.online_bonus()
        
        sleep_time = 3*3600
    else:
        sleep_time = 500

    threads.stop_threads.wait(sleep_time)
    
