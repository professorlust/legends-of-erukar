from pg import DB

pwd = input('Enter your password: ')

db = DB(dbname='loedev', user='postgres', passwd=pwd)
db.query("create table players(uid varchar primary key, name varchar)")
db.query("create table items(id serial primary key, name varchar, material varchar)")
db.query("create table modifiers(id serial primary key, weapon_id integer REFERENCES items, class_name varchar)")
db.query("create table characters(id serial primary key, player_id varchar REFERENCES players, name varchar, max_health smallint, health smallint, strength smallint, dexterity smallint, vitality smallint, acuity smallint, sense smallint, resolve smallint, level smallint, xp integer, equipment integer REFERENCES items, inventory integer REFERENCES items)")
db.query("create table effects(id serial primary key, character_id integer REFERENCES characters, class_name varchar)")


'''
USEFUL COMMANDS

SELECT * FROM characters INNER JOIN players ON characters.player_id=players.uid;

'''
