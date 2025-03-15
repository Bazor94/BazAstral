import services.send_fleet as send_fleet
import logging

def collect_all_resources_cron(planet, planets, seconds_delay, stop_threads):
    cargos = ['LIGHT_CARGO', 'HEAVY_CARGO']
    main_planet_id = planet.id
    other_planet_ids = [p.id for p in planets]

    while not stop_threads.is_set():
        send_fleet.collect_all_resources(main_planet_id, other_planet_ids, cargos)
        logging.info(f'collect resources | sleeping for {seconds_delay}')
        stop_threads.wait(seconds_delay)
