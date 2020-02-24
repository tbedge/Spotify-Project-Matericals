################################
### Syneos Health Case Study ###
###       Trevor Edge        ###
###        Due 2/23/20       ###
################################

rm(list = ls())

#Packages
#install.packages("dplyr")
#install.packages("readxl")
#install.packages("Rcmdr")
#install.packages("ggplot2")

library(dplyr)
library(readxl)
library(Rcmdr)
library(ggplot2)

#Loading ArtistData and popularity
setwd("C:/Users/trevo.DESKTOP-Q3G2N9L/Documents/Resume Materials/Syneos Health/Case Study Scripts")
data <- read_excel('ArtistData.xlsx')
popularity <- read_excel('Popularity.xlsx')

#Adding the popularity variable to our data
data <- merge(data, popularity, by="song_uri")

#Data Cleaning
names(data)[2] <- 'X'
names(data)[25] <- 'Y'
data <- subset(data, select = -c(X, Y))
cleandata <- subset(data, select = -c(album_uri, id, track_href, analysis_url, type))

#Binning continuous variables - INSTRUMENTALNESS NOT INCLUDED IN GROUPING
cleandata$danceability_bin <- as.factor(bin.var(cleandata$danceability, bins = 3, method = "proportion"))
cleandata$energy_bin <- as.factor(bin.var(cleandata$energy, bins = 3, method = "proportion"))
cleandata$loudness_bin <- as.factor(bin.var(cleandata$loudness, bins = 3, method = "proportion"))
cleandata$speechiness_bin <- as.factor(bin.var(cleandata$speechiness, bins = 3, method = "proportion"))
cleandata$acousticness_bin <- as.factor(bin.var(cleandata$acousticness, bins = 3, method = "proportion"))
cleandata$liveness_bin <- as.factor(bin.var(cleandata$liveness, bins = 3, method = "proportion"))
cleandata$valence_bin <- as.factor(bin.var(cleandata$valence, bins = 3, method = "proportion"))
cleandata$tempo_bin <- as.factor(bin.var(cleandata$tempo, bins = 3, method = "proportion"))
cleandata$duration_ms_bin <- as.factor(bin.var(cleandata$duration_ms, bins = 3, method = "proportion"))
cleandata$popularity_bin <- as.factor(bin.var(cleandata$popularity, bins = 3, method = "proportion"))

ggplot(cleandata, aes(x = factor(energy_bin))) +
  geom_bar(color = "black") +
  theme(panel.border = element_blank(), panel.grid.major = element_blank(),
              panel.grid.minor = element_blank(), axis.line = element_line(colour = "black"))
######### Happy/Danceable/Party Metrics (Rank ordered by Popularity) ##############
#Valence (high)   Energy (high)   Danceability (high)

happysongs <- filter(cleandata, (valence_bin == 3  & energy_bin == 3 & danceability_bin ==3 &
                                   popularity_bin == 3))

happysongs$popularity <- as.numeric(happysongs$popularity)
sort.happysongs <- happysongs[order(-happysongs$popularity),]

#Randomly sampling from the list of "happy" songs so that a new playlist can be created each time 
      #with a different seed
set.seed(1234)
HappyPlaylist <- sample(sample(seq_len(nrow(sort.happysongs))), size = 25)
HappyPlaylist <- sort.happysongs[HappyPlaylist, c("track", "artist")]
HappyPlaylist <- unique(HappyPlaylist[,c("track", "artist")]) #Making sure there's no duplicates 

############## Sad/Slow Metrics (Rank ordered by Popularity) ###################
# Valence(low)  Energy (low)  Danceability (low)  Loudness (low)

sadsongs <- filter(cleandata, (valence_bin == 1  & energy_bin == 1 & danceability_bin ==1 & 
                                 loudness_bin == 1 & popularity_bin == 3))

sadsongs$popularity <- as.numeric(sadsongs$popularity)
sort.sadsongs <- sadsongs[order(-sadsongs$popularity),]

#Randomly sampling from the list of "sad" songs so that a new playlist can be created each time 
      #with a different seed
set.seed(1234)
SadPlaylist <- sample(sample(seq_len(nrow(sort.sadsongs))), size = 25)
SadPlaylist <- sort.sadsongs[SadPlaylist, c("track", "artist")]
SadPlaylist <- unique(SadPlaylist[,c("track", "artist")])

############# Live/Acoustic Metrics (Rank ordered by Popularity) ###############
# Liveness (high)   Acousticness

livesongs <- filter(cleandata, (liveness_bin == 1  & acousticness_bin == 1 & popularity_bin == 3))

livesongs$popularity <- as.numeric(livesongs$popularity)
sort.livesongs <- livesongs[order(-livesongs$popularity),]

#Randomly sampling from the list of "acoustic"/"live" songs so that a new playlist can be created each time 
#with a different seed
set.seed(1234)
LivePlaylist <- sample(sample(seq_len(nrow(sort.livesongs))), size = 25)
LivePlaylist <- sort.livesongs[LivePlaylist, c("track", "artist")]
LivePlaylist <- unique(LivePlaylist[,c("track", "artist")])

#Exporting Playlists to excel files
install.packages("openxlsx")
library(openxlsx)
happy <- "C:/Users/trevo.DESKTOP-Q3G2N9L/Documents/Resume Materials/Syneos Health/HappyPlaylist.xlsx"
sad <- "C:/Users/trevo.DESKTOP-Q3G2N9L/Documents/Resume Materials/Syneos Health/SadPlaylist.xlsx"
live <- "C:/Users/trevo.DESKTOP-Q3G2N9L/Documents/Resume Materials/Syneos Health/LivePlaylist.xlsx"

write.xlsx(HappyPlaylist, file = happy)
write.xlsx(SadPlaylist, file = sad)
write.xlsx(LivePlaylist, file = live)

#Getting correlations of spotify's numeric metrics
install.packages("corrplot")
library(corrplot)

numericdata <- subset(data, select = -c(song_uri, artist, album_name, album_uri, track, release_date, id,track_href, analysis_url, type))
numericdata.cor = cor(numericdata, method = c("kendall"))
corrplot(numericdata.cor)

palette = colorRampPalette(c("red", "white", "green")) (100)
heatmap(x = numericdata.cor, col = palette, symm = TRUE)
