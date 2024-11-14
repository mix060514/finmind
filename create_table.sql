CREATE TABLE `financialdata`.`TaiwanStockPrice` (
    `stock_id` VARCHAR(10) NOT NULL,
    `trade_volume` BIGINT NOT NULL,
    `transactions` INT NOT NULL,
    `trade_value` BIGINT NOT NULL,
    `open` FLOAT NOT NULL,
    `max` FLOAT NOT NULL,
    `min` FLOAT NOT NULL,
    `close` FLOAT NOT NULL,
    `change` FLOAT NOT NULL,
    `date` DATE NOT NULL,
    PRIMARY KEY (`stock_id`, `date`)
)
