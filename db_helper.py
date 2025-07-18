import mysql.connector
global cnx

cnx = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="root",
    database="pandeyji_eatery"
)
#---------------------------------------------------------------------------------------
def insert_order_item(food_item, quantity, order_id):
    try:
        cursor = cnx.cursor()

        # Calling the stored procedure
        cursor.callproc('insert_order_item', (food_item, quantity, order_id))

        # Committing the changes
        cnx.commit()

        # Closing the cursor
        # cursor.close()

        print("Order item inserted successfully!")

        return 1

    except mysql.connector.Error as err:
        print(f"Error inserting order item: {err}")

        # Rollback changes if necessary
        cnx.rollback()

        return -1

    except Exception as e:
        print(f"An error occurred: {e}")
        # Rollback changes if necessary
        cnx.rollback()

        return -1


#--------------------------------------------------------------------------------------------
# Function to fetch the order status from the order_tracking table
def get_order_status(order_id):
    cursor = cnx.cursor()

    # Executing the SQL query to fetch the order status
    query = f"SELECT status FROM order_tracking WHERE order_id = {order_id}"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()


    # Returning the order status
    if result:
        return result[0]
    else:
        return None

#---------------------------------------------------------------------------------
# Function to get the next available order_id
def get_next_order_id():
    cursor = cnx.cursor()

    # Executing the SQL query to get the next available order_id
    query = "SELECT MAX(order_id) FROM orders"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()[0]


    # Returning the next available order_id
    if result is None:
        return 1
    else:
        return result + 1


#-------------------------------------------------------------------------

def get_total_order_price(order_id):
    cursor = cnx.cursor()

    # Executing the SQL query to get the total order price
    query = f"SELECT get_total_order_price({order_id})"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()[0]


    return result

#-----------------------------------------------------------------------------
# Function to insert a record into the order_tracking table
def insert_order_tracking(order_id, status):
    cursor = cnx.cursor()

    # Inserting the record into the order_tracking table
    insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
    cursor.execute(insert_query, (order_id, status))

    # Committing the changes
    cnx.commit()


#--------------------------------------------------------------------------------------------
def get_order_summary(order_id):
    try:
        cursor = cnx.cursor()

        # SQL query to join orders and food_items
        query = """
            SELECT fi.name, o.quantity, fi.price, (o.quantity * fi.price) AS total_price
            FROM orders o
            JOIN food_items fi ON o.item_id = fi.item_id
            WHERE o.order_id = %s
        """
        cursor.execute(query, (order_id,))
        results = cursor.fetchall()

        # Format results
        summary = []
        for name, quantity, price, total in results:
            summary.append({
                "name": name,
                "quantity": quantity,
                "unit_price": price,
                "total_price": total
            })

        return summary

    except mysql.connector.Error as err:
        print(f"Error fetching order summary: {err}")
        return None



