from flask import Flask, request, render_template,redirect,jsonify,url_for,send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import uuid
import base64
import psycopg2 
from sqlalchemy import text

import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(app)



class Postdata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid= db.Column(db.String(200))
    postid = db.Column(db.String(200))
    title = db.Column(db.String(200))
    description = db.Column(db.String(500))
    content = db.Column(db.String(500))
    created = db.Column(db.String(500))
    category = db.Column(db.String(500))
    selected = db.Column(db.String(50))
    imageurl = db.Column(db.String(500))
    color = db.Column(db.String(500))

class HomeData(db.Model):
    __tablename__ = 'homedata'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(200))
    titlefirst = db.Column(db.String(200))
    titlesecond = db.Column(db.String(500))
    linkurlcv = db.Column(db.String(500))
    logourl = db.Column(db.String(200))


class HomeDataImage(db.Model):
    __tablename__ = 'homedataimage'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(200))
    homeid = db.Column(db.String(200))
    image_url = db.Column(db.String(200))
    linkurlmedia = db.Column(db.String(200))

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')
 





# Cloudinary configuration
cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET")
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')  

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    print(f"Created uploads folder at: {UPLOAD_FOLDER}")

# Route to serve uploaded files
# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     try:
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         print(f"Attempting to serve file from: {file_path}")
#         return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
#     except Exception as e:
#         print(f"Error serving file {filename}: {str(e)}")
#         return jsonify({'error': f'File {filename} not found'}), 404


# # Function to save the image to the uploads folder
# def save_image_to_folder(image_data, image_format):
#     unique_filename = f"{uuid.uuid4()}.{image_format.lower()}"  # Ensure lowercase extension
#     file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
#     try:
#         with open(file_path, 'wb') as f:
#             f.write(image_data)
#         print(f"Successfully saved image to: {file_path}")
#         return unique_filename
#     except Exception as e:
#         print(f"Error saving image: {str(e)}")
#         raise

# Route to handle image uploads
# @app.route("/upload", methods=['POST'])
# def upload():
#     print("Received upload request")
    
#     if 'featuredPhoto' not in request.files:
#         print("No file part in request")
#         return jsonify({'error': 'No file part'}), 400

#     photo = request.files['featuredPhoto']

#     if photo.filename == '':
#         print("No file selected")
#         return jsonify({'error': 'No selected file'}), 400

#     try:
#         image_binary = photo.read()
#         image_format = photo.filename.split('.')[-1].lower()  # Get the file extension
#         image_filename = save_image_to_folder(image_binary, image_format)

#         # Construct the correct image URL for the frontend
#         image_url = f"uploads/{image_filename}"
#         print(f"Generated image URL: {image_url}")

#         return jsonify({'image_url': image_url}), 200
#     except Exception as e:
#         print(f"Error processing upload: {str(e)}")
#         return jsonify({'error': 'Failed to process upload'}), 500


@app.route("/upload", methods=['POST']) 
def upload_image():
    if 'featuredPhoto' not in request.files:
        print("No file part in request")
        return jsonify({'error': 'No file uploaded'}), 400

    photo = request.files['featuredPhoto']


# Debug environment variables
    print("Cloudinary Config:")
    print(f"CLOUD_NAME: {os.environ.get('CLOUDINARY_CLOUD_NAME')}")
    print(f"API_KEY: {os.environ.get('CLOUDINARY_API_KEY')}")
    print(f"API_SECRET: {os.environ.get('CLOUDINARY_API_SECRET')}")

    if photo.filename == '':
        print("No file selected")
        return jsonify({'error': 'No selected file'}), 400

    try:
        print(f"Received file: {photo.filename}")
        # Upload the file to Cloudinary
        upload_result = cloudinary.uploader.upload(
            photo,
            folder="uploads",  # Optional: organize uploads in a folder
            resource_type="image",
            use_filename=True,
            unique_filename=True
        )
        image_url = upload_result.get("secure_url")
        print(f"Uploaded to Cloudinary: {image_url}")

        # # Optionally, optimize the image URL
        # optimize_url, _ = cloudinary_url(
        #     upload_result["public_id"],
        #     fetch_format="auto",
        #     quality="auto",
        #     width=500,
        #     height=500,
        #     crop="auto",
        #     gravity="auto"
        # )
        # print(f"Optimized URL: {optimize_url}")

        return jsonify({'image_url': image_url}), 200
    except Exception as e:
        print(f"Error uploading to Cloudinary: {str(e)}")
        return jsonify({'error': str(e)}), 500
    


@app.route("/getdata", methods = ['POST'])
def getdata():
    try:
        print("sdfsdfsf")
        data=request.get_json(force=True)
        print("asdadasdasdas---------->",data)
        userid= data['userid']
        postid= str(uuid.uuid4())
        title = data['title']
        description = data['description']
        content = data['content']
        created = data['created']
        category = data['category']
        selected = data['selected']
        image_url = data['featuredPhoto']
        color = data['color']

        new_post = Postdata(userid=userid,postid=postid, title=title, description=description, content=content, created=created,
                            category=category, selected=selected, imageurl=image_url,color=color)
        db.session.add(new_post)
        db.session.commit()
    

        return jsonify({'status':200})
    except :
         return jsonify({'status':500})


