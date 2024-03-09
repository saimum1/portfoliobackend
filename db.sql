CREATE TABLE postdata (
    id SERIAL PRIMARY KEY,
    userid VARCHAR(200) ,
    postid VARCHAR(200) ,
    title VARCHAR(200) ,
    description VARCHAR(500) ,
    color VARCHAR(200),
    content VARCHAR(50000000000) ,
    created VARCHAR(500) ,
    category VARCHAR(500) ,
    selected VARCHAR(50) ,
    imageurl VARCHAR(500)
);




CREATE TABLE homedata (
    id SERIAL PRIMARY KEY,
    userid VARCHAR(200) ,
    titlefirst VARCHAR(200) ,
    titlesecond VARCHAR(500) ,
    linkurlcv VARCHAR(500) ,
    logourl VARCHAR(200)
);




CREATE TABLE homedataimage (
    id SERIAL PRIMARY KEY,
    userid VARCHAR(200) ,
    homeid VARCHAR(200),
    image_url VARCHAR(200) ,
    linkurlmedia VARCHAR(200) 
);