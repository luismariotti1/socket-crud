# Protocol Rules

## CRUD with sockets and HTTP

## Operators

### `1` = create
### `2` = read
### `3` = update
### `4` = delete
### `5` = exit

## Data Types

### `1` = string
### `2` = integer
### `3` = float

## Stop Code

### `0` = stop


# Message Format

## Create

### Op + Type + Key + Value

## Read

### Op

## Update

### Op + id + Type + Key + Value

## Delete

### Op + id

# example

## create

### 1 1 "name" "Picachu" 2 "hp" 100

## read

### 2

## update

### 3 1 2 "age" 3

## delete

### 4 1