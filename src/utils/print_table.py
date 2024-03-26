# from prettytable import PrettyTable
# from utils.config import prompts


# def view_user_account(obj):
#     """
#     function to print user details
#     """
#     result = [obj.name, obj.username, obj.phone, obj.address, obj.city, obj.state, obj.pincode]
#     table = PrettyTable()    
#     table.field_names = ["NAME", "USERNAME", "PHONE", "ADDRESS", "CITY", "STATE", "PINCODE"]
#     if result:    
#         table.add_row([result[0], result[1], result[2], result[3], result[4], result[5], result[6]])
#     table.align = "l"
#     table.max_width["Address"] = 15
#     table.max_width["Pincode"] = 19   
#     print(table)
#     return
        

# def view_requests(details):
#     """
#     function to view seller accounts for delete request
#     """
#     if details:
#         table = PrettyTable()
#         table.field_names = ["USERNAME", "STATUS"]
#         for detail in details:
#             table.add_row([detail[1], detail[2]])
#         table.align = "l"
#         table.max_width["Username"] = 5
#         table.max_width["Status"] = 10 
#         print(table)
#         return
#     else:
#         print(prompts["NO_REQUESTS"])

    
# def print_users(users):
#         table = PrettyTable()
#         table.field_names = ["USERNAME", "NAME", "PHONE", "ADDRESS", "CITY", "STATE", "PINCODE"]
#         for user in users:
#             table.add_row([user[7], user[1], user[2], user[3], user[4], user[5], user[6]])
#         table.align = "l"
#         table.max_width["Address"] = 15
#         table.max_width["Pincode"] = 19 
#         print(table)
#         return

    
# def list_products(products):
#     """
#     function to list all Products of that sellers
#     """
#     if products:
#         table = PrettyTable()    
#         table.field_names = ["PRODUCT_ID", "DESCRIPTION", "PRICE", "CATEGORY", "GENDER", "SIZE", "QUANTITY"]
#         for product in products:
#             table.add_row([product[1], product[3], product[4], product[6], product[7], product[8], product[9]])
#         table.align = "l"
#         table.max_width["Category"] = 10
#         table.max_width["Quantity"] = 16
#         print(table)    
#         return
#     else:
#         print(prompts["NO_PRODUCT_FOUND"])

        
# def view_products(products):
#     """
#     function to view Products to customers
#     """
#     if products:
#         table = PrettyTable()    
#         table.field_names = ["PRODUCT_ID", "DESCRIPTION", "PRICE", "CATEGORY", "GENDER", "SIZE"]
#         for product in products:
#             table.add_row([product[1], product[3], product[4], product[6], product[7], product[8]])
#         table.align = "l"
#         table.max_width["Price"] = 10
#         table.max_width["Size"] = 16
#         print(table)    
#         return
#     else:
#         print(prompts["NO_PRODUCT_FOUND"])
        

# def seller_orders(orders):
#     """
#     function to view all the Products of that particular seller
#     """
#     if orders:
#         table = PrettyTable()    
#         table.field_names = ["ORDER_ID", "USERNAME", "PRODUCT_ID", "QUANTITY", "STATUS", "ORDER_DATE"]
#         for order in orders:
#             table.add_row([order[0], order[2], order[4], order[5], order[7], order[8]])
#         table.align = "l"
#         table.max_width["Quantity"] = 15
#         table.max_width["Order Date"] = 19   
#         print(table)
#     else:
#         print(prompts["NO_ORDER"])

        
# def customer_orders(orders):
#     """
#     function to view all orders of the customer
#     """
#     if orders:
#         table = PrettyTable()    
#         table.field_names = ["ORDER_ID", "PRODUCT_ID", "QUANTITY", "STATUS", "ORDER_DATE"]
#         for order in orders:
#             table.add_row([order[0], order[4], order[5], order[7], order[8]])
#         table.align = "l"
#         table.max_width["Quantity"] = 15
#         table.max_width["Order Date"] = 19   
#         print(table)
#     else:
#         print(prompts["NO_ORDER"])  
        

# def print_seller_orders(products):
#     """
#     function to print all sellers Products
#     """
#     if products:
#         table = PrettyTable()
#         table.field_names = ["PRODUCT_ID", "QUANTITY", "STATUS"]
#         for product in products:
#             table.add_row([product[0], product[1], product[2]])
#         table.align = "l"
#         table.max_width["Quantity"] = 5
#         table.max_width["Status"] = 10
#         print(table)
#     else:
#         print("\nNo Products found!\n")