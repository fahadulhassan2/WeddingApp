"""This is the main flask python file"""
import os
import imghdr
from smtplib import SMTPAuthenticationError

from flask import Flask, flash, request, render_template, redirect, url_for, session, g,send_from_directory
import seed
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from WEBSITE_INFORMATION import WEBSITE_INFORMATION
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import WeddingClass as wedding

person = wedding.WeddingClass()

app = Flask(__name__)

# Database Details
app.config['MYSQL_HOST'] = seed.host
app.config['MYSQL_USER'] = seed.user
app.config['MYSQL_PASSWORD'] = seed.password
app.config['MYSQL_PORT'] = seed.port
app.config['MYSQL_DB'] = seed.db_name

# EMAIL SMTP DETAILS
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = "legendbest123@gmail.com"
app.config['MAIL_PASSWORD'] = "sefnbvaevoctmmav"
app.config['MAIL_DEFAULT_SENDER'] = "legendbest123@gmail.com"
app.config['MAIL_ASCII_ATTACHMENTS'] = False

# SECRET KEY

app.secret_key = seed.secret_key
# token_key = URLSafeTimedSerializer(seed.secret_key)


mysql = MySQL(app)
mail = Mail(app)


# FOR HOME PAGE #
####################################
# BACKEND: COMPLETED
# FRONTEND:
####################################


@app.route("/")
def index():
    if 'username' in session:
        g.email = session['username']
        return redirect(url_for('dashboard'))
    return render_template("login.html")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@app.route("/registration", methods=['GET'])
def registration():
    if 'username' in session:
        g.email = session['username']
        return redirect(url_for('dashboard'))

    else:
        return render_template("registration.html")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@app.route("/process-registration", methods=['POST'])
def process_registration():
    if 'username' in session:
        g.username = session['username']
        return redirect(url_for('dashboard'))
    elif request.method == 'POST':
        person.dateOfMarriage = request.form["inputDateOfMarriage"]
        person.endDateOfMarriage = request.form["inputEndDateOfMarriage"]
        person.timeOfMarriage = request.form["inputTimeOfMarriage"]
        person.endTimeOfMarriage = request.form["inputEndTimeOfMarriage"]
        person.Location = request.form["inputLocation"]
        person.Address = request.form["inputAddress"]
        person.groomFirstName = request.form["inputFirstName1"]
        person.groomLastName = request.form["inputLastName1"]
        person.brideFirstName = request.form["inputFirstName2"]
        person.brideLastName = request.form["inputLastName2"]

        person.username = request.form["inputUsername"]
        person.email = request.form["inputEmail"]
        person.password = request.form["inputPassword"]
        person.contactNumber = request.form["inputContact"]

        print(person.dateOfMarriage+" "+person.endDateOfMarriage)
        print(person.Location+" "+person.Address)
        hashedPassword = generate_password_hash(person.password)
        try:

            # Email sent to the user
            try:

                msg = Message('Welcome to The Wedding Application',
                              sender="legendbest123@gmail.com", recipients=[person.email])

                msg.body = 'Your Account is created'

                cur = mysql.connection.cursor()
                cur.execute(
                    "INSERT INTO weddingInformation(groomFirstName,groomLastName,brideFirstName,brideLastName,dateOfMarriage,timeOfMarriage,endDateOfMarriage,endTimeOfMarriage,locationName,address,username,email,contactNumber,password) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (person.groomFirstName, person.groomLastName, person.brideFirstName, person.brideLastName,
                     person.dateOfMarriage,person.timeOfMarriage,person.endDateOfMarriage,person.endTimeOfMarriage, person.Location,person.Address, person.username, person.email, person.contactNumber,
                     hashedPassword))
                mail.send(msg)
                mysql.connection.commit()
                cur.close()
                flash("Successfully Registered", "success")
                print("Successfull")
                return redirect(url_for("login"))

            except Exception as e:
                print(e)
                
                flash("Email or username not valid", "danger")
                return redirect(url_for("login"))
            # ----------------------------

        except:
            print("Server issue")

            flash("Server is busy", "warning")
            return redirect(url_for("login"))
    else:
        flash("Session Ended", "warning")
        return redirect(url_for("login"))


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'username' in session:
        g.username = session['username']
        return redirect(url_for('dashboard'))

    elif request.method == 'POST':

        # login check over here if it is done go to dashboard
        #
        #
        #

        session.pop('username', None)
        session.pop('email', None)
        username = request.form['username']
        password = request.form['password']
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                '''SELECT groomFirstName,groomLastName,brideFirstName,brideLastName,dateOfMarriage,timeOfMarriage,endDateOfMarriage,endTimeOfMarriage,locationName,address,username,email,contactNumber,password FROM weddingInformation WHERE username=%s''',
                (username,))
            person = cur.fetchone()
            if person is None:
                flash("Username Incorrect", "danger")
                return render_template("login.html")
            else:
                if check_password_hash(person[13], password):
                    session['groomFirstName'] = person[0]
                    session['groomLastName'] = person[1]
                    session['brideFirstName'] = person[2]
                    session['brideLastName'] = person[3]
                    session['dateOfMarriage'] = person[4]
                    session['timeOfMarriage'] = person[5]
                    session['endDateOfMarriage'] = person[6]
                    session['endTimeOfMarriage'] = person[7]
                    session['Location'] = person[8]
                    session['Address'] = person[9]
                    session['username'] = person[10]
                    session['email'] = person[11]
                    session['contactNumber'] = person[12]

                    cur.execute('''SELECT templateNo,url FROM website where username = %s''',(session['username'],))
                    result=cur.fetchone()
                    if result is None:
                        # no template and url has yet set
                        pass
                    else:
                        session['template_id'] = result[0]
                        session['url'] = result[1]

                    

                    cur.execute(
                        '''SELECT count(guest_name) FROM guests where username = %s''',
                        (session['username'],))
                    countedGuests = cur.fetchone()
                    session['guests'] = countedGuests[0]
                    cur.execute("SELECT count(itemName) FROM item_cart where username=%s", (session['username'],))
                    registries = cur.fetchone()
                    session['registries'] = registries[0]
                    mysql.connection.commit()
                    return redirect(url_for('dashboard'))
                else:
                    # Password error
                    flash("Password Incorrect", "danger")
                    return render_template("login.html")
        except:
            flash("Server is busy", "danger")
            return render_template("login.html")

    else:
        return render_template("login.html")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if 'username' in session:
        g.username = session['username']
        return render_template("dashboard.html", session=session)
    else:
        flash("Session Ended", "warning")
        return render_template("login.html")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@app.route("/vendors", methods=['GET'])
