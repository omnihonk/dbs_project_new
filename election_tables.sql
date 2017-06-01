create TABLE hashtag (label TEXT PRIMARY KEY NOT NULL);
create TABLE tweet (
ID INT PRIMARY KEY NOT NULL,
time TIMESTAMP,
NoRetweets INT ,
handle TEXT,
NoFav INT,
content TEXT NOT NULL
);
create TABLE contains (
ID INT NOT NULL,
label TEXT NOT NULL,
PRIMARY KEY(ID,label));
