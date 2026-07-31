drop database if exists vegan_cook_website;
create database vegan_cook_website;
use vegan_cook_website;


create table category(
    category_id int auto_increment primary key,
    cat_name varchar(255) unique not null
);


create table ingredient(
    ingredient_id int auto_increment primary key,
    ing_name varchar(255) unique not null
);

create table origin(
    origin_id int auto_increment primary key,
    ori_name varchar(255) not null
);


create table user(
    user_id int auto_increment primary key,
    user_name varchar(255) unique not null,
    user_email varchar(255) not null,
    user_password varchar(255) not null
);

create table recipe(
    recipe_id int auto_increment primary key,
    rec_name varchar(255) not null,
    rec_description text not null,
    rec_instructions text not null,
    rec_image_url varchar(255) not null,
    rec_time integer not null,
    author_id int not null,
    origin_id int not null,
    foreign key (author_id) references user(user_id),
    foreign key (origin_id) references origin(origin_id)
);

create table recipe_category(
    recipe_id int not null,
    category_id int not null,
    primary key (recipe_id, category_id),
    foreign key (recipe_id) references recipe(recipe_id),
    foreign key (category_id) references category(category_id)
);

create table saved_recipe(
    user_id int not null,
    recipe_id int not null,
    primary key (user_id, recipe_id),
    foreign key (user_id) references user(user_id),
    foreign key (recipe_id) references recipe(recipe_id)
);


create table rating(
    user_id int not null,
    recipe_id int not null,
    rating_value int not null,
    primary key (user_id, recipe_id),
    foreign key (user_id) references user(user_id),
    foreign key (recipe_id) references recipe(recipe_id)
);



create table recipe_ingredient(
    recipe_id int not null,
    ingredient_id int not null,
    quantity varchar(255) not null,
    quantity_unit varchar(255) not null,
    primary key (recipe_id, ingredient_id),
    foreign key (recipe_id) references recipe(recipe_id),
    foreign key (ingredient_id) references ingredient(ingredient_id)
);


show tables;