from absFacDealWith import Service


if __name__ == "__main__":

    serviceA = Service(FILE_Style,TCP_Style)

    serviceA.from_routing(FILE_Style)  # data from routing by file;    

    serviceA.to_service()              #deal with data by service;
    serviceA.from_service()

    serviceA.to_routing(TCP_Style)     # data to routing by tcp;
