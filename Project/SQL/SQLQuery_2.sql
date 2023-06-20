SELECT ord_dets.pizza_id
        ,ord_dets.quantity
        ,ord.date
        ,ord.time
        ,price.size 
        ,price.price 
        ,types.category
    from pizza_order_details ord_dets
        LEFT JOIN pizza_orders ord
            ON ord_dets.order_id = ord.order_id
        LEFT JOIN pizza_prices price
            ON ord_dets.pizza_id = price.pizza_id
        LEFT JOIN pizza_types types
            ON price.pizza_type_id = types.pizza_type_id