# DataBases-Homework-2
Second practise assignment 

my query is finding top 100 active clients by order count in product categories



-- non-optimized query--
explain analyze
select
    c.client_id,
    c.first_name,
    c.last_name,
    p.category,
    count(o.order_id) as orders_count,
    sum(o.quantity) as total_quantity
from orders o
join clients c on o.client_id = c.client_id
join products p on o.product_id = p.product_id
where o.order_date >= date '2024-01-01' and c.status = 'active'
group by
    c.client_id,
    c.first_name,
    c.last_name,
    p.category
order by
    orders_count desc,
    total_quantity desc
limit 100;



# -- indexes--

create index if not exists idx_orders_order_date on orders(order_date);
-- цей індекс має допомогти знайти замовлення швидше по потрібній даті--

create index if not exists idx_orders_client_id on orders(client_id);
-- цей індекс потрібен щоб замовлення швидше з'єднувалось з клієнтом, ну наприклад щоб знайти всі замовлення конкретного клієнта--

create index if not exists idx_orders_product_id on orders(product_id);
--цей індекс допоможе перевірити скільки разів купували конкретний товар--

create index if not exists idx_clients_status on clients(status);
-- цей індекс допоможе у випадку коли треба вибрати тільки активних або ні клієнтів--



--optimized query
set enable_seqscan = off;

explain analyze
with filtered_orders as (
    select
        o.order_id,
        o.quantity,
        c.client_id,
        c.first_name,
        c.last_name,
        p.category
    from orders o
    join clients c on o.client_id = c.client_id
    join products p on o.product_id = p.product_id
    where o.order_date >= date '2024-01-01'
      and c.status = 'active'
)
select
    client_id,
    first_name,
    last_name,
    category,
    count(order_id) as orders_count,
    sum(quantity) as total_quantity
from filtered_orders
group by
    client_id,
    first_name,
    last_name,
    category
order by
    orders_count desc,
    total_quantity desc
limit 100;

reset enable_seqscan;


# Actual time before optimisation is 7.832 ms

<img width="279" height="133" alt="image" src="https://github.com/user-attachments/assets/0d7599e3-4c59-4f0d-b6f8-af708be78169" />

#Time-result after optimization

<img width="346" height="129" alt="image" src="https://github.com/user-attachments/assets/096830d8-a68b-4521-8910-332acf828cad" />

# Output of optimized query:

<img width="731" height="602" alt="image" src="https://github.com/user-attachments/assets/657c41a9-5664-4807-84ab-8b3b256d5207" />

# Output of non-optimized query:

<img width="798" height="543" alt="image" src="https://github.com/user-attachments/assets/9125963f-8da1-4446-9445-6d72c0579b3d" />