@app.route("/getdatax", methods = ['GET'])
def getdatax():

    userid=request.args.get('userid', None)
    print("------getting data-------",userid)


    sql_query = text("""SELECT * FROM postdata 
                 ORDER BY created DESC""")

    result = db.session.execute(sql_query,{"userid": userid})

    # Convert the result to a list of dictionaries for JSON serialization
    posts_data = [
        {   'userid':row.userid,
            'postid': row.postid,
            'title': row.title,
            'description': row.description,
            'content': row.content,
            'created': row.created,
            'category': row.category,
            'selected': row.selected,
            'image_url': row.imageurl,
            'color': row.color,
        }
        for row in result.fetchall()
    ]
    return jsonify(posts_data)

@app.route("/update_selected", methods=['POST'])
def update_selected():
    try:
        data = request.get_json(force=True)
        post_ids = tuple(data['settleList'])  # Ensure it's a tuple for SQL IN clause
        userid = str(data['userid'])
        print("update list --->", post_ids)
        # Corrected SQL Queries
        sql_reset = text("UPDATE postdata SET selected = 'false' WHERE userid = :userid")
        sql_update = text("UPDATE postdata SET selected = 'true' WHERE postid IN :post_ids")

        with db.engine.connect() as connection:
            connection.execute(sql_reset, {"userid": userid})
            if post_ids: 
                connection.execute(sql_update, {"post_ids": post_ids})
            connection.commit()

        print("Rows updated successfully")
        return jsonify({'status': 200})
    
    except Exception as e:
        print("Error updating posts:", str(e))
        return jsonify({'status': 500, 'error': str(e)})


@app.route("/delete_item", methods=['POST'])
def delete_item():
    try:
        print("Received delete request")
        data = request.get_json(force=True)
        post_id = data['id']
        userid = str(data['userid'])
        print(f"Item to delete: post_id={post_id}, userid={userid}")

        # Retrieve the post from the database
        post = Postdata.query.filter_by(postid=post_id, userid=userid).first()

        if not post:
            print("Post not found in database")
            return jsonify({'error': 'Post not found'}), 404

        # Handle image deletion
        if post.imageurl:
            # Extract the filename from the imageurl (e.g., 'uploads/829108c7-d511-4c2a-aff0-522d3382c307.png')
            image_filename = os.path.basename(post.imageurl)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            print(f"Attempting to delete image: {image_path} (absolute path: {os.path.abspath(image_path)})")

            # Check if the image file exists and delete it
            if os.path.exists(image_path):
                os.remove(image_path)
                print(f"Image deleted successfully: {image_path}")
            else:
                print(f"Image file not found at: {image_path}")
        # Delete the post from the database
        db.session.delete(post)
        db.session.commit()
        print(f"Post deleted successfully: post_id={post_id}")

        return jsonify({'status': 200, 'message': 'Post and associated image deleted successfully'})

    except Exception as e:
        db.session.rollback()  # Rollback the database session in case of error
        print(f"Error deleting item: {str(e)}")
        return jsonify({'status': 500, 'error': str(e)}), 500


@app.route("/update_item", methods=['POST'])
def update_item():
    try:
            # Parse the JSON data from the request body
            data = request.get_json(force=True)
            postid = data.get('id') 
            userid = str(data.get('userid') )
            title = data.get('title')
            description = data.get('description')
            content = data.get('content')
            created = data.get('created')
            category = data.get('category')
            selected = data.get('selected')
            image_url = data.get('featuredPhoto')
            color =  data.get('color')


            item = Postdata.query.filter_by(postid=postid).filter_by(userid=userid).first()

            # Check if the item exists
            if not item:
                return jsonify({'error': 'Item not found'}), 404

            item.title = title
            item.description = description
            item.content = content
            item.created = created
            item.category = category
            item.selected = selected
            item.imageurl = image_url
            item.color = color

            # Commit the changes to the database
            db.session.commit()

            return jsonify({'status':200})
    except :
         return jsonify({'status':500})


 
@app.route('/posthomedata', methods=['POST'])
def insert_data():

    try:
                new_post =  request.get_json(force=True)

                # Check if user exists
                user_data = HomeData.query.filter_by(userid='1').first()
                if not user_data:
                    # If user doesn't exist, create a new record in HomeData
                    new_data = HomeData(userid='1', titlefirst=new_post['titlefirst'], titlesecond=new_post['titlesecond'], linkurlcv=new_post['linkurlcv'],logourl=new_post['logourl'])
                    db.session.add(new_data)
                    db.session.commit()
                    home_id = new_data.id
                else:
                    # If user exists, update existing record
                    user_data.titlefirst = new_post['titlefirst']
                    user_data.titlesecond = new_post['titlesecond']
                    user_data.linkurlcv = new_post['linkurlcv']
                    user_data.logourl = new_post['logourl']
                    db.session.commit()
                    home_id = user_data.id
                HomeDataImage.query.filter_by(userid='1').delete()
                db.session.commit()
 
                # Insert new data into HomeDataImage
                for updated_item in new_post['featuredPhoto']:
                    new_image_data = HomeDataImage(userid='1', homeid=str(home_id), image_url=updated_item['imageprevurl'], linkurlmedia=updated_item['linkUrl'])
                    db.session.add(new_image_data)
                db.session.commit()
                return jsonify({'status':200})
    except :
         return jsonify({'status':500})



@app.route('/userdata', methods=['GET'])
def get_user_data():
    sql_query = text("SELECT * FROM homedata")
    sql_query2=text("SELECT * FROM homedataimage")
    with db.engine.connect() as connection:
        result = connection.execute(sql_query) 
        result2 = connection.execute(sql_query2) 
        data = [dict(row) for row in result.mappings()]  
        data2 = [dict(row) for row in result2.mappings()]  
        alldata={'profile':data,'media':data2}

    print("----data----", alldata) 
    return jsonify(alldata)  





if __name__ == "__main__":
    app.run(debug=True)
    
    
    
