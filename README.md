# CIAN analysis (CMF task)
## Description
The project is devoted to the data mining from CIAN and investigating the results. The first file **CIAN_parser.py** downloads the information from [CIAN](http://www.cian.ru). Flats only from central district of Moscow are considered. The output file is **flats_CAD.csv**. It includes the following parameters:

- **N** – number of string
- **Rooms** – room number 
- **Price** – price
- **Totsp** – total apartment space, m^2
- **Livesp** – live apartment space, m^2
- **Kitsp** – kitchen space, m^2
- **Dist** – distance to Moscow center
- **Metrdist** – distance to metro, minutes
- **Walk** – 1 if Metrdist is by foot, 0 if by transport
- **Brick** – 1 if the house is made of bricks/monolith, 0 if another material
- **Tel** – 1 telephone, 0 no telephone
- **Bal** – 1 there is a balcony, 0 if no
- **Floor** – floor number
- **Nfloors** – total number of floors
- **New** – 1 if new house, 0 if secondhand

