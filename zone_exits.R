## Fauzan Lodhi
## Undergraduate, University of Waterloo Faculty of Math
## 2024 HBDC Submission
## this script was used to create graphics included in submission
## please note that other graphics were produced using Power BI

library(ggplot2)

data <- read.csv("BDC_Breakout_Levels_update.csv")

level5 <- subset(data, Breakout_Level == 5)
level4 <- subset(data, Breakout_Level == 4)
level3 <- subset(data, Breakout_Level == 3)
level2 <- subset(data, Breakout_Level == 2)
level1 <- subset(data, Breakout_Level == 1)

df_shots <- subset(data, Event == 'Shot' | Event == 'Goal')
df_goals <- subset(data, Event == 'Goal')
breakout_shots <- subset(data, Breakout_End == 4 |  Breakout_End == 5)
breakout_goals <- subset(data, Breakout_End == 5)

shooting_percentage <- 100 * nrow(df_goals) / nrow(df_shots)
breakout_shooting_percentage <- 100 * nrow(breakout_goals) / nrow(breakout_shots)

shooting_percentage
breakout_shooting_percentage



## heat map of all shots generated in the dataset
gr2 <- ggplot(df_shots, aes(x = X.Coordinate, 
                            y = Y.Coordinate)) +
        geom_density_2d_filled() +
        xlab("x from center ice") + 
        ylab("y from center ice") + ggtitle("Heat Map of All Shots")

plot(gr2)




## Heat map of all shots generated from breakout level 4 and 5
gr2 <- ggplot(breakout_shots, aes(x = X.Coordinate, 
                            y = Y.Coordinate)) +
  geom_density_2d_filled() +
  xlab("x from center ice") + 
  ylab("y from center ice") + ggtitle("Heat Map of Shots Generated From Zone Exits")

plot(gr2)


## Heat map of all level 5 breakouts
level5heatmap <- ggplot(level5, aes(x = X.Coordinate, 
                                  y = Y.Coordinate)) +
  geom_density_2d_filled() +
  xlab("x from center ice") + 
  ylab("y from center ice") + ggtitle("Heat Map of Level 5 Zone Exits")
plot(level5heatmap)


## Heat map of all level 4 breakouts
level4heatmap <- ggplot(level4, aes(x = X.Coordinate, 
                                    y = Y.Coordinate)) +
  geom_density_2d_filled() +
  xlab("x from center ice") + 
  ylab("y from center ice") + ggtitle("Heat Map of Level 4 Zone Exits")
plot(level4heatmap)


## Heat map of all level 3 breakouts
level3heatmap <- ggplot(level3, aes(x = X.Coordinate, 
                                    y = Y.Coordinate)) +
  geom_density_2d_filled() +
  xlab("x from center ice") + 
  ylab("y from center ice") + ggtitle("Heat Map of Level 3 Zone Exits")
plot(level3heatmap)

## Heat map of all level 2 breakouts
level2heatmap <- ggplot(level2, aes(x = X.Coordinate, 
                                    y = Y.Coordinate)) +
  geom_density_2d_filled() +
  xlab("x from center ice") + 
  ylab("y from center ice") + ggtitle("Heat Map of Level 2 Zone Exits")
plot(level2heatmap)

## Heat map of all level 1 breakouts
level1heatmap <- ggplot(level1, aes(x = X.Coordinate, 
                                    y = Y.Coordinate)) +
  geom_density_2d_filled() +
  xlab("x from center ice") + 
  ylab("y from center ice") + ggtitle("Heat Map of Level 1 Zone Exits")
plot(level1heatmap)