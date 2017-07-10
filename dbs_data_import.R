library(dplyr)
library(lubridate)
library(stringr)
library(RPostgreSQL)
library(stringi)
library(tidyr)

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
content <- iconv(content, "ASCII", "UTF-8", sub = "")
tweet_query <- data.frame(ID=id, time=time, NoRetweets=retweets, handle=handle, NoFav=likes, content=content)

#contains relation
##hashtag format: whitespace #word
##get all hashtags and store them in a column. the regex just find correctly formatted hashtags.
data <- mutate(data, name=str_extract_all(data$text, "\\B#\\w\\w+"))
##get tweet id for each hashtag
data <- mutate(data, id=(1:length(content)))
temp <- select(data, label=name, ID=id)
contains <- unnest(temp)
##all hashtags to lower case.
contains <- mutate(contains, label = tolower(label))
contains_query <- (unique(contains))

data <- mutate(data, all_hashtags=str_extract_all(data$text, "#\\s*\\w+"))
all_hashtags <- select(data, all_hashtags)
all_hashtags <- tolower(unique(unlist(all_hashtags)))
good_hashtags <- unique(contains$label)
bad_hashtags <- setdiff(all_hashtags, good_hashtags) 

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

##close the connection
dbDisconnect(conn)
dbUnloadDriver(pg)



