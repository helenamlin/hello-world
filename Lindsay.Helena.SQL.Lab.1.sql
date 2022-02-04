# 1.	Write a query to get Product name and quantity/unit.  
SELECT northwind.products.product_name, northwind.products.quantity_per_unit
FROM northwind.products;

#2. Write a query to get current Product list (Product ID and name).  
SELECT id, product_name
FROM products
WHERE Discontinued = "False"
ORDER BY product_name;

#3. Write a query to get discontinued Product list (Product ID and name). 
SELECT id , product_name
FROM products
WHERE Discontinued = 1 
ORDER BY product_name;

#4. Write a query to get most expense and least expensive Product list (name and unit price).  
SELECT product_name, list_price
FROM products
WHERE list_price IN
(SELECT MAX(list_price)
FROM products)
UNION
SELECT product_name, list_price
FROM products
WHERE list_price IN
(SELECT MIN(list_price)
FROM products);

#5. Write a query to get Product list (id, name, unit price) where current products cost less than $20.  
SELECT id, product_name, list_price
FROM products
WHERE (((list_price)<20) AND ((Discontinued)=False))
ORDER BY list_price DESC;

#6. Write a query to get Product list (id, name, unit price) where products cost between $15 and $25.  
SELECT id, product_name, list_price
FROM products
WHERE (((list_price)>=15 And (list_price)<=25) 
AND ((Discontinued)=False))
ORDER BY list_price DESC;

#7. Write a query to get Product list (name, unit price) of above average price.  
SELECT product_name, list_price
FROM products
WHERE list_price > (SELECT avg(list_price) FROM products)
ORDER BY list_price;

#8. Write a query to get Product list (name, unit price) of ten most expensive products.  
SELECT product_name, list_price
FROM products
ORDER BY list_price DESC
LIMIT 10;

#9. Write a query to count current and discontinued products. 
SELECT Count(product_name)
FROM products
GROUP BY Discontinued;

#10. Write a query to get Product list (name, units on order, units in stock) of stock is less than the quantity on order.  
SELECT product_name,  reorder_level , target_level
FROM products
WHERE (((Discontinued)=False) AND ((reorder_level)<target_level));












