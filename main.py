from scraping.scraping import main as rdbms
from scraping.new import main
import schedule
import time

previous_return_value = None
def job():
  global previous_return_value
  previous_return_value = main(previous_return_value)
  rdbms()
schedule.every().day.at("23:00").do(job)
while True:
    schedule.run_pending()
    time.sleep(1)

# from scraping.new import get_og_image
# from utils.mongo import create_og_image, update_image
# a = create_og_image()
# for i in a:
#   og_image = get_og_image(i['id'])
#   if og_image == False:
#     continue
#   update_image(i['id'], og_image)

# from utils.sandbox import only_clustering_mongo
# only_clustering_mongo()