def vendors():
    if 'username' in session:
        g.username = session['username']
        # Select all query

        if request.args.get('city') or request.args.get('category'):
            category = request.args.get('category')
            city = request.args.get('city')
            if (city == "All Cities"):
                city = "%"
            if (category == "All Categories"):
                category = "%"
            vendors: list = []
            categoryList: list = []
            cities: list = []
            cur = mysql.connection.cursor()

            # vendor details
            cur.execute(
                '''SELECT Image,Name,Category,Location,vendor_id FROM categories where Location LIKE %s AND Category LIKE %s''',
                (city, category))
            vendors_list = cur.fetchall()
            mysql.connection.commit()

            # Categories fetching from database
            cur.execute(
                '''SELECT  category_name  FROM categories_list''', )
            categories_list = cur.fetchall()

            mysql.connection.commit()

            # Cities fetching from database
            cur.execute(
                '''SELECT  Cities  FROM Cities''', )
            Cities = cur.fetchall()

            mysql.connection.commit()
            cur.close()

            for category in categories_list:
                categoryList.append(category)

            for vendor in vendors_list:
                vendors.append(vendor)

            for city in Cities:
                cities.append(city)
            return render_template("vendors.html", vendors=vendors, categories=categoryList, cities=cities)

        else:
            vendors: list = []
            categoryList: list = []
            cities: list = []
            cur = mysql.connection.cursor()

            # vendor details
            cur.execute(
                '''SELECT Image,Name,Category,Location,vendor_id FROM categories''', )
            vendors_list = cur.fetchall()
            mysql.connection.commit()

            # Categories fetching from database
            cur.execute(
                '''SELECT  category_name  FROM categories_list''', )
            categories_list = cur.fetchall()

            mysql.connection.commit()

            # Cities fetching from database
            cur.execute(
                '''SELECT  Cities  FROM Cities''', )
            Cities = cur.fetchall()

            mysql.connection.commit()
            cur.close()

            for category in categories_list:
                categoryList.append(category)

            for vendor in vendors_list:
                vendors.append(vendor)

            for city in Cities:
                cities.append(city)
            return render_template("vendors.html", vendors=vendors, categories=categoryList, cities=cities)

            return render_template("vendors.html")
    else:
        flash("Session Ended", "warning")
        return render_template("login.html")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@app.route("/vendor-category", methods=['GET', 'POST'])
def VendorCategory():
    if 'username' in session:
        g.username = session['username']
        if request.args['id']:
            id = request.args['id']
            cur = mysql.connection.cursor()

            # vendor details
            cur.execute(
                '''SELECT * FROM categories where vendor_id = %s''', [id])

            vendor = cur.fetchone()
            mysql.connection.commit()
            cur.close()
            return render_template("vendor-category.html", vendor=vendor)
        else:
            return render_template("vendors.html")
    else:
        flash("Session Ended", "warning")
        return render_template("login.html")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@app.route("/guestslist", methods=['GET', 'POST'])
