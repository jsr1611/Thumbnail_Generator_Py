import cv2
import os
import mysql.connector
from mysql.connector import Error

# db_settings
db_host = ''        # change to host ip
db_name = ''        # change to db name
db_user = ''        # change to db user name
db_password = ''    # change to db password
db_table = ''       # change to db table name


SQL_SELECT_QUERY = 'SELECT * FROM ' + db_name + '.' + db_table + ' LIMIT 10'
# change it to fit your needs, ex: SELECT * FROM green.lesson WHERE course_id >= 1498 ORDER BY id;

folder_name = ''
img_path = ''


def generate_thumbnail(video_path):
    global folder_name, img_path
    try:
        video_captured = cv2.VideoCapture(video_path)
        success, image = video_captured.read()
        # for i in range(1):
        width = int(image.shape[1] * 0.4)
        height = int(image.shape[0] * 0.4)
        image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
        if not os.path.exists(folder_name):  # create directory if not exists
            os.mkdir(folder_name)
        cv2.imwrite(folder_name + '\\' + img_path, image)  # save frame as JPEG file
        # success, image = vidcap.read()
        return 'Thumbnail image generated: ' + img_path + '  successfully'
    except AttributeError:
        return 'video_file_error: ' + video_path
    except Exception as errorMsg:
        return errorMsg


def main():
    global folder_name, img_path
    connection = None
    cursor = None
    try:
        connection = mysql.connector.Connect(host=db_host,
                                             database=db_name,
                                             user=db_user,
                                             password=db_password)

        db_info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_info)
        cursor = connection.cursor()
        cursor.execute(SQL_SELECT_QUERY)
        results = cursor.fetchall()  # Fetching all results

        for data in results:
            # print(data)
            # change below data according to your needs
            lesson_id = data[5]
            course_id = data[4]
            video_link = data[3]
            folder_name = str(course_id)        # set folder name dynamically
            img_path = str(lesson_id) + ".jpg"  # set image path dynamically
            if not os.path.exists(folder_name + '/' + img_path):
                # print('courseId: ' + str(course_id) + ', lesson_index: ' +
                # str(lesson_id) + ', videoLink: ' + video_link)
                result_text = generate_thumbnail(video_link)
                print(result_text)
            else:
                print("Thumbnail already exists: " + folder_name + '/' + img_path)
        print("The job is done.")

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


if __name__ == "__main__":
    main()
