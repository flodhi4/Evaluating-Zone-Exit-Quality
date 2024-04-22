# Evaluating-Zone-Exit-Quality
Finalist submission to the 2024 Hockey Big Data Cup.

**Introduction**
Using data provided by Stathletes on women's international ice hockey at an event-based granularity, created a brand new, groundbreaking, robust method of evaluating the quality of a zone exit and a player's individual zone exit talent. This method aims to fill a gap in hockey analytics, where current analytics fail to effectively give credit to players that complete successful zone exits. 

**Methods & Algorithms**
By first cleaning the data to isolate sequences of plays beginning in the defensive zone, this method successfully quantifiies the quality and talent of a zone exit dependent on the outcome of a play that started from the defensive zone. In order to identify plays starting in the defensive zone, this method leverages the given x- and y-coordinates with the "zone" column to map each recorded event to the corresponding zone in which it occurred. Once identifying a play that was recorded by a team in its defensive zone, the next step was to narrow this down to plays made in the defensive zone, where the immediate following play occurred in a different zone. This was then further broken down into various cases, including who owned possession in the following play, how long the current team has possession, where they ultimately advanced the puck, and how the sequence ended.

After completing more data cleaning, the data has now been split into different sequences of plays beginning in the defensive zone and ending in a change of possession, shot, or goal. Based on this, a five-point rating scale was developed, as per the following:

Level 1 = Defensive zone turnover
Level 2 = Successful zone exit without a subsequent successful offensive zone entry
Level 3 = Successful zone exit w/ subsequent successful offensive zone entry
Level 4 = Successful zone entry w/ subsequent successful offensize entry and a shot attempt
Level 4 = Successful zone entry w/ subsequent successful offensize entry and a goal scored

Using the above rating scale, each zone exit attempt was scored based on its level, where a level 1 is a score of 1/5, level 2 is a score of 2/5, and so on. Then to further evaluate an individual player's talent, this is calculated by SUM(zone exit level) / (5 * zone exit attempts).


**Application**
The talent level quantified by this rating scale provides a way to evaluate how adept an individual player is at making successful zone exits, and how they are able to generate offense from the defensive zone. Ultimately, this works as a scouting tool for players and teams, giving insight as to how player may succeed or struggle at moving the puck from their own end. Additionally, given the x- and y-coordinate values, each event can be mapped on a scatterplot to devise patterns and trends of where players struggle and excel, based on the quality of their zone exit. For example, it was found that most level 5 zone exits occurred near the blueline, and most level 1 zone exits occurred below the goal line. It was also shown that each player respectively struggled in particular areas of the defensive zone, with some players especially struggling in front of the net, or perhaps along the boards on their strong side, etc. 
