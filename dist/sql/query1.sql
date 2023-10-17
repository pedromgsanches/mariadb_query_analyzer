select ol.ol_w_id, ol.ol_d_id, ol.ol_number, ol.ol_amount, o.o_id, o.o_w_id, o.o_carrier_id, c.c_id, c.c_first, c.c_last, c.c_city, c.c_state 
from
order_line ol
inner join orders o on o.o_id = ol.ol_o_id
inner join customer c on c.c_id = o.o_c_id
where c.c_id in (7,12,20,44,55,400)
order by 1,2,3