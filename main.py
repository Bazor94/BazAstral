import EP.galaxydata as galaxydata
import config
import asteroid_searcher
import EP.fleet as fleet

#print(galaxydata.get_galaxydata_html("https://lyra.ogamex.net/home", 1, 184))
#asteroid_searcher.get_closest_asteroid(config.coords[0], 5)

x = fleet.get_fleet_html()
print(x)
#fleet.send_fleet_3(1, 1, 184, 17)