import shodan

SHODAN_API_KEY = "SkVS0RAbiTQpzzEsahqnq2Hv6SwjUfs3"
api = shodan.Shodan(SHODAN_API_KEY)
try:
    results = api.pipsearch('Apache')
    print('Results found: %s' % results['total'])
    for result in results['matches']:
        print ("%s:%s|%s|%s"%(result['ip_str'],result['port'],result['location']['country_name'],result['hostnames']))
except shodan.APIError as e:
    print('Error: %s' % e)