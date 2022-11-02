create table Users(
  Id SERIAL primary key,
  login varchar(50) not null constraint must_be_unique unique,
  password varchar(128) not null ,
  email varchar(128) not null,
  name_user varchar(50) not null,
  surname varchar(50) not null,
  role boolean default false
);

create table Administrators(
  Id SERIAL primary key,
  user_id integer not null,
  foreign key (user_id) references Users (Id) on delete CASCADE
);

create table Actioneers(
  Id SERIAL primary key,
  user_id integer not null,
  education varchar(128),
  foreign key (user_id) references Users (Id) on delete CASCADE
);

create table Reviewers(
  Id SERIAL primary key,
  user_id integer not null,
  education varchar(128),
  foreign key (user_id) references Users (Id) on delete CASCADE
);

create table Authors(
  Id SERIAL primary key,
  user_id integer not null,
  date_of_birth date,
  genre varchar(50) ARRAY,
  education varchar(128),
  foreign key (user_id) references Users (Id) on delete CASCADE
);

create table Owners(
  Id SERIAL primary key,
  user_id integer not null,
  work varchar(128),
  foreign key (user_id) references Users (Id) on delete CASCADE
);

create table Reviews(
  Id SERIAL primary key,
  rev_id INTEGER not null,
  pick_id INTEGER not null,
  message text not null,
  date_of_review date,
  foreign key (rev_id) references Reviewers (Id) on delete cascade,
  foreign key (pick_id) references Pictures (Id) on delete cascade
);

create table Pictures(
  Id SERIAL primary key,
  auth_id INTEGER not null,
  owner_id INTEGER not null,
  cost_pick INTEGER default 0,
  name_pick varchar(50),
  genre varchar(50),
  date_of_create date,
  foreign key (auth_id) references Authors (Id) on delete cascade,
  foreign key (owner_id) references Owners (Id) on delete cascade 
);

create table Auctions(
  Id SERIAL primary key,
  date_of_action date,
  auctioneer_id INTEGER not null,
  status_apll BOOLEAN default false,
  foreign key (auctioneer_id) references Auctioneers (Id) on delete cascade
);

create table Application_Auction(
  Id SERIAL primary key,
  auction_id INTEGER not null,
  admin_id INTEGER,
  status boolean default false,
  foreign key (admin_id) references Administrators (Id),
  foreign key (auction_id) references Auctions (Id) on delete cascade 
);

create table Auction_Buyers(
  Id SERIAL primary key,
  auction_id INTEGER,
  owner_id INTEGER,
  foreign key (auction_id) references Auctions (Id) on delete cascade,
  foreign key (owner_id) references Owners (Id) on delete cascade
)

create table Auction_Pictures( 
  Id SERIAL primary key, 
  auction_id INTEGER not null,
  pick_id INTEGER not null,
  foreign key (auction_id) references Auctions (Id) on delete cascade,
  foreign key (pick_id) references Pictures (Id) on delete cascade
);

CREATE TYPE role_change AS ENUM ('author', 'actioneer', 'reviewer', 'owner');

create table Applications(
  Id SERIAL primary key,
  user_id INTEGER not null,
  admin_id INTEGER,
  variant_request role_change,
  status BOOLEAN default false,
  foreign key (user_id) references Users (Id) on delete cascade,
  foreign key (admin_id) references Administrators (Id) 
);