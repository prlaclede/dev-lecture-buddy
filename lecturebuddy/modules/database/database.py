import psycopg2, psycopg2.extras

def connectToDB():
  #connectionString = 'dbname=lecturebuddy user=postgres password=beatbox host=localhost'
  connectionString = 'dbname=lecturebuddy user=lecturebuddyuser password=lecturebuddyp@$$ host=localhost'
  try:
    return psycopg2.connect(connectionString)
  except:
    print("Can't connect to database")