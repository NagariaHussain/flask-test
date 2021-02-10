DROP TABLE IF EXISTS Product;
DROP TABLE IF EXISTS Location;
DROP TABLE IF EXISTS ProductMovement;

-- Create the product table
CREATE TABLE Product (product_id TEXT PRIMARY KEY);

-- Create the location table
CREATE TABLE Location (location_id TEXT PRIMARY KEY);

-- Create product movement table
CREATE TABLE ProductMovement (
    movement_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, 
    from_location TEXT, 
    to_location TEXT, 
    product_id TEXT NOT NULL, 
    qty INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES Product (product_id)
);