import services.fleet as fleet
import logging
import threads


def collect_all_resources_cron(planet, planets, seconds_delay):
    cargos = ['LIGHT_CARGO', 'HEAVY_CARGO']
    main_planet_id = planet.id
    other_planet_ids = [p.id for p in planets]

    collect(main_planet_id, other_planet_ids, cargos, seconds_delay)


@threads.stoper(threads.stop_threads, threads.running_threads['collect'])
def collect(main_planet_id, other_planet_ids, cargos, seconds_delay):
    fleet.collect_all_resources(main_planet_id, other_planet_ids, cargos)
    logging.info(f'collect resources | sleeping for {seconds_delay}')
    threads.stop_threads.wait(seconds_delay)
