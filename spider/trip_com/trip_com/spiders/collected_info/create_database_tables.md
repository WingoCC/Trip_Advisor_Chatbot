
```
create table toplist(
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  link VARCHAR(100) NOT NULL,
  PRIMARY KEY(id)
);
```

```
create table toplist_and_destination(
  toplist_id INT NOT NULL,
  destination_id INT NOT NULL
);
```

```
create table destination(
     id INT NOT NULL AUTO_INCREMENT,
     name VARCHAR(100) NOT NULL,
     link VARCHAR(100) NOT NULL,
     description TEXT,
     location_tags VARCHAR(100),
     attractions_link VARCHAR(200),
     restaurants_link VARCHAR(200),
     tours_link VARCHAR(200),
     trip_moments_link VARCHAR(200),
     PRIMARY KEY(id)
     );
```

```
create table destination_and_attraction(
     destination_id INT NOT NULL,
     attraction_id INT NOT NULL
     );
```

```
create table attraction(
     id INT NOT NULL AUTO_INCREMENT,
     name VARCHAR(100) NOT NULL,
     link VARCHAR(200) NOT NULL,
     location_tags VARCHAR(150), 
     open_status TEXT, 
     recommended_sightseeing_time VARCHAR(100),
     phone VARCHAR(100),
     address TEXT,
     PRIMARY KEY(id)
);
```

```
create table attraction_and_review(
     attraction_id INT NOT NULL,
     review_id INT NOT NULL
     );
```

```
create table review(
     id INT NOT NULL AUTO_INCREMENT,
     content TEXT,
     PRIMARY KEY (id)
     );
```