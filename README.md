# NBA Data Analysis

## About the Project

This project is mostly to develop my analytics skills and to learn about new Python modules. I decided to key in on a topic of interest for me: sports analytics. Specifically, I will extract NBA data, transform/clean it for readability, and derive unique insights. There are a multitude of methods I plan on analyzing the data that may provide differing context surrounding popular topics of discussion amongs the NBA community. These methods/tools include, but are not limited to:

* Seaborn
* Dash
* Data Visualization
* K Means Clustering
* Regression Analysis
* Predictive Analytics
* etc.

The main dataset (basketball.sqlite) can be downloaded via Kaggle (https://www.kaggle.com/datasets/wyattowalsh/basketball).

## Referee Bias

The first topic I wanted to explore was a controversial issue often discussed amongst NBA fans and analysts alike: are referees biased/do they intentionally impact the outcome of a game?

To start, I connected to the SQL database and queried for the features I was most interested in seeing. I was only interested in viewing data for the 2020-2021 season for now so I matched the referees with the specific game IDs for all games during the season.

Then, I developed a summary data table consisting of information for all referees. This included calculated columns, such as "Home Win %," "Away Win %," "Win Bias," "Home Fouls Per Game," "Away Fouls Per Game," and "Foul Bias." The "Win Bias" calculation took the absolute difference between home and away win percentages to measure the overall bias a referee may have, regardless of who it may favor. The "Foul Bias" followed the same process to better understand to what degree a ref may sway when calling fouls.

Once the data was cleansed and I had derived my features of interest, it was time to visualize the data in a format that allows for anyone to derive insights from. I utilized Seaborn to form an initial visualization to better contextualize the dataset. While most refs did not appear to pose substantial bias (e.g., win % close to 50-50 or low "Win Bias"), there were some that stood out. As I visualized the most biased referees, I noticed some refs had abnormaly high percentages. As I dug a little deeper, I found they only reffed a handful of games so I updated my dataset by removing these outliers that provided no statisitical significance.

As there are limitations to Seaborn, I developed a dashboard that better summarized _all_ the data via a Python module called Dash. This better painted a picture as to _how many_ referees actually show bias.

As you can see below, there is only a handful of referees that show a large enough bias to pose some questioning. And for the most part, that bias is in favor of the home team. According to Bleacher Report, the home team wins about 60% of the games. Home court advantage does exist and should be factored into this data as we contextualize it. The referees we are most interested in are the ones that referee games with a high percent of away teams winning. Unsuprisingly, these are the ones that ranked the highest in the "Win Bias" calculations, specifically Andy Nagy, Jason Goldenberg, and Marc Davis.

<img width="900" alt="image" src="https://user-images.githubusercontent.com/64810038/169672666-f57fed53-bd0d-42e3-bcc4-5103d7ef0a42.png">
<img width="878" alt="image" src="https://user-images.githubusercontent.com/64810038/169672669-f650fc1d-6344-40b7-8aa9-7ace101d842a.png">
<img width="880" alt="image" src="https://user-images.githubusercontent.com/64810038/169672676-1e19e88e-70db-4053-af3a-060f597a4b3f.png">
<img width="871" alt="image" src="https://user-images.githubusercontent.com/64810038/169672681-3de2864e-1825-4685-b76a-e92719106380.png">
<img width="880" alt="image" src="https://user-images.githubusercontent.com/64810038/169672685-88dee119-6b2d-44e2-8140-f472159f3753.png">

I also wanted to see if the way referees called fouls had an affect on the outcome of the game. We see below that some referees that had a large differential in fouls between home and away teams trended toward having a higher difference in win percentage as well. However, their is no clear overall trend to conclude that the increased foul bias has an effect on the game. It id clear that there are a multitude of factors in a game that the referees may take advantage of to sway a game in one direction or another.

<img width="917" alt="image" src="https://user-images.githubusercontent.com/64810038/169672695-69b96945-72f2-42fa-82b2-bdb86cd0bfb4.png">

I think there are some interesting insights to gather from these visualizations beyond what I have mentioned above. It's worrying that there are refs that are on extreme ends of the spectrum in this dataset. This should be something for the NBA, fans, or analysts to key in on and scrutinize. It is increasingly clear that Tim Donaghy was not the only referee of his kind and that the NBA may be hiding similar corrupt refs that may be swaying the outcome of games. Additionally, understanding this information and knowing who is refereeing each game could be a valuable betting strategy.

So what solutions are there to minimize referee bias? For one, the NBA can better utilize analytics to automatically derive referee schedules. By utilizing AI and machine learning, the NBA can pinpoint which refs may pose a risk of the most bias and pair them with those that have shown little bias when scheduling what games they will be reffing. Additionally, a form of regular auditing may be necessary. These referees have the ability to sway outcomes of games that have a multitude of financial implications. Team owners, bettors/investors, and fans have money and emotional attachments to each and every game. Making sure that the refs are good at their job and offer fair/non-preferential treatment night in and night out is important for the long-term sustainability of the league as a whole.
