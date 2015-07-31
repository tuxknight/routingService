from absFacDealWith import Service


if __name__ == "__main__":

    serviceA = Service('TCP','HTTP')

    serviceA.from_routing()            # data from routing by file;    

    serviceA.to_service()              #deal with data by service;
    serviceA.from_service()

    serviceA.to_routing()              # data to routing by tcp;
