import services.build_defense as defense_service
import logging
import threads


def build_def_cron(planet, seconds_delay):
    threads.stop_threads.wait(5*60)
    build_def(planet, seconds_delay)
        

@threads.stoper(threads.stop_threads, threads.running_threads['defense'])
def build_def(planet, seconds_delay):
    defense_service.build_max_defense_one_planet(planet)
    logging.info(f'building defence | sleeping for {seconds_delay}')
    threads.stop_threads.wait(seconds_delay)