def guestslist():
    if 'username' in session:
        if request.method == "GET":
            g.username = session['username']

            Guests: list = []

            cur = mysql.connection.cursor()

            # vendor details
            cur.execute(
                '''SELECT id,GuestNames,street_address,AptFloor,City,Country,StateProvince,ZipCode,Invited,email,phone,Status,Reply,Total FROM guests where username = %s''',
                (session['username'],))
            guestsData = cur.fetchall()
            mysql.connection.commit()
           
            status = []
            replied = 0
            Attending = 0
            Not_Attending = 0
            Maybe = 0
            Invited = 0
            Not_Invited = 0

            for guest in guestsData:
                Guests.append(guest)

            cur.execute(
                '''SELECT status,Reply FROM guestInfo where username = %s''',
                (session['username'],))
            statusData = cur.fetchall()
            
            mysql.connection.commit()
            cur.close()
            for st in statusData:
                if st[1] == "Not Replied":
                    replied= replied + 1
                
                if st[1] == "Attending":
                    Attending = Attending + 1
                
                if st[1] == "Not Attending":
                    Not_Attending = Not_Attending + 1
                
                if st[1] == "Maybe":
                    Maybe = Maybe + 1
                
                if st[0] == "Invited":
                    Invited = Invited +  1 
                
                if st[0] == "Not Invited":
                    Not_Invited = Not_Invited + 1 

            status.append(replied)
            status.append(Attending)
            status.append(Not_Attending)
            status.append(Maybe)
            status.append(Invited)
            status.append(Not_Invited)
            return render_template("guestslist.html", Guests=Guests,status = status)


    ## Here we will add post request for form submission 
        elif request.method == 'POST':
            if (request.form['action'] == 'AddRow'):
                opt = request.form['opt'];
                if opt == "1":
                    firstName1 = request.form['inputFirstName1']
                    lastName1 = request.form['inputLastName1']
                    title1 = request.form['inputTitle1']
                    GuestNames = title1+" "+firstName1+" "+lastName1

                elif opt == "2":
                    firstName1 = request.form['inputFirstName1']
                    lastName1 = request.form['inputLastName1']
                    title1 = request.form['inputTitle1']
                    firstName2 = request.form['inputFirstName2']
                    lastName2 = request.form['inputLastName2']
                    title2 = request.form['inputTitle2']
                    GuestNames = title1+" "+firstName1+" "+lastName1+","+title2+" "+firstName2+" "+lastName2

                elif opt == "3":
                    firstName1 = request.form['inputFirstName1']
                    lastName1 = request.form['inputLastName1']
                    title1 = request.form['inputTitle1']
                    firstName2 = request.form['inputFirstName2']
                    lastName2 = request.form['inputLastName2']
                    title2 = request.form['inputTitle2']
                    firstName3 = request.form['inputFirstName3']
                    lastName3 = request.form['inputLastName3']
                    title3 = request.form['inputTitle3']
                    GuestNames = title1+" "+firstName1+" "+lastName1+","+title2+" "+firstName2+" "+lastName2+","+title3+" "+firstName3+" "+lastName3
                
                invited = request.form['invited']
                email = request.form['inputEmail']
                street_address = request.form['inputStreetAddress']
                AptFloor = request.form['inputAptFloor']
                City = request.form['inputCity']
                Country = request.form['inputCountry']
                StateProvince = request.form['inputStateProvince']
                ZipCode = request.form['inputZipCode']
                phone = request.form['inputContactNumber']
                status = "Not Invited"
                Reply = "Not Replied"
                # Email sent to the user
                try:
                        cur = mysql.connection.cursor()
                        cur.execute(
                            "INSERT INTO guests(GuestNames,street_address,AptFloor,City,Country,StateProvince,ZipCode,email,phone,Status,invited,Reply,Total,username) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            (GuestNames,street_address,AptFloor,City,Country,StateProvince,ZipCode,email,phone,status,invited,Reply,int(opt),session['username']))
                    
                        
                        # Maintain Guest Info table for using it when we deal with guest seats
                        if opt == "1":
                            cur.execute(
                                "INSERT INTO guestInfo(Title,First_Name,Last_Name,status,reply,username) VALUES (%s,%s,%s,%s,%s,%s)",
                                (title1,firstName1,lastName1,status,Reply,session['username']))
                        elif opt == "2":
                            cur.execute(
                                "INSERT INTO guestInfo(Title,First_Name,Last_Name,status,reply,username) VALUES (%s,%s,%s,%s,%s,%s)",
                                (title1,firstName1,lastName1,status,Reply,session['username']))
                            cur.execute(
                                "INSERT INTO guestInfo(Title,First_Name,Last_Name,status,reply,username) VALUES (%s,%s,%s,%s,%s,%s)",
                                (title2,firstName2,lastName2,status,Reply,session['username']))
                        elif opt == "3":
                            cur.execute(
                                "INSERT INTO guestInfo(Title,First_Name,Last_Name,status,reply,username) VALUES (%s,%s,%s,%s,%s,%s)",
                                (title1,firstName1,lastName1,status,Reply,session['username']))
                            cur.execute(
                                "INSERT INTO guestInfo(Title,First_Name,Last_Name,status,reply,username) VALUES (%s,%s,%s,%s,%s,%s)",
                                (title2,firstName2,lastName2,status,Reply,session['username']))
                            cur.execute(
                                "INSERT INTO guestInfo(Title,First_Name,Last_Name,status,reply,username) VALUES (%s,%s,%s,%s,%s,%s)",
                                (title3,firstName3,lastName3,status,Reply,session['username']))
                        mysql.connection.commit()
                        cur.close()
                        flash("Guest Added Successfully", "success")


                        return redirect(url_for("guestslist"))

                except Exception as e:
                        print(e)
                        flash("Error in Query", "danger")
                        return redirect(url_for("guestslist"))
                # ----------------------------
            elif (request.form['action'] == "DeleteRow"):
                ID = request.form['DeleteID']
                GuestNames = request.form['guestNames']
                print(GuestNames)
                GuestList : list = []
                GuestList = GuestNames.split(',')
                print(GuestList)

                numberOfGuests = len(GuestList)
            
                FirstName = []
                LastName = []
                title = []

                for Guest in GuestList:
                    guest = Guest.split()
                    print(guest)
                    title.append(guest[0])
                    FirstName.append(guest[1])
                    LastName.append(guest[2])

                try:
                        cur = mysql.connection.cursor()
                        cur.execute(
                            "DELETE from guests WHERE id=%s AND username=%s",
                            (ID,session['username']))
                    
                        
                        # Maintain Guest Info table for using it when we deal with guest seats
                        for i in range(numberOfGuests):
                            cur.execute(
                                    "DELETE from guestInfo where Title = %s AND First_Name = %s AND Last_Name = %s AND username = %s",
                                    (title[i],FirstName[i],LastName[i],session['username']))
                        
                        mysql.connection.commit()
                        cur.close()
                        flash("Guest Deleted Successfully", "success")


                        return redirect(url_for("guestslist"))

                except Exception as e:
                        print(e)
                        flash("Error in Query", "danger")
                        return redirect(url_for("guestslist"))

        ##--------------------------------------------------


    else:
        flash("Session Ended", "warning")
        return render_template("login.html")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response







# Items Adding To Cart

@app.route("/add-cart", methods=['GET', 'POST'])
def add_cart():
    if 'username' in session:
        g.username = session['username']

        if request.method == "GET":

            if request.args['action'] == 'addCart':

                id = request.args['id']
                cur = mysql.connection.cursor()
                # get item details here ---

                cur.execute(
                    "SELECT producttitle, productimagesrc, price,productlinkhref,product_type FROM gifts where id=%s",
                    (id,))
                item = cur.fetchone()
                mysql.connection.commit()

                itemName = item[0]
                itemImage = item[1]
                price = item[2]
                itemLink = item[3]
                product_type = item[4]
                # item adding to cart
                cur.execute(
                    "INSERT INTO item_cart(itemID,itemName,itemImage,price,itemLink,product_type,username) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                    (int(id), itemName, itemImage, price, itemLink, product_type, session['username']))

                cur.execute("SELECT count(itemName) FROM item_cart where username=%s", (session['username'],))
                registries = cur.fetchone()
                session['registries'] = registries[0]
                mysql.connection.commit()

                # for storing data into Database
                cur.close()
                flash("Successfully Added", "success")
                return redirect(url_for("Gifts"))
            else:
                return redirect(url_for("Gifts"))
        elif request.method == "POST":
            if (request.form['action'] == "addGiftToList"):
                giftUrl = request.form['giftUrl']
                giftName = request.form['giftName']
                imageURL = request.form['imageURL']
                priceGift = request.form['priceGift']
                giftCategory = request.form['giftCategory']

                cur = mysql.connection.cursor()

                cur.execute(
                    "INSERT INTO gifts( producttitle, productimagesrc, price,productlinkhref,product_type) VALUES (%s,%s,%s,%s,%s)",
                    (giftName, imageURL, priceGift, giftUrl, giftCategory))

                cur.execute("SELECT id FROM gifts where producttitle = %s",
                            (giftName,))
                item = cur.fetchone()
                item_id = int(item[0])
                cur.execute(
                    "INSERT INTO item_cart(itemID,itemName,itemImage,price,itemLink,product_type,username) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                    (item_id, giftName, imageURL, priceGift, giftUrl, giftCategory, session['username']))

                cur.execute("SELECT count(itemName) FROM item_cart where username=%s", (session['username'],))
                registries = cur.fetchone()
                session['registries'] = registries[0]

                mysql.connection.commit()
                cur.close()
                flash("Successfully Added", "success")
                return redirect(url_for("Gifts"))
            else:
                flash("You cannot access that !", "warning")
                redirect(url_for("Gifts"))

    else:

        flash("Session Ended", "warning")
        return render_template("login.html")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


# ---------------------------------------------------

# Module: Profile 
# Status: Completed

@app.route("/profile", methods=['GET', 'POST'])
def profile():
    if 'username' in session:
        g.username = session['username']
        return render_template("profile.html", session=session)
    else:
        flash("Session Ended", "warning")
        return render_template("login.html")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response




@app.route("/update_profile", methods=['GET', 'POST'])
def update_profile():
    if 'username' in session:
        if request.method == "POST":
            if (request.form['action'] == 'update_personal_information'):
                updatePerson = wedding.WeddingClass()
                updatePerson.groomFirstName = request.form["inputFirstName1"]
                updatePerson.groomLastName = request.form["inputLastName1"]
                updatePerson.brideFirstName = request.form["inputFirstName2"]
                updatePerson.brideLastName = request.form["inputLastName2"]
                updatePerson.username = session['username']
                try:
                    cur = mysql.connection.cursor()
                    cur.execute(
                        "UPDATE weddingInformation set groomFirstName=%s, groomLastName=%s,"
                        "brideFirstName=%s, brideLastName=%s WHERE username = %s",
                        (updatePerson.groomFirstName, updatePerson.groomLastName, updatePerson.brideFirstName,
                         updatePerson.brideLastName, updatePerson.username))

                    mysql.connection.commit()
                    cur.close()
                    session['groomFirstName'] = updatePerson.groomFirstName
                    session['groomLastName'] = updatePerson.groomLastName
                    session['brideFirstName'] = updatePerson.brideFirstName
                    session['brideLastName'] = updatePerson.brideLastName

                    flash("Successfully Updated", "success")
                    return redirect(url_for("profile", setting=0))

                except:
                    flash("Email Not valid", "danger")
                    return redirect(url_for("profile", setting=0))
                    # ----------------------------


            elif (request.form['action'] == "update_contact_info"):
                updatePerson = wedding.WeddingClass()

                updatePerson.username = session['username']
                updatePerson.email = request.form["inputEmail"]
                updatePerson.contactNumber = request.form["inputContact"]

                try:

                    # Email sent to the user
                    try:

                        msg = Message('Email is Updated !',
                                      sender="legendbest123@gmail.com", recipients=[updatePerson.email])

                        msg.body = 'Your Account email is updated'

                        cur = mysql.connection.cursor()
                        cur.execute(
                            "UPDATE weddingInformation set email=%s,contactNumber=%s WHERE username = %s",
                            (updatePerson.email, updatePerson.contactNumber,
                             updatePerson.username))
                        mail.send(msg)
                        mysql.connection.commit()
                        cur.close()

                        session['email'] = updatePerson.email
                        session['contactNumber'] = updatePerson.contactNumber
                        flash("Successfully Updated", "success")
                        return redirect(url_for("profile", setting=1))

                    except:
                        flash("Email Not valid", "danger")
                        return redirect(url_for("profile", setting=1))
                    # ----------------------------

                except:
                    flash("Server is busy", "warning")
                    return redirect(url_for("profile", setting=1))

            elif (request.form['action'] == "update_wedding_informaton"):
                updatePerson = wedding.WeddingClass()
                updatePerson.timeOfMarriage = request.form["inputTime"]
                updatePerson.endTimeOfMarriage = request.form["inputEndTime"]
                updatePerson.dateOfMarriage = request.form["inputDate"]
                updatePerson.endDateOfMarriage = request.form["inputEndDate"]
                updatePerson.Location = request.form["inputLocation"]
                updatePerson.Address = request.form["inputAddress"]
                updatePerson.username = session['username']

                try:

                    cur = mysql.connection.cursor()
                    cur.execute(
                        "UPDATE weddingInformation set dateOfMarriage=%s,timeOfMarriage=%s,endDateOfMarriage=%s,endTimeOfMarriage=%s,locationName=%s,address=%s WHERE username = %s",
                        (updatePerson.dateOfMarriage,updatePerson.timeOfMarriage,updatePerson.endDateOfMarriage,updatePerson.endTimeOfMarriage, updatePerson.Location,updatePerson.Address, updatePerson.username))

                    mysql.connection.commit()
                    cur.close()

                    session['dateOfMarriage'] = updatePerson.dateOfMarriage
                    session['timeOfMarriage'] = updatePerson.timeOfMarriage
                    session['endDateOfMarriage'] = updatePerson.endDateOfMarriage
                    session['endTimeOfMarriage'] = updatePerson.endTimeOfMarriage
                    session['Location'] = updatePerson.Location
                    session['Address'] = updatePerson.Address

                    flash("Successfully Updated", "success")
                    return redirect(url_for("profile", setting=2))

                except:
                    flash("Email Not valid", "danger")
                    return redirect(url_for("profile", setting=2))
                # ----------------------------

            elif (request.form['action'] == "update_password"):
                updatePerson = wedding.WeddingClass()
                updatePerson.email = session['email']
                updatePerson.username = session['username']
                if (request.form["inputPassword"] == request.form["inputPassword1"]):
                    updatePerson.password = request.form["inputPassword"]
                    newPassword = updatePerson.password
                    updatePerson.password = generate_password_hash(updatePerson.password)

                    try:

                        # Email sent to the user
                        try:

                            msg = Message('Password Updated !',
                                          sender="legendbest123@gmail.com", recipients=[updatePerson.email])

                            msg.body = 'Your Account password is: ' + newPassword

                            cur = mysql.connection.cursor()
                            cur.execute(
                                "UPDATE weddingInformation set password=%s WHERE username = %s",
                                (updatePerson.password, updatePerson.username))
                            mail.send(msg)
                            mysql.connection.commit()
                            cur.close()

                            flash("Successfully Updated", "success")
                            return redirect(url_for("profile", setting=3))

                        except:
                            flash("Password Not updated", "danger")
                            return redirect(url_for("profile", setting=3))
                        # ----------------------------

                    except:
                        flash("Server is busy", "warning")
                        return redirect(url_for("profile", setting=3))
                else:
                    flash("Password Not Matched", "danger")
                    return redirect(url_for("profile", setting=3))

                    # URL STILL TO ADD
            # PRIVACY STILL TO ADD

            # ==============================


            elif (request.form['action'] == "update_URL"):
                updatePerson = wedding.WeddingClass()
                updatePerson.urls = request.form["inputURL"]
                updatePerson.username = session['username']

                try:
                    cur = mysql.connection.cursor()

                    # check if the user record is present or not
                    cur.execute(
                        "SELECT url FROM website WHERE username = %s",
                        (updatePerson.username,))
                    result = cur.fetchone()
                    if result is None:
                        # if no then insert
                        cur.execute("INSERT INTO website(url,username) VALUES (%s,%s)",(updatePerson.urls,updatePerson.username))
                    else:
                        # if yes then update
                        cur.execute(
                            "UPDATE website set url=%s WHERE username = %s",
                            (updatePerson.urls, updatePerson.username))
                    mysql.connection.commit()
                    cur.close()

                    session['url'] = updatePerson.urls

                    flash("Successfully Updated Url", "success")
                    return redirect(url_for("profile", setting=4))

                except:
                    flash("URL is not unique", "danger")
                    return redirect(url_for("profile", setting=4))
                # ----------------------------

            else:
                return redirect(url_for("profile"))
        else:
            return redirect(url_for("profile"))
    else:
        flash("Session Ended", "warning")
        return render_template("login.html")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


# Module : Invitation Cards
# Status :

@app.route("/invitation_cards", methods=['GET', 'POST'])
def invitation_cards():
    if 'username' in session:
        g.username = session['username']
        return render_template("invitation_cards.html")
    else:
        flash("Session Ended", "warning")
        return render_template("login.html")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


# Module : Invitation Websites
# Status : Completed

@app.route("/invitation_website", methods=['GET', 'POST'])
def invitation_website():
    if 'username' in session:
        
        if request.args.get('id'):
            id = request.args.get('id')

            # Action: Edit Website 
            # Status: 
            
            if request.args.get('action') == 'form-edit':
                # here data will be deleted from the table of previous session
                return redirect(url_for("templateEdit"))

            # Action: Preview Invitation Website
            # Status: Do Edit First

            elif request.args.get('action') == 'previewWebsite':
                if ('url' in session):
                    url = session['url']
                    return redirect(url_for('PreviewWebsite',url=url))
                else:
                    flash("Add URL!", "warning")
                    return redirect(url_for('profile',setting=4))


            # Action: Select Invitation Template
            # Status: Completed

            elif request.args.get('action') == 'form-select':
                session['template_id'] = id
                cur = mysql.connection.cursor()
                
                # check if data is present or not

                cur.execute("SELECT url FROM website where username=%s",(session['username'],))
                result = cur.fetchone()
                if (result is None):
                    # if no then insert
                    cur.execute("INSERT INTO website(templateNo,username) VALUES (%s,%s)",(id, session['username']))
                else:
                    cur.execute("UPDATE website SET templateNo = %s WHERE username = %s",(id, session['username']))
                mysql.connection.commit()
                cur.close()
                # query for storing template id in webTemplate 

                return redirect(url_for("invitation_website"))
            
            
            # Action: Preview Invitation Template
            # Status: Completed
            elif request.args.get('action') == 'openTemplate':

                cur = mysql.connection.cursor()
                return redirect(url_for("previewTemplate",id=id))

            # Action: Delete Invitation Template
            # Status: Completed
            
            elif request.args.get('action') == 'form-remove':
                cur = mysql.connection.cursor()
                cur.execute("UPDATE website SET templateNo = %s WHERE username = %s",("NULL", session['username']))
                mysql.connection.commit()
                cur.close()
                session.pop('template_id',None) 
                # query for removing template id in webTemplate
                return redirect(url_for("invitation_website"))
            else:
                return render_template(id + ".html", id=id)
        else:
            g.username = session['username']

            templates: list = []
            categoryList: list = []
            cities: list = []
            cur = mysql.connection.cursor()

            # vendor details
            cur.execute(
                '''SELECT id,Name,imagePath from website_template''',
            )
            templatesDetails = cur.fetchall()
            mysql.connection.commit()

            cur.close()

            for template in templatesDetails:
                templates.append(template)

            return render_template("invitation_website.html", templates=templates)
    else:
        flash("Session Ended", "warning")
        return render_template("login.html")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


# Module : Website Template Preview
# Status : Completed

@app.route("/template_<id>", methods=['GET', 'POST'])
def previewTemplate(id):
    if 'username' in session:
        g.username = session['username']
        return render_template(id + ".html", id=id)
    else:
        flash("Session Ended", "warning")
        return render_template("login.html")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response




# Module : User Website
# Status : Set the edit section first 


@app.route("/<url>", methods=['GET', 'POST'])
def PreviewWebsite(url):
    if 'username' in session:
        
        g.username = session['username']
        username = session['username']
        cur = mysql.connection.cursor()
        websiteInfo = WEBSITE_INFORMATION()
        
        # This is taking Title Data
        title: list = []
        cur.execute('''SELECT Title_Name,Title_Description,Title_Background FROM Website_Title WHERE username=%s''',(username,))
        result = cur.fetchone()
        if result is None:
            # title will be copied as it is empty...
            pass
        else:
            title.append(result)
        websiteInfo.title = title
        # This is taking Preparation Data
        Preparation: list = []
                
        cur.execute('''SELECT Preparation_Title,Preparation_Description,Preparation_Image FROM Website_Preparation WHERE username=%s''',(username,))
        result = cur.fetchall()
        if (result is None):
        # Preparation will be copied as it is empty...
            pass
        else:
            for prep in result:
                Preparation.append(prep)
        websiteInfo.Preparation = Preparation
        # This is taking About Us Data
        About: list = []
                    
        cur.execute('''SELECT About_Title,About_Description,About_Image FROM Website_About WHERE username=%s''',(username,))
        result = cur.fetchall()
        if (result is None):
            # About us will be copied as it is empty...
            pass
        else:
            for abt in result:
                About.append(abt)

        websiteInfo.About = About
        # This is taking Services Data
        Services: list = []
                    
        cur.execute('''SELECT Services_Name,Services_Description,Services_Image FROM Website_Services WHERE username=%s''',(username,))
        result = cur.fetchall()
        if (result is None):
            # Services will be copied as it is empty...
            pass
        else:
            for ser in result:
                Services.append(ser)

        websiteInfo.Services = Services
        # This is taking OurLoveStory Data
        OurLoveStory: list = []
                    
        cur.execute('''SELECT LoveStory_Title,LoveStory_Description,LoveStory_Image FROM Website_OurLoveStory WHERE username=%s''',(username,))
        result = cur.fetchall()
        if (result is None):
            # Love Story will be copied as it is empty...
            pass
        else:
            for ols in result:
                OurLoveStory.append(ols)
        websiteInfo.OurLoveStory = OurLoveStory
        # Now we have the data and we will pass to the template and show on screen
        
        mysql.connection.commit()
        cur.close()        




        template_id = session['template_id']
        # fetch all the data from the database and display here

        return render_template("Edit_"+template_id + ".html", websiteInfo = websiteInfo)
    else:
        flash("Session Ended", "warning")
        return render_template("login.html")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

@app.route("/update_webInfo",methods=['GET','POST'])
def update_webInfo():
    if 'username' in session:
        if request.method == "POST":
            username = session['username']
            cur = mysql.connection.cursor()
            if (request.form['action'] == 'update_title'):
                UPLOAD_FOLDER = 'static/users/'+ session['username']+"/images"
                
                if not os.path.exists('static/users/'+session['username']):
                    os.makedirs('static/users/'+session['username'])
                    os.makedirs('static/users/'+session['username']+"/images")

                app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
                app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
                app.config['UPLOAD_PATH'] = UPLOAD_FOLDER
                # try:
                file = request.files["title_background"]   
                filename = secure_filename(file.filename)
                if "title_background" not in request.files:
                        title = request.form["title"]
                        description = request.form["description"]
                        # update title and description
                        cur.execute("SELECT title_name FROM website_title where username = %s",(username,))
                        result = cur.fetchone()
                        if result is None:
                            # insert title name and description
                            cur.execute("INSERT INTO website_title(title_name,Title_Description,username) VALUES (%s,%s,%s)",
                                    (title, description, username))
                            pass
                        else:
                            # update title name and description
                            cur.execute(
                                "UPDATE website_title set title_name=%s, Title_Description=%s where username = %s",
                                (title, description, username))

                        
                else:
                        title = request.form["title"]
                        description = request.form["description"]
                        # update file if available
                        if filename != '':
                            file_ext = os.path.splitext(filename)[1]
                            if file_ext not in app.config['UPLOAD_EXTENSIONS'] or file_ext != validate_image(file.stream):
                                return "Invalid image", 400
                            filename='title_bg'+file_ext
                            file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                            path = app.config['UPLOAD_PATH']+'/'+filename
                            
                            title_background = path
                            cur.execute("SELECT title_name FROM website_title where username = %s",(username,))
                            result = cur.fetchone()
                            if result is None :
                                # insert title name, description and image_url
                                cur.execute("INSERT INTO website_title(title_name,Title_Description,Title_Background,username) VALUES (%s,%s,%s,%s)",
                                        (title, description,title_background, username))
                                pass
                            else:
                                # update title name and description
                                cur.execute(
                                    "UPDATE website_title set title_name=%s, Title_Description=%s,Title_Background=%s where username = %s",
                                    (title, description,title_background, username))
                        else:
                            mysql.connection.commit()
                            cur.close()        
                            flash("Image not uploaded", "danger")
                            return redirect(url_for("templateEdit", page=0))
                mysql.connection.commit()
                cur.close()
                flash("Successfully Updated", "success")
                return redirect(url_for("templateEdit", page=0))

                # except:
                #     flash("Title not updated", "danger")
                #     return redirect(url_for("templateEdit", page=0))
                    # ----------------------------


            else:
                return redirect(url_for("profile"))
        else:
            return redirect(url_for("profile"))
    else:
        flash("Session Ended", "warning")
        return render_template("login.html")

   

# Module : Edit Template
# Status : 

@app.route("/edit_template", methods=['GET', 'POST'])
def templateEdit():
    if 'username' in session:
        g.username = session['username']
        
        username = session['username']
        cur = mysql.connection.cursor()
        cur.execute('''SELECT url,templateNo FROM website WHERE username=%s''',(username,))
        result = cur.fetchone()
        if (result is None or result[0] == 'NULL' or result[0]=='' or result[0] is None):
            flash("Add URL!", "warning")
            return redirect(url_for('profile',setting=4))
        elif (result[1] == 'NULL'  or result[1] ==''):
            flash("You haven't selected Any Design!", "warning")
            return redirect(url_for('invitation_website'))
        else:    
            url = result[0]
            templateNo = result[1]
            websiteInfo = WEBSITE_INFORMATION()
            websiteInfo.template_id = templateNo
            websiteInfo.username=username
            websiteInfo.url=url
            if request.method == "POST":


                # Module : Preview Template
                # Status : 
                if request.form['action'] == 'previewTemplate':
                    return redirect(url_for("PreviewWebsite",url = websiteInfo.url))
        
            else:
            # This is taking Title Data
                title: list = []
                cur.execute(
                            '''SELECT Title_Name,Title_Description,Title_Background FROM Website_Title WHERE username=%s''',
                            (websiteInfo.username,))
                result = cur.fetchone()
                if result is None:
                    pass
                else:
                    title.append(result)
                websiteInfo.title = title
                # This is taking Preparation Data
                Preparation: list = []
                
                cur.execute(
                            '''SELECT Preparation_Title,Preparation_Description,Preparation_Image FROM Website_Preparation WHERE username=%s''',
                            (websiteInfo.username,))
                result = cur.fetchall()
                if (result is None):
                    pass
                else:
                    for prep in result:
                        Preparation.append(prep)

                    websiteInfo.Preparation = Preparation
                # This is taking About Us Data
                About: list = []
                    
                cur.execute(
                            '''SELECT About_Title,About_Description,About_Image FROM Website_About WHERE username=%s''',
                            (websiteInfo.username,))
                result = cur.fetchall()
                if (result is None):
                    pass
                else:
                    for abt in result:
                        About.append(abt)

                    websiteInfo.About = About
                # This is taking Services Data
                Services: list = []
                    
                cur.execute(
                            '''SELECT Services_Name,Services_Description,Services_Image FROM Website_Services WHERE username=%s''',
                            (websiteInfo.username,))
                result = cur.fetchall()
                if (result is None):
                    pass
                else:
                    for ser in result:
                        Services.append(ser)

                    websiteInfo.Services = Services
                # This is taking OurLoveStory Data
                OurLoveStory: list = []
                    
                cur.execute(
                            '''SELECT LoveStory_Title,LoveStory_Description,LoveStory_Image FROM Website_OurLoveStory WHERE username=%s''',
                            (websiteInfo.username,))
                result = cur.fetchall()
                if (result is None):
                    pass
                else:
                    for ols in result:
                        OurLoveStory.append(ols)
                    websiteInfo.OurLoveStory = OurLoveStory
                # Now we have the data and we will pass to the template and show on screen
                session['websiteInfo'] = websiteInfo.__dict__
                mysql.connection.commit()
                cur.close()
                return render_template("edit_template.html",websiteInfo=websiteInfo)

    else:
        flash("Session Ended", "warning")
        return render_template("login.html")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response



@app.route("/gifts", methods=['GET'])
def Gifts():
    if 'username' in session:
        g.username = session['username']

        if request.args.get('product_type'):

            # Select all query
            product_type = request.args.get('product_type')

            Gifts: list = []
            cur = mysql.connection.cursor()
            if (product_type == "All"):
                # vendor details
                cur.execute(
                    '''SELECT productimagesrc,producttitle,price,productlinkhref,id,product_type FROM gifts where product_type!=%s''',
                    ('Others',))
            else:
                cur.execute(
                    '''SELECT productimagesrc,producttitle,price,productlinkhref,id,product_type FROM gifts where product_type = %s''',
                    (product_type,))
            gifts = cur.fetchall()
            mysql.connection.commit()

            cur.close()

            for gift in gifts:
                Gifts.append(gift)
            return render_template("gifts.html", gifts=Gifts)

            return render_template("gifts.html")
        else:
            # Select all query
            Gifts: list = []
            cur = mysql.connection.cursor()

            # vendor details
            cur.execute(
                '''SELECT productimagesrc,producttitle,price,productlinkhref,id,product_type FROM gifts where product_type!=%s''',
                ('Others',))
            gifts = cur.fetchall()
            mysql.connection.commit()

            cur.close()

            for gift in gifts:
                Gifts.append(gift)
            return render_template("gifts.html", gifts=Gifts)

            return render_template("gifts.html")
    else:
        flash("Session Ended", "warning")
        return render_template("login.html")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@app.route("/registry", methods=['GET', 'POST'])
def Registry_Gifts():
    if 'username' in session:

        if request.method == "GET":
            g.username = session['username']
            username = session['username']
            # Select all query
            RegistryData: list = []
            cur = mysql.connection.cursor()

            # vendor details
            cur.execute(
                '''SELECT * FROM item_cart where username = %s''', [username])
            registries = cur.fetchall()
            mysql.connection.commit()

            cur.close()

            for registry in registries:
                RegistryData.append(registry)

            return render_template("registry.html", RegistryData=RegistryData)
        elif (request.form['action'] == "removeCart"):
            username = session['username']
            id = request.form['id']
            cur = mysql.connection.cursor()

            # vendor details
            cur.execute(
                '''DELETE FROM item_cart where username = %s AND itemID = %s''',
                ([username], id))

            cur.execute("SELECT count(itemName) FROM item_cart where username=%s", ([username],))
            registries = cur.fetchone()
            session['registries'] = registries[0]

            mysql.connection.commit()
            cur.close()
            flash("Successfully Deleted", "success")
            return redirect(url_for("Registry_Gifts"))

    else:
        flash("Session Ended", "warning")
        return render_template("login.html")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


# FOR SIGN UP AND LOGIN PAGE ##

####################################
# BACKEND: COMPLETED
# FRONTEND: COMPLETED
####################################


# @app.route("/signup", methods=['GET', 'POST'])
# def signup():
#     if 'email' in session:
#         g.email = session['email']
#         return redirect(url_for('guidelines'))
#     else:
#         if request.method == 'GET':
#             return render_template('signup.html')

#         else:
#             if request.form['action'] == "Signup":
#                 email = request.form['email']
#                 fname = request.form['fname']
#                 lname = request.form['lname']
#                 password = request.form['password']
#                 organization = request.form['organization']

#                 hashedPassword = generate_password_hash(password)
#                 errormsg = ErrorMessages()
#                 try:
#                     cur = mysql.connection.cursor()
#                     cur.execute("INSERT INTO users(fname,lname,email,password,organization) VALUES (%s,%s,%s,%s,%s)",
#                                 (fname, lname, email, hashedPassword, organization))
#                     token = token_key.dumps(email, salt='email-confirmation')
#                     msg = Message('Email Confirmation from opTeam',
#                                   sender="legendbest123@gmail.com", recipients=[email])
#                     link = url_for('confirmEmail', token=token, _external=True)
#                     msg.body = 'Your confirmation link is : {}'.format(link)
#                     mail.send(msg)
#                     # Token is generated sent to the email for confirmation
#                     errormsg.confirmationMessage()
#                     mysql.connection.commit()
#                     cur.close()
#                     return render_template('signup.html', signup=errormsg)
#                 except IntegrityError:
#                     errormsg.emailExist()
#                 except SMTPAuthenticationError:
#                     errormsg.serverBusy()
#                 except:
#                     errormsg.emailExist()
#                 return render_template('signup.html', signup=errormsg)

#             elif request.form['action'] == "Login":
#                 errormsg = ErrorMessages()
#                 session.pop('email', None)
#                 session.pop('name', None)
#                 email = request.form['email-login']
#                 password = request.form['password-login']
#                 try:
#                     cur = mysql.connection.cursor()
#                     cur.execute(
#                         '''SELECT fname,lname,email,password,organization FROM users WHERE email=%s and confirmation=%s''', (email, 1))
#                     person = cur.fetchone()
#                     if person is None:
#                         errormsg.emailIncorrect()
#                     else:
#                         if check_password_hash(person[3], password):
#                             session['name'] = person[0] + ' ' + person[1]
#                             session['email'] = person[2]
#                             session['fname'] = person[0]
#                             session['lname'] = person[1]
#                             session['organization'] = person[4]
#                             mysql.connection.commit()
#                             return redirect(url_for('guidelines'))
#                         else:
#                             errormsg.passwordIncorrect()
#                 except:
#                     errormsg.serverBusy()
#         return render_template('signup.html', login=errormsg)

# # FOR CONFIRM EMAIL #


# @app.after_request
# def after_request(response):
#     response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     return response


# @app.route('/confirm-email<token>')
# def confirmEmail(token):

#     errormsg = ErrorMessages()
#     try:
#         email = token_key.loads(token, salt='email-confirmation', max_age=3600)
#         cur = mysql.connection.cursor()
#         cur.execute("UPDATE users SET confirmation = %s WHERE email = %s",
#                     (1, email))

#         msg = Message('Email Confirmation from opTeam',
#                       sender="legendbest123@gmail.com", recipients=[email])
#         msg.body = 'Your email is confirmed.\n Thanks you for using OPTEAM'
#         mail.send(msg)

#         errormsg.emailConfirmed()
#         mysql.connection.commit()
#         cur.close()
#     except SignatureExpired:
#         errormsg.tokenExpired()

#     return render_template('signup.html', signup=errormsg)


# @app.after_request
# def after_request(response):
#     response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     return response
# FOR FORGET PASSWORD #


"""
Requirement: Functional Requirement
Type: Compulsory
"""


####################################
# BACKEND:  COMPLETED
# FRONTEND: COMPLETED
####################################


@app.route("/logout")
def logout():
    if 'username' in session:
        session.pop('email', None)
        session.pop('username', None)
        session.pop('groomFirstName', None)
        session.pop('groomLastName', None)
        session.pop('brideFirstName', None)
        session.pop('brideLastName', None)
        session.pop('dateOfMarriage', None)
        session.pop('placeOfMarriage', None)
        session.pop('contactNumber', None)
        session.pop('template_id',None)
        session.pop('websiteInfo',None)
        session.pop('guests',None)
        session.pop('registries',None)
        session.pop('url',None)
        session.pop('url',None)
        flash("Account Logged Out", "success")
        return redirect(url_for('login'))
    else:
        flash("Access Denied", "danger")
        return render_template("login.html")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


if __name__ == "__main__":
    app.run("127.0.0.1", port=3000, debug=True)
