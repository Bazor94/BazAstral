login = 'tijaci2136@sectorid.com'
password = 'BazAstral123'
session_id = 'vemh5pgpm3wbn3nbrbybqjn0'
jwt = 'eyJhbGciOiJodHRwOi8vd3d3LnczLm9yZy8yMDAxLzA0L3htbGRzaWctbW9yZSNobWFjLXNoYTI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3MzkwNDExNDAsImV4cCI6MjA1NDU3Mzk0MCwiSWQiOiIzYTBjYmE1Ny1iYTU3LTQyZGItYjVjMS1iMzUyOTFkMDA0N2QiLCJTZXNzaW9uSWQiOiI5YWY4N2YwYy01MGRiLTQ4MjUtOGNjZC1hYTYwNGE3Y2I3OTYifQ.o5SWnY9PWV-HA8UDF5y-ThUCNuTeoMJnAgbKAe9HuP0'
cloudflare = 'Cc9X6h1.px9wSEGqgvaRWY7SZsLynM3mUzQAtvmiWmE-1739041032-1.2.1.1-rpkf2OsDaOs06wHPWZkGnrspEWwGKkT6MuGZPpeR3YKPmwKCboodz2fxJNK2kMxKZm7sri7rCGTlvN48n8kdYlMIVWKvwGDykOp9okwubT_GgC4ngolfloCBgtVXjdOMxyPwVz5PVAxci33i44adg7IGXU5SfE7NGvvfyaPgNM2B5rz0DrNxJDERcTnsYNgPVCO9GvnThoUeEFKhMQX9d6ry8cMdxOtWTuxJHW2GYd7_bq9QvEuPHOrrLjTItw4_f1kCbyLYvuB4KnuzdT2jLCEXbo.wI630zfk4V5wFiTo'

host = 'https://lyra.ogamex.net'
coords = ["1:184:5"]

cookies = {
    'SessionId': f'{session_id}',
    'gameAuthToken': f'{jwt}',
    'cf_clearance': f'{cloudflare}',
    'lang': 'en',
    'timeZoneOffset': '60',
    '_gid': 'GA1.2.441450251.1739041032',
    '_ga': 'GA1.1.38274606.1739041032',
    '_ga_65PNDYM0LK': 'GS1.1.1739041032.1.1.1739041194.50.0.0'
}


headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en",
        "priority": "u=0, i",
        "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132")',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    }
