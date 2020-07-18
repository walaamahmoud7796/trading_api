DROP TABLE IF EXISTS Transactions;
-- DROP TABLE IF EXISTS post;

CREATE TABLE Transactions (
			user_id VARCHAR(22),
			amount DECIMAL,
			type VARCHAR(22),
			transaction_timestamp timestamp);