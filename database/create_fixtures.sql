CREATE TABLE IF NOT EXISTS orac_scrap_be (
    id BIGINT,
    line BIGINT, 
    amount BIGINT,
    reason Text,
    opmerking Text,
    timestamp DATETIME,
    foto Text
);