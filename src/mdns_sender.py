from zeroconf import Zeroconf, ServiceInfo

# create a zeroconf instance
zeroconf = Zeroconf()

# create a service info object with your desired configuration
info = ServiceInfo("_http._tcp.local.",
                   "ArtNetMerger._http._tcp.local.",
                   port=80,
                   weight=0,
                   priority=0,
                   properties={})

# register the service with zeroconf
zeroconf.register_service(info)

# when you're done, make sure to unregister the service
zeroconf.unregister_service(info)
while True:
    pass

# finally, close the zeroconf instance
zeroconf.close()