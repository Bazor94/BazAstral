import config
import EP.login as login
import mine_asteroid
from EP import home
from EP import fleet


login.login()
x, y, z = map(int, config.coords[0].split(':'))
mine_asteroid.mine_asteroids_cron(x, y, z)