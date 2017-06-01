library(dplyr)
library(lubridate)
library(stringr)
library(RPostgreSQL)
library(stringi)

#read data
data <- read.csv2("/Users/HeMan/Desktop/DatenbankenSS17/american-election-tweets.csv", header = T, encoding = "UTF-8")

#extract relevant data from the .csv and store it in seperate vectors. build tables afterwards.

#tweet realtion
handle <- as.character(data$handle)
content <- as.character(data$text)
retweets <- as.numeric(data$retweet_count)
likes <- as.numeric(data$favorite_count)
time <- ymd_hms(data$time)
id <- (1:(length(content)))
##make content db safe
content <- iconv(content, "ASCII", "UTF-8", sub = "x")
tweet_query <- data.frame(ID=id, time=time, NoRetweets=retweets, handle=handle, NoFav=likes, content=content)

#contains relation
##get all hashtags and store them in a vector.
data <- mutate(data, name=str_extract_all(data$text, "#(\\s)*(\\w)+"))
##get tweet id for each hashtag
data <- mutate(data, id=(1:length(content)))
temp <- select(data, label=name, ID=id)
##no need for a listtype column
contains <- unnest(temp)
##all hashtags to lower case.
contains <- mutate(contains, label = tolower(label))
contains_query <- (unique(contains))

#hashtag relation
hashtag_query <- data.frame(label = unique(contains$label))


#export

## connect to database
pg = dbDriver("PostgreSQL")
conn = dbConnect(pg, user="postgres", password="postgres", host="localhost", port="5432", dbname="election")

##write tables tweet, hashtag
dbWriteTable(conn,'tweet', tweet_query, row.names=F, overwrite=F, append=T)
dbWriteTable(conn,'hashtag', hashtag_query, row.names=F, overwrite=F, append=T)
dbWriteTable(conn,'contains', contains_query, row.names=F, overwrite=F, append=T)




