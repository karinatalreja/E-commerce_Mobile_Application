from connection import mydb

mycursor = mydb.cursor()

#########################################################################
#  CREATING TABLE ACCOUNT FOR CUSTOMER FOR LOGIN CREDENTIALS CHECK      #
#  Table Name = Account                                                 #
#  cust_id = Primary Key (Auto-Generated)                               #
#  name = Customer Name                                                 #
#  email = Customer Email                                               #
#  password = Customer Password                                         #
#########################################################################
mycursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Account
    (
        cust_id INT PRIMARY KEY AUTO_INCREMENT, 
        name VARCHAR(255), 
        email VARCHAR(255) NOT NULL UNIQUE, 
        password VARCHAR(15) NOT NULL
    )
    """
)

##########################################################################
#  CREATING CUSTOMER TABLE TO STORE THE PROFILE DETAILS OF THE CUSTOMER  #
#  Table Name = Customer                                                 #
#  cust_id = Primary Key (Foreign Key from Account Table)                #
#  name = Customer Name                                                  #
#  email = Customer Email                                                #
#  mob_num = Customer Mobile Number                                      #
#  address = Customer Address                                            #
#  city = Customer City                                                  #
#  state = Customer State                                                #
#  pincode = Customer Pincode                                            #
##########################################################################

mycursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Customer 
    (
        cust_id INT,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        mob_num VARCHAR(15) NOT NULL,
        address VARCHAR(255) NOT NULL,
        city VARCHAR(100) NOT NULL,
        state VARCHAR(100) NOT NULL,
        pincode VARCHAR(10) NOT NULL,
        FOREIGN KEY (cust_id) REFERENCES Account(cust_id) ON DELETE CASCADE
    )
    """
)

#########################################################################
#  CREATING TABLE CATEGORY FOR STORING TYPE OF CATEGORIES               #
#  Table Name = Category                                                #
#  category_id = Primary Key                                            #
#  category_name = Category Name                                        #
#  Number of Items = Number of Items each category has                  #
#  Description = Description of the category                            #
#  Image_url = Image url to show on webpage                             #
#########################################################################
mycursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Category 
    (
        category_id VARCHAR(5) Primary Key,
        category_name VARCHAR(255) NOT NULL UNIQUE,
        number_of_items INT NOT NULL,
        description VARCHAR(255) NOT NULL,
        image_url VARCHAR(255) NOT NULL
    )
    """  
)


#########################################################################
#  CREATING TABLE Item FOR ITEM Information                             #
#  Table Name = ITEM                                                    #
#  item_id = Primary Key                                                #
#  item_name = Item Name                                                #
#  Number of Items = Number of Items each category has                  #
#  Description = Description of the category                            #
#  Image_url = Image url to show on webpage                             #
#########################################################################
mycursor.execute(
    """
   CREATE TABLE IF NOT EXISTS Item (
    item_id VARCHAR(10) PRIMARY KEY,
    item_name VARCHAR(255) NOT NULL,
    category_id Varchar(5),
    FOREIGN KEY (category_id) REFERENCES Category(category_id),
    price DECIMAL(10, 2) NOT NULL,
    unit VARCHAR(50) NOT NULL,
    available_units INT NOT NULL,
    sold_unit INT DEFAULT 0,
    status ENUM('active', 'discontinued', 'out_of_stock') DEFAULT 'active',
    image_url VARCHAR(255) NOT NULL
);

    """
    
)


mycursor.execute(
    """
        CREATE TABLE Orders 
        (
            order_id INT PRIMARY KEY AUTO_INCREMENT,
            customer_id INT,
            FOREIGN KEY (customer_id) REFERENCES Customer(cust_id),
            order_date DATETIME NOT NULL,
            total_amount DECIMAL(10, 2) NOT NULL,
            status ENUM('pending', 'processing', 'shipped', 'delivered') DEFAULT 'pending',
            payment_method VARCHAR(50),
            payment_status ENUM('pending', 'paid') DEFAULT 'pending' 
);

    """
)




