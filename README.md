# CIAN analysis (CMF task)
## Description
The project is devoted to the data mining from CIAN and investigating the results.

1.The first file [CIAN_parser.py](https://github.com/V0lkoff/CIAN_CMF_task-/blob/master/CIAN_parser.py) downloads the information from [CIAN](http://www.cian.ru). Flats only from central district of Moscow are considered. The output file is [flats_CAD.csv](https://github.com/V0lkoff/CIAN_CMF_task-/blob/master/flats_CAD.csv). It includes the following parameters:

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

2.The second file is [Data cleaning.ipynb](https://github.com/V0lkoff/CIAN_CMF_task-/blob/master/Data%20cleaning.ipynb). Here the data is prepared for further investigation. All NuN values are corrected, mostly with machine lerning algorithms. The out put file is presented [Flats_handled.csv](https://github.com/V0lkoff/CIAN_CMF_task-/blob/master/Flats_handled.csv). 

3.The final file is [Price_prediction.ipynb](https://github.com/V0lkoff/CIAN_CMF_task-/blob/master/Price_prediction.ipynb). Some visual analysis is given based on the results of the second script. Below the investigation of flat's space characteristics 
![](https://github.com/V0lkoff/CIAN_CMF_task-/blob/master/SpaceAnalysis.png)

Flats' location
![](https://github.com/V0lkoff/CIAN_CMF_task-/blob/master/LocationAnalysis.png)

And flats additional characteristics
![](https://github.com/V0lkoff/CIAN_CMF_task-/blob/master/TypeAnalysis.png)

Regression model is built with the lightGBM. The prediction is rather accurate. Feature importance bar is presented below. It is logically correlated with previous plots. 
![](https://github.com/V0lkoff/CIAN_CMF_task-/blob/master/feature_importance.png)

From the first view, predictions are accurate despite some fails on anomaly high prices. It can easily be explained. First, the amount of such flats is low. Secondly, when people buy or sell such flats, price depends more on personal sense, rather then on formal features. Plot is presented below.

![](https://github.com/V0lkoff/CIAN_CMF_task-/blob/master/check_accuracy.png